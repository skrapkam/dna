#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Chinese character encoding in all HTML files in the project
Converts gb2312/gbk/gb18030 encoded files to UTF-8
"""

import os
import sys
import glob
from pathlib import Path

def fix_html_encoding(file_path):
    """Fix encoding of a single HTML file"""
    try:
        # First, try to detect the current encoding
        encodings_to_try = ['gb2312', 'gbk', 'gb18030', 'utf-8']
        content = None
        detected_encoding = None
        
        for encoding in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                detected_encoding = encoding
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"Could not decode {file_path} with any known encoding")
            return False
        
        # Check if the file already has UTF-8 charset
        if 'charset=utf-8' in content.lower():
            print(f"Already UTF-8: {file_path}")
            return True
        
        # Replace charset declarations
        content = content.replace('charset=gb2312', 'charset=utf-8')
        content = content.replace('charset=gbk', 'charset=utf-8')
        content = content.replace('charset=gb18030', 'charset=utf-8')
        content = content.replace('charset=GB2312', 'charset=utf-8')
        content = content.replace('charset=GBK', 'charset=utf-8')
        content = content.replace('charset=GB18030', 'charset=utf-8')
        
        # Write back with UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed: {file_path} (was {detected_encoding})")
        return True
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Directories to skip
    skip_dirs = {
        'backups_gb18030',
        'backups_gb18030_specific', 
        'backups_gb18030_specific2',
        'content/auto-migrated',
        'deploy',
        '.git'
    }
    
    # Find all HTML files
    html_files = []
    for html_file in project_root.rglob("*.html"):
        # Skip files in backup directories
        if any(skip_dir in str(html_file) for skip_dir in skip_dirs):
            continue
        html_files.append(html_file)
    
    if not html_files:
        print("No HTML files found")
        return
    
    print(f"Found {len(html_files)} HTML files to process...")
    
    fixed_count = 0
    for html_file in html_files:
        if fix_html_encoding(html_file):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} out of {len(html_files)} files")

if __name__ == "__main__":
    main() 