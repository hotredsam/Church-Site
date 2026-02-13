import os
import csv
import shutil
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import re
from pathlib import Path

# --- Configuration ---
ROOT_DIR = r"C:\Users\hotre\OneDrive\Desktop\Kaleo Website Bot"
PROCESSED_DIR_NAME = "processed_content"
INVENTORY_FILE = os.path.join(ROOT_DIR, "kaleo_inventory.csv")
MANIFEST_FILE = os.path.join(ROOT_DIR, "content_manifest.csv")

# Ensure we are in the correct directory
os.chdir(ROOT_DIR)

# Setup directories
PROCESSED_PATH = os.path.join(ROOT_DIR, PROCESSED_DIR_NAME)
IMAGES_DIR = os.path.join(PROCESSED_PATH, "images")

for d in [PROCESSED_PATH, IMAGES_DIR]:
    os.makedirs(d, exist_ok=True)

# Initialize Manifest CSV
def init_manifest():
    with open(MANIFEST_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Original_URL', 'Clean_Markdown_Path'])

def log_manifest(original_url, markdown_path):
    with open(MANIFEST_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([original_url, markdown_path])

def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted tags
    for tag in soup(['header', 'footer', 'nav', 'script', 'style', 'noscript', 'iframe']):
        tag.decompose()
        
    # Also remove elements by class/id that are likely noise (heuristic based on common names)
    noise_selectors = [
        '.nav', '.navigation', '.footer', '.header', '.menu', '.sidebar', 
        '#nav', '#navigation', '#footer', '#header', '#menu', '#sidebar',
        '.cookie-consent', '.popup', '.modal', '.advertisement', '.social-share',
        '.search-box', '#banner', '.banner-text', '#waves', '#nav-drawer' # Kaleo specific
    ]
    
    for selector in noise_selectors:
        for element in soup.select(selector):
            element.decompose()

    # Get the main content if possible
    # We try to narrow down to 'main' or specific content divs if they exist
    content_area = soup.find('main') or soup.find('div', class_='content') or soup.find('div', id='content')
    
    if content_area:
        return str(content_area)
    
    return str(soup.body) if soup.body else str(soup)

def get_safe_filename(title):
    # Sanitize title for filename
    clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
    clean_title = clean_title.replace(" ", "_").strip()
    return clean_title[:200] # truncate if too long

def process_content():
    init_manifest()
    
    print("Reading inventory...")
    
    with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    print(f"Found {len(rows)} items to process.")
    
    for row in rows:
        original_url = row['Original_URL']
        local_path = row['Local_File_Path']
        page_title = row['Page_Title']
        asset_type = row['Asset_Type']
        
        if not os.path.exists(local_path):
            print(f"Warning: File not found {local_path}")
            continue
            
        if asset_type == 'HTML':
            try:
                with open(local_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                cleaned_html = clean_html(html_content)
                markdown_content = md(cleaned_html, heading_style="ATX")
                
                # Add Metadata header to markdown
                markdown_content = f"---\ntitle: {page_title}\nurl: {original_url}\n---\n\n" + markdown_content
                
                filename = get_safe_filename(page_title) + ".md"
                # Handle duplicate filenames
                counter = 1
                base_filename = filename
                while os.path.exists(os.path.join(PROCESSED_PATH, filename)):
                     filename = f"{os.path.splitext(base_filename)[0]}_{counter}.md"
                     counter += 1
                     
                output_path = os.path.join(PROCESSED_PATH, filename)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                    
                log_manifest(original_url, output_path)
                print(f"Processed HTML: {page_title}")
                
            except Exception as e:
                print(f"Error processing HTML {local_path}: {e}")

        elif asset_type == 'Image':
            try:
                # Copy image
                filename = os.path.basename(local_path)
                target_path = os.path.join(IMAGES_DIR, filename)
                shutil.copy2(local_path, target_path)
                print(f"Copied Image: {filename}")
            except Exception as e:
                print(f"Error copying image {local_path}: {e}")
                
    print("Processing complete.")

if __name__ == "__main__":
    process_content()
