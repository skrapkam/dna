#!/usr/bin/env python3
"""
Script to fix broken paths in HTML files after reorganizing the project.
This script updates image paths, CSS paths, and internal links to work with the new directory structure.
"""

import os
import re
import glob
from pathlib import Path

def fix_html_file(file_path, is_chinese=False):
    """Fix paths in an HTML file"""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original_content = content
    
    # Fix image paths - convert to ../assets/images/
    image_patterns = [
        (r'src="([^"]*\.(?:jpg|jpeg|png|gif|bmp))"', r'src="../assets/images/\1"'),
        (r"src='([^']*\.(?:jpg|jpeg|png|gif|bmp))'", r"src='../assets/images/\1'"),
    ]
    
    for pattern, replacement in image_patterns:
        # Don't double-fix paths that already point to assets
        if '../assets/images/' not in content:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Fix CSS paths
    css_patterns = [
        (r'href="([^"]*\.css)"', r'href="../assets/css/\1"'),
        (r"href='([^']*\.css)'", r"href='../assets/css/\1'"),
        (r'href="infant/text\.css"', r'href="../assets/css/layout-styles.css"'),
        (r'href="infant/newtext\.css"', r'href="../assets/css/layout-styles.css"'),
    ]
    
    for pattern, replacement in css_patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Fix language switching links
    if is_chinese:
        # In Chinese files, link to English
        content = re.sub(r'href="indexEN\.html"', r'href="../en/index.html"', content, flags=re.IGNORECASE)
        content = re.sub(r'href="([^"]*EN\.html)"', r'href="../en/\1"', content, flags=re.IGNORECASE)
    else:
        # In English files, link to Chinese
        content = re.sub(r'href="index\.html"', r'href="../zh/index.html"', content, flags=re.IGNORECASE)
        content = re.sub(r'href="([^"/]*\.html)"', lambda m: f'href="{m.group(1)}"' if not m.group(1).startswith('http') and not m.group(1).startswith('../') else m.group(0), content, flags=re.IGNORECASE)
    
    # Remove absolute URLs that point to the same domain
    content = re.sub(r'href="http://www\.bydnacoding\.org/([^"]*)"', r'href="\1"', content, flags=re.IGNORECASE)
    
    # Fix broken links with leading slashes (absolute paths)
    content = re.sub(r'href="/([^"]*\.html)"', r'href="\1"', content, flags=re.IGNORECASE)
    
    # Fix double slashes in asset paths
    content = re.sub(r'src="../assets/images/([^/"]*\.(?:jpg|jpeg|png|gif|bmp))"', r'src="../assets/images/\1"', content, flags=re.IGNORECASE)
    
    # Clean up any double ../assets/images/ paths
    content = re.sub(r'../assets/images/../assets/images/', r'../assets/images/', content)
    content = re.sub(r'../assets/css/../assets/css/', r'../assets/css/', content)
    
    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed paths in {file_path}")
        return True
    else:
        print(f"  - No changes needed in {file_path}")
        return False

def main():
    """Main function to process all HTML files"""
    print("=== Fixing HTML File Paths ===\n")
    
    # Get all HTML files in en/ and zh/ directories
    html_files = []
    
    # English files
    en_files = glob.glob('en/**/*.html', recursive=True)
    for f in en_files:
        html_files.append((f, False))  # False = not Chinese
    
    # Chinese files
    zh_files = glob.glob('zh/**/*.html', recursive=True)
    for f in zh_files:
        html_files.append((f, True))   # True = Chinese
    
    print(f"Found {len(html_files)} HTML files to process\n")
    
    fixed_count = 0
    for file_path, is_chinese in html_files:
        if fix_html_file(file_path, is_chinese):
            fixed_count += 1
    
    print(f"\n=== Summary ===")
    print(f"Total files processed: {len(html_files)}")
    print(f"Files with fixes applied: {fixed_count}")
    print(f"Files already correct: {len(html_files) - fixed_count}")

if __name__ == "__main__":
    main()