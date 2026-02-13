import csv
import json
import os
from collections import defaultdict
from urllib.parse import urlparse

# --- Configuration ---
ROOT_DIR = r"C:\Users\hotre\OneDrive\Desktop\Kaleo Website Bot"
MANIFEST_FILE = os.path.join(ROOT_DIR, "content_manifest.csv")
INVENTORY_FILE = os.path.join(ROOT_DIR, "kaleo_inventory.csv")
OUTPUT_SITEMAP_MD = os.path.join(ROOT_DIR, "proposed_sitemap.md")
OUTPUT_MIGRATION_JSON = os.path.join(ROOT_DIR, "migration_map.json")

# Ensure we are in the correct directory
os.chdir(ROOT_DIR)

def load_data():
    manifest_data = []
    inventory_data = {}
    
    # Load Manifest
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            manifest_data = list(reader)

    # Load Inventory for extra metadata (Word Count, etc.)
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                inventory_data[row['Original_URL']] = row

    return manifest_data, inventory_data

def categorize_page(url, title):
    """
    Heuristic categorization based on URL and Title.
    Returns (Category, Subcategory)
    """
    parsed = urlparse(url)
    path = parsed.path.lower()
    
    if path == "/" or path == "/index.html" or path == "":
        return "Home", None
    
    # Sermon handling
    if "/sermons" in path:
        return "Sermons", "Archive"
        
    # Ministries
    ministry_keywords = ["kaleo-kids", "mens-ministry", "kaleo-student-ministry", "small-groups", "k-groups", "women", "reengage"]
    for kw in ministry_keywords:
        if kw in path:
            return "Ministries", title

    # About / New Here
    about_keywords = ["about", "what-we-believe", "staff", "leadership", "our-story", "belief"]
    for kw in about_keywords:
        if kw in path:
            return "About Us", title
            
    # Connect / Visit
    connect_keywords = ["connect", "plan-your-visit", "contact", "location", "times", "membership"]
    for kw in connect_keywords:
        if kw in path:
            return "Connect", title

    # Resources
    resource_keywords = ["resources", "prayer", "reading-plan", "bible"]
    for kw in resource_keywords:
        if kw in path:
            return "Resources", title
            
    # Events
    if "event" in path or "calendar" in path:
        return "Events", title

    # Default
    return "Uncategorized", title

def generate_structure(manifest_data, inventory_data):
    sitemap = defaultdict(lambda: defaultdict(list))
    migration_map = {}
    
    skipped_count = 0
    
    for item in manifest_data:
        original_url = item['Original_URL']
        markdown_path = item['Clean_Markdown_Path']
        
        # Get metadata
        meta = inventory_data.get(original_url, {})
        title = meta.get('Page_Title', 'Untitled')
        word_count = int(meta.get('Word_Count', 0)) if meta.get('Word_Count') else 0
        
        # Heuristic: Merge very short pages (unless they are sermons or vital)
        # We will still list them but mark them for review/merging
        note = ""
        if word_count < 50 and "sermo" not in original_url:
            note = "(Review: Low Content)"

        category, subcategory = categorize_page(original_url, title)
        
        # Store for JSON
        filename = os.path.basename(markdown_path)
        migration_map[filename] = {
            "original_url": original_url,
            "new_section": f"{category}/{subcategory}" if subcategory else category,
            "action": "Keep" if not note else "Merge/Review"
        }
        
        # Store for Markdown Tree
        sitemap[category][subcategory].append(f"{title} {note} [{filename}]")

    return sitemap, migration_map

def write_outputs(sitemap, migration_map):
    # Write Markdown
    with open(OUTPUT_SITEMAP_MD, 'w', encoding='utf-8') as f:
        f.write("# Proposed Website Sitemap\n\n")
        f.write("Generated based on content analysis of `processed_content/`.\n\n")
        
        # Define a preferred order for top-level categories
        order = ["Home", "About Us", "Ministries", "Connect", "Sermons", "Resources", "Events", "Uncategorized"]
        
        for category in order:
            if category in sitemap:
                f.write(f"- **{category}**\n")
                subcats = sitemap[category]
                
                # Handle direct items (None subcategory) first
                if None in subcats:
                    for item in subcats[None]:
                        f.write(f"  - {item}\n")
                    del subcats[None]
                    
                for subcat, items in subcats.items():
                    # If the subcategory name is roughly the same as the item name, just list the item
                    # Otherwise, make a sub-bullet
                    f.write(f"  - {subcat}\n")
                    for item in items:
                        # Don't repeat title if it matches subcat
                        clean_item = item.split(" [")[0].strip()
                        if clean_item != subcat:
                             f.write(f"    - {item}\n")
        
        # Write any remaining categories
        for category in sitemap:
            if category not in order:
                 f.write(f"- **{category}**\n")
                 for subcat, items in sitemap[category].items():
                    f.write(f"  - {subcat}\n")
                    for item in items:
                        f.write(f"    - {item}\n")

    print(f"Sitemap generated: {OUTPUT_SITEMAP_MD}")

    # Write JSON
    with open(OUTPUT_MIGRATION_JSON, 'w', encoding='utf-8') as f:
        json.dump(migration_map, f, indent=2)
    
    print(f"Migration map generated: {OUTPUT_MIGRATION_JSON}")

if __name__ == "__main__":
    manifest, inventory = load_data()
    sitemap, migration_map = generate_structure(manifest, inventory)
    write_outputs(sitemap, migration_map)
