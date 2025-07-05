#!/usr/bin/env python3
"""
Detect and fix file encoding issues by converting files from their original encoding to UTF-8.
This addresses files that were saved with Chinese encodings (gb2312, gb18030, etc.) and need to be converted.
"""

import os
import re
import glob
import chardet

def detect_encoding(filepath):
    """Detect the encoding of a file."""
    try:
        with open(filepath, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding'], result['confidence']
    except Exception as e:
        print(f"Error detecting encoding for {filepath}: {e}")
        return None, 0

def convert_file_encoding(filepath, from_encoding, to_encoding='utf-8'):
    """Convert a file from one encoding to another."""
    try:
        # Read with detected encoding
        with open(filepath, 'r', encoding=from_encoding, errors='ignore') as f:
            content = f.read()
        
        # Write with target encoding
        with open(filepath, 'w', encoding=to_encoding) as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error converting {filepath}: {e}")
        return False

def fix_file_encoding(filepath):
    """Fix encoding for a single file."""
    try:
        # Detect current encoding
        detected_encoding, confidence = detect_encoding(filepath)
        
        if not detected_encoding:
            return False
        
        # If it's already UTF-8 with high confidence, skip
        if detected_encoding.lower() in ['utf-8', 'utf8'] and confidence > 0.8:
            return False
        
        # If it's a Chinese encoding or low confidence, convert to UTF-8
        if (detected_encoding.lower() in ['gb2312', 'gb18030', 'gbk', 'big5', 'gb2312-80'] or 
            confidence < 0.8):
            
            print(f"Converting {filepath} from {detected_encoding} (confidence: {confidence:.2f}) to UTF-8")
            return convert_file_encoding(filepath, detected_encoding, 'utf-8')
        
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
    
    converted_count = 0
    for filepath in html_files:
        if fix_file_encoding(filepath):
            converted_count += 1
    
    print(f"\nConverted encoding for {converted_count} files")

if __name__ == "__main__":
    main() 