import os
import re

# Configuration
ROOT_DIR = r"C:\Users\hotre\OneDrive\Desktop\Kaleo Website Bot"
CONTENT_DIR = os.path.join(ROOT_DIR, "kaleo-web", "content")

def fix_frontmatter():
    print(f"Scanning for markdown files in {CONTENT_DIR}...")
    
    if not os.path.exists(CONTENT_DIR):
        print(f"Error: Content directory {CONTENT_DIR} does not exist.")
        return

    modified_count = 0
    
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                modified = False
                new_lines = []
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        
                    in_frontmatter = False
                    frontmatter_count = 0
                    
                    for i, line in enumerate(lines):
                        stripped = line.strip()
                        
                        # Check for frontmatter delimiters
                        if stripped == "---":
                            frontmatter_count += 1
                            if frontmatter_count == 1:
                                in_frontmatter = True
                            elif frontmatter_count == 2:
                                in_frontmatter = False
                            new_lines.append(line)
                            continue
                        
                        if in_frontmatter and stripped.startswith("title:"):
                            # Split key and value
                            parts = line.split(":", 1)
                            if len(parts) == 2:
                                key = parts[0]
                                value = parts[1].strip()
                                
                                # Check if needs quoting: contains : or > and not already quoted
                                if (":" in value or ">" in value) and not (value.startswith('"') and value.endswith('"')) and not (value.startswith("'") and value.endswith("'")):
                                    # Escape existing quotes if we use double quotes?
                                    # Simple approach: wrap in double quotes, escape internal double quotes
                                    safe_value = value.replace('"', '\\"')
                                    new_line = f'{key}: "{safe_value}"\n'
                                    new_lines.append(new_line)
                                    modified = True
                                    print(f"Fixed: {file} -> {safe_value}")
                                else:
                                    new_lines.append(line)
                            else:
                                new_lines.append(line)
                        else:
                            new_lines.append(line)
                            
                    if modified:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(new_lines)
                        modified_count += 1
                        
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    print(f"Done. Modified {modified_count} files.")

if __name__ == "__main__":
    fix_frontmatter()
