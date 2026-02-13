import os
import json
import shutil
import re
import csv

# Configuration
ROOT_DIR = r"C:\Users\hotre\OneDrive\Desktop\Kaleo Website Bot"
PROJECT_DIR = os.path.join(ROOT_DIR, "kaleo-web")
CONTENT_DIR = os.path.join(PROJECT_DIR, "content")
PUBLIC_IMAGES_DIR = os.path.join(PROJECT_DIR, "public", "images")
PROCESSED_CONTENT_DIR = os.path.join(ROOT_DIR, "processed_content")
SOURCE_IMAGES_DIR = os.path.join(PROCESSED_CONTENT_DIR, "images")
MIGRATION_MAP_FILE = os.path.join(ROOT_DIR, "migration_map.json")
INVENTORY_FILE = os.path.join(ROOT_DIR, "kaleo_inventory.csv")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def sanitize_filename(name):
    # Remove invalid characters for Windows paths
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    return name.strip()

def load_image_map():
    mapping = {}
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Asset_Type'] == 'Image':
                    url = row['Original_URL']
                    local_path = row['Local_File_Path']
                    # We only care about filename since all images are flat in /images/
                    filename = os.path.basename(local_path)
                    mapping[url] = filename
                    
                    # Also map the filename itself in case markdown has relative path
                    # (though less likely if we see absolute URLs)
    return mapping

def seed():
    print(f"Seeding project at {PROJECT_DIR}...")
    
    if not os.path.exists(PROJECT_DIR):
        print(f"Error: Project directory {PROJECT_DIR} does not exist. Please run 'npx create-next-app' first.")
        return

    # 1. Load Data
    print(f"Loading migration map from {MIGRATION_MAP_FILE}...")
    with open(MIGRATION_MAP_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Loading image inventory from {INVENTORY_FILE}...")
    image_map = load_image_map()
    print(f"Loaded {len(image_map)} image mappings.")

    # 2. Copy Images
    print(f"Copying images from {SOURCE_IMAGES_DIR} to {PUBLIC_IMAGES_DIR}...")
    ensure_dir(PUBLIC_IMAGES_DIR)
    
    if os.path.exists(SOURCE_IMAGES_DIR):
        image_count = 0
        for filename in os.listdir(SOURCE_IMAGES_DIR):
            src = os.path.join(SOURCE_IMAGES_DIR, filename)
            dst = os.path.join(PUBLIC_IMAGES_DIR, filename)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
                image_count += 1
        print(f"Copied {image_count} images.")
    else:
        print("No source images directory found.")
    
    # 3. Process Content
    print("Processing content files...")
    ensure_dir(CONTENT_DIR)
    
    file_count = 0
    for filename, info in data.items():
        if info.get("action") == "Ignore":
            continue
            
        new_section = info.get("new_section", "Uncategorized")
        
        # Handle path separators and sanitization
        parts = new_section.replace('\\', '/').split('/')
        safe_parts = [sanitize_filename(p) for p in parts]
        section_path = os.path.join(*safe_parts)
        
        target_dir = os.path.join(CONTENT_DIR, section_path)
        ensure_dir(target_dir)
        
        src_file = os.path.join(PROCESSED_CONTENT_DIR, filename)
        dst_file = os.path.join(target_dir, filename)
        
        if os.path.exists(src_file):
            # Read content
            with open(src_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update Image Links
            def replace_link(match):
                alt = match.group(1)
                url = match.group(2)
                
                # Check if it's in our inventory lookup
                if url in image_map:
                     return f"![{alt}](/images/{image_map[url]})"

                # Check stripped URL or other variations if needed?
                # For now, exact match.

                # Fallback: check if it's already a local relative filename?
                if not url.strip().startswith(('http', 'https', '/', 'mailto')):
                     return f"![{alt}](/images/{url})"
                
                return match.group(0)
            
            new_content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_link, content)
            
            # Write to destination
            with open(dst_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            file_count += 1
        else:
            # print(f"Warning: Source file not found: {src_file}") # less noise
            pass

    print(f"Seeding complete. Processed {file_count} markdown files.")

if __name__ == "__main__":
    seed()
