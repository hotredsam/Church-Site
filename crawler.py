import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import csv
import re
from pathlib import Path

# --- Configuration ---
ROOT_DIR = r"C:\Users\hotre\OneDrive\Desktop\Kaleo Website Bot"
ARCHIVE_DIR_NAME = "site_archive"
BASE_URL = "https://www.kaleoalaska.org/"
DOMAIN = "kaleoalaska.org"

# Ensure we are in the correct directory
os.chdir(ROOT_DIR)

# Setup directories
ARCHIVE_PATH = os.path.join(ROOT_DIR, ARCHIVE_DIR_NAME)
HTML_DIR = os.path.join(ARCHIVE_PATH, "html")
IMAGES_DIR = os.path.join(ARCHIVE_PATH, "images")
DOCS_DIR = os.path.join(ARCHIVE_PATH, "documents")

for d in [ARCHIVE_PATH, HTML_DIR, IMAGES_DIR, DOCS_DIR]:
    os.makedirs(d, exist_ok=True)

# CSV Files
INVENTORY_FILE = os.path.join(ROOT_DIR, "kaleo_inventory.csv")
BROKEN_LINKS_FILE = os.path.join(ROOT_DIR, "broken_links.csv")

# Initialize CSVs
def init_csvs():
    with open(INVENTORY_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Original_URL', 'Local_File_Path', 'Page_Title', 'Asset_Type', 'AI_Summary', 'Word_Count'])
    
    with open(BROKEN_LINKS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Source_URL', 'Broken_Link', 'Status_Code'])

init_csvs()

# --- Helpers ---

def get_safe_filename(url, ext=".html"):
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path:
        filename = "index"
    else:
        filename = re.sub(r'[^a-zA-Z0-9_\-]', '_', path)
    
    # Avoid duplicate filenames in flat directory by appending hash or counter if needed, 
    # but for now, let's keep it simple. If it gets too long, truncate.
    return filename[:200] + ext

def is_internal(url):
    return DOMAIN in urlparse(url).netloc

def generate_summary(text_content):
    """
    Generates a summary of the text content.
    For now, extracts the first 200 characters as a fallback.
    """
    cleaned_text = ' '.join(text_content.split())
    if not cleaned_text:
        return "No content found."
    
    # Placeholder for LLM integration
    # if api_key: ... call LLM ...
    
    return cleaned_text[:200] + "..." if len(cleaned_text) > 200 else cleaned_text

def log_inventory(original_url, local_path, page_title, asset_type, ai_summary, word_count):
    with open(INVENTORY_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([original_url, local_path, page_title, asset_type, ai_summary, word_count])

def log_broken_link(source_url, broken_link, status_code):
    with open(BROKEN_LINKS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([source_url, broken_link, status_code])

# --- Crawler ---

def download_asset(url, source_url):
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code != 200:
            log_broken_link(source_url, url, response.status_code)
            return None
        
        content_type = response.headers.get('content-type', '').lower()
        ext = ''
        target_dir = ''
        asset_type = 'Unknown'

        if 'pdf' in content_type:
            ext = '.pdf'
            target_dir = DOCS_DIR
            asset_type = 'PDF'
        elif 'word' in content_type or url.endswith(('.doc', '.docx')):
            ext = '.docx' # simplified
            target_dir = DOCS_DIR
            asset_type = 'Word Doc'
        elif 'image' in content_type:
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
            elif 'png' in content_type:
                ext = '.png'
            else:
                return None # Skip other images for now if not requested
            target_dir = IMAGES_DIR
            asset_type = 'Image'
        else:
            return None

        filename = get_safe_filename(url, ext)
        local_path = os.path.join(target_dir, filename)
        
        # Don't redownload if exists (optional optimization, but good for restartability)
        if not os.path.exists(local_path):
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        return {
            'local_path': local_path,
            'asset_type': asset_type,
            'filename': filename
        }

    except Exception as e:
        print(f"Error downloading asset {url}: {e}")
        return None

def crawl():
    queue = [BASE_URL]
    visited = set()
    
    print(f"Starting crawl from {BASE_URL}")

    while queue:
        url = queue.pop(0)
        
        # Normalize URL
        if url.endswith("/"):
            url = url[:-1]
        
        if url in visited:
            continue
        visited.add(url)
        
        print(f"Crawling: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                log_broken_link("N/A", url, response.status_code)
                continue
            
            # Save HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract Main Content (heuristic)
            # Try to find common content wrappers or just body
            content_div = soup.find('main') or soup.find('div', class_='content') or soup.body
            text_content = content_div.get_text(separator=' ', strip=True) if content_div else ""
            
            page_title = soup.title.string if soup.title else "No Title"
            summary = generate_summary(text_content)
            word_count = len(text_content.split())
            
            filename = get_safe_filename(url, ".html")
            local_html_path = os.path.join(HTML_DIR, filename)
            
            with open(local_html_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            log_inventory(url, local_html_path, page_title, "HTML", summary, word_count)
            
            # Find Links and Assets
            for link in soup.find_all(['a', 'img', 'link']):
                href = link.get('href') or link.get('src')
                if not href:
                    continue
                
                full_url = urljoin(url, href)
                parsed_full = urlparse(full_url)
                
                # Filter out irrelevant links (mailto, tel, javascript)
                if parsed_full.scheme not in ('http', 'https'):
                    continue

                path_lower = parsed_full.path.lower()
                is_asset = path_lower.endswith(('.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png'))

                if is_asset:
                    asset_info = download_asset(full_url, url)
                    if asset_info:
                        log_inventory(full_url, asset_info['local_path'], Path(asset_info['filename']).stem, asset_info['asset_type'], "Asset", 0)
                elif is_internal(full_url):
                    # It's a page, add to queue
                     # remove fragments
                    clean_url = full_url.split('#')[0]
                    if clean_url.endswith("/"):
                        clean_url = clean_url[:-1]
                    
                    if clean_url not in visited and clean_url not in queue:
                         queue.append(clean_url)

            time.sleep(1) # Be nice to the server

        except Exception as e:
            print(f"Failed to crawl {url}: {e}")

    print("Crawl complete.")

if __name__ == "__main__":
    crawl()
