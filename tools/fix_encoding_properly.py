#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Properly fix Chinese character encoding in HTML files
Reads files as binary and correctly converts from gb2312 to UTF-8
"""

import os
import sys
import glob
from pathlib import Path

def fix_html_encoding_properly(file_path):
    """Fix encoding of a single HTML file by reading as binary"""
    try:
        # Read the file as binary
        with open(file_path, 'rb') as f:
            content_bytes = f.read()
        
        # Try to decode with different encodings
        encodings_to_try = ['gb2312', 'gbk', 'gb18030', 'utf-8']
        content = None
        detected_encoding = None
        
        for encoding in encodings_to_try:
            try:
                content = content_bytes.decode(encoding)
                detected_encoding = encoding
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"Could not decode {file_path} with any known encoding")
            return False
        
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
    add_files_dir = project_root / "ADD_files"
    
    if not add_files_dir.exists():
        print(f"ADD_files directory not found at {add_files_dir}")
        return
    
    # Find all HTML files in ADD_files
    html_files = list(add_files_dir.glob("*.html"))
    
    if not html_files:
        print("No HTML files found in ADD_files directory")
        return
    
    print(f"Found {len(html_files)} HTML files to process...")
    
    fixed_count = 0
    for html_file in html_files:
        if fix_html_encoding_properly(html_file):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} out of {len(html_files)} files")

if __name__ == "__main__":
    main() 