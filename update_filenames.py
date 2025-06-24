#!/usr/bin/env python3
import os
import re
import glob

# Mapping of old Chinese filenames to new ASCII filenames
filename_mappings = {
    '日文E.jpg': 'japaneseE.jpg',
    '末代公主.jpg': 'lastPrincess.jpg',
    '英文B3封面.jpg': 'B3_cover.jpg',
    '英文B2封面.jpg': 'B2_cover.jpg',
    '英文B1封面.jpg': 'B1_cover.jpg',
    '中文E.jpg': 'zhongwenE.jpg',
    '法文E.jpg': 'frenchE.jpg',
    '德文E.jpg': 'germanE.jpg',
    '俄文E.jpg': 'russianE.jpg',
    '意大利文E.jpg': 'italianE.jpg',
    '西班牙文E.jpg': 'westernE.jpg',
    '英文B3封面': 'B3_cover',
    '英文B2封面': 'B2_cover',
    '英文B1封面': 'B1_cover',
    '中文E': 'zhongwenE',
    '法文E': 'frenchE',
    '德文E': 'germanE',
    '俄文E': 'russianE',
    '意大利文E': 'italianE',
    '西班牙文E': 'westernE',
    '日文E': 'japaneseE',
    '末代公主': 'lastPrincess',
    # Additional mappings found in the search
    '8其它空白.jpg': '8_other.jpg',
    '1英文.jpg': '1_english.jpg',
    '2中文.jpg': '2_chinese.jpg',
    '3法文.jpg': '3_french.jpg',
    '4德文.jpg': '4_german.jpg',
    '5俄文.jpg': '5_russian.jpg',
    '6意大利文.jpg': '6_italian.jpg',
    '7西班牙文.jpg': '7_spanish.jpg',
    '8其它空白': '8_other',
    '1英文': '1_english',
    '2中文': '2_chinese',
    '3法文': '3_french',
    '4德文': '4_german',
    '5俄文': '5_russian',
    '6意大利文': '6_italian',
    '7西班牙文': '7_spanish',
    # Video page mapping
    '視頻1b頁.html': 'video1b.html',
    # Corrupted Chinese filenames found in DUTY files
    'ӢB1.jpg': 'B1_cover.jpg',
    'ӢB2.jpg': 'B2_cover.jpg',
    'ӢB3.jpg': 'B3_cover.jpg',
    'ӢB1.jpg': 'B1_cover.jpg',
    'ӢB2.jpg': 'B2_cover.jpg',
    'ӢB3.jpg': 'B3_cover.jpg'
}

def update_file(filepath):
    """Update a single HTML file with the filename mappings."""
    try:
        # Read the file with UTF-8 encoding
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all replacements
        for old_name, new_name in filename_mappings.items():
            # Replace in src attributes
            content = re.sub(r'src=["\']([^"\']*' + re.escape(old_name) + r'[^"\']*)["\']', 
                           r'src="\1'.replace(old_name, new_name) + '"', content)
            
            # Replace in href attributes
            content = re.sub(r'href=["\']([^"\']*' + re.escape(old_name) + r'[^"\']*)["\']', 
                           r'href="\1'.replace(old_name, new_name) + '"', content)
            
            # Replace standalone filenames (for cases where they appear in text)
            content = content.replace(old_name, new_name)
        
        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")
            return True
        else:
            print(f"No changes needed: {filepath}")
            return False
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main function to update all HTML files."""
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Found {len(html_files)} HTML files")
    
    updated_count = 0
    for filepath in html_files:
        if update_file(filepath):
            updated_count += 1
    
    print(f"\nUpdate complete! Updated {updated_count} files out of {len(html_files)} total files.")

if __name__ == "__main__":
    main() 