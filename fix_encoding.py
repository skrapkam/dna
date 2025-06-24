#!/usr/bin/env python3
import sys
import os
import codecs

def detect_and_fix_encoding(filename):
    """Detect and fix encoding issues in HTML files."""
    
    # Read the file as bytes first
    with open(filename, 'rb') as f:
        content_bytes = f.read()
    
    # Try different encodings to see which one works
    encodings_to_try = ['gb18030', 'gbk', 'gb2312', 'utf-8', 'latin1']
    
    for encoding in encodings_to_try:
        try:
            # Try to decode with this encoding
            content = content_bytes.decode(encoding)
            
            # Check if we can find Chinese characters
            if any('\u4e00' <= char <= '\u9fff' for char in content):
                print(f"Found Chinese characters with {encoding} encoding")
                
                # Create backup
                backup_filename = filename + '.backup2'
                os.rename(filename, backup_filename)
                print(f"Created backup: {backup_filename}")
                
                # Write with UTF-8 encoding
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Update the meta tag
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                content = content.replace('charset=gb18030', 'charset=utf-8')
                content = content.replace('charset=gbk', 'charset=utf-8')
                content = content.replace('charset=gb2312', 'charset=utf-8')
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"Successfully converted {filename} using {encoding} as source")
                return True
                
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error with {encoding}: {e}")
            continue
    
    print(f"Could not find proper encoding for {filename}")
    return False

def main():
    files_to_fix = ['WHY1.html', 'WHY.html']
    
    for filename in files_to_fix:
        if os.path.exists(filename):
            print(f"\nFixing {filename}...")
            success = detect_and_fix_encoding(filename)
            if not success:
                print(f"Failed to fix {filename}")
        else:
            print(f"File {filename} not found")

if __name__ == "__main__":
    main() 