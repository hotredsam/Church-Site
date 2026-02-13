import os
import re

# Configuration
# Use the absolute path or relative if running from root
CONTENT_DIR = r"C:\Users\hotre\OneDrive\Desktop\Kaleo Website Bot\kaleo-web\content"

def force_fix_titles():
    print(f"Scanning for markdown files in {CONTENT_DIR}...")
    
    if not os.path.exists(CONTENT_DIR):
        print(f"Error: Content directory {CONTENT_DIR} does not exist.")
        return

    modified_count = 0
    checked_count = 0
    
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                modified = False
                new_lines = []
                checked_count += 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    for line in lines:
                        # Regex to find title line
                        match = re.match(r"^title:\s*(.+)$", line)
                        if match:
                            value = match.group(1).strip()
                            
                            # Check if it contains : or >
                            if (":" in value or ">" in value):
                                # Check if already properly quoted
                                is_double = value.startswith('"') and value.endswith('"')
                                is_single = value.startswith("'") and value.endswith("'")
                                
                                if not (is_double or is_single):
                                    # Fix it: Escape internal double quotes and wrap in double quotes
                                    safe_value = value.replace('"', '\\"')
                                    new_line = f'title: "{safe_value}"\n'
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

    print(f"Checked {checked_count} file(s). Modified {modified_count} file(s).")

if __name__ == "__main__":
    force_fix_titles()
