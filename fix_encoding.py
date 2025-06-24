#!/usr/bin/env python3
"""
Fix character encoding declarations in HTML files.
Changes gb2312 and gb18030 to utf-8 for proper Chinese character display.
"""

import os
import re
import glob

def fix_encoding_in_file(filepath):
    """Fix encoding declaration in a single HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Track if we made changes
        original_content = content
        
        # Fix various encoding declarations
        patterns = [
            # Fix gb2312
            (r'charset=gb2312', 'charset=utf-8'),
            (r'charset=gb18030', 'charset=utf-8'),
            # Fix Content-Type declarations
            (r'<meta http-equiv=Content-Type content="text/html; charset=gb2312">', 
             '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'),
            (r'<meta http-equiv=Content-Type content="text/html; charset=gb18030">', 
             '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'),
            # Fix META declarations
            (r'<META http-equiv=Content-Type content="text/html; charset=gb2312">', 
             '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'),
            (r'<META http-equiv=Content-Type content="text/html; charset=gb18030">', 
             '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        # Add UTF-8 declaration if none exists
        if 'charset=utf-8' not in content.lower() and 'charset' not in content.lower():
            # Find the head tag and add meta charset
            head_match = re.search(r'<head[^>]*>', content, re.IGNORECASE)
            if head_match:
                charset_meta = '<meta charset="utf-8">'
                content = content[:head_match.end()] + '\n\t' + charset_meta + content[head_match.end():]
        
        # Write back if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main function to fix encoding in all HTML files."""
    # Find all HTML files
    html_files = []
    for pattern in ['*.html', '**/*.html']:
        html_files.extend(glob.glob(pattern, recursive=True))
    
    print(f"Found {len(html_files)} HTML files")
    
    fixed_count = 0
    for filepath in html_files:
        if fix_encoding_in_file(filepath):
            print(f"Fixed encoding in: {filepath}")
            fixed_count += 1
    
    print(f"\nFixed encoding in {fixed_count} files")

if __name__ == "__main__":
    main() 