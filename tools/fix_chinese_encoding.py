#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Chinese character encoding in HTML files
Converts gb2312 encoded files to UTF-8
"""

import os
import sys
import glob
from pathlib import Path

def fix_html_encoding(file_path):
    """Fix encoding of a single HTML file"""
    try:
        # Read the file with gb2312 encoding
        with open(file_path, 'r', encoding='gb2312', errors='ignore') as f:
            content = f.read()
        
        # Replace the charset declaration
        content = content.replace('charset=gb2312', 'charset=utf-8')
        content = content.replace('charset=gbk', 'charset=utf-8')
        content = content.replace('charset=gb18030', 'charset=utf-8')
        
        # Write back with UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed: {file_path}")
        return True
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    add_files_dir = project_root / "ADD_files"
    
    if not add_files_dir.exists():
        print(f"ADD_files directory not found at {add_files_dir}")
        return
    
    # Find all HTML files
    html_files = list(add_files_dir.glob("*.html"))
    
    if not html_files:
        print("No HTML files found in ADD_files directory")
        return
    
    print(f"Found {len(html_files)} HTML files to process...")
    
    fixed_count = 0
    for html_file in html_files:
        if fix_html_encoding(html_file):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} out of {len(html_files)} files")

if __name__ == "__main__":
    main() 