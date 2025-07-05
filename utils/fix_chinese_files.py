#!/usr/bin/env python3
"""
Convert files that were originally saved with Chinese encodings to UTF-8.
This addresses the issue where files show garbled characters when interpreted as UTF-8.
"""

import os
import re
import glob
import chardet

def test_encoding_quality(filepath, encoding):
    """Test how well an encoding works for a file."""
    try:
        with open(filepath, 'rb') as f:
            raw_data = f.read()
        
        decoded = raw_data.decode(encoding, errors='ignore')
        
        # Count Chinese characters
        chinese_chars = [char for char in decoded if '\u4e00' <= char <= '\u9fff']
        
        # Check if title looks reasonable
        title_match = re.search(r'<title>(.*?)</title>', decoded, re.IGNORECASE)
        title = title_match.group(1) if title_match else ""
        
        # Score based on number of Chinese chars and title quality
        score = len(chinese_chars)
        if title and any('\u4e00' <= char <= '\u9fff' for char in title):
            score += 100  # Bonus for readable title
        
        return score, len(chinese_chars), title
    except:
        return 0, 0, ""

def find_best_encoding(filepath):
    """Find the best encoding for a file."""
    encodings_to_test = ['gb2312', 'gb18030', 'gbk', 'big5', 'utf-8']
    
    best_encoding = 'utf-8'
    best_score = 0
    best_chinese_count = 0
    
    for encoding in encodings_to_test:
        score, chinese_count, title = test_encoding_quality(filepath, encoding)
        if score > best_score:
            best_score = score
            best_encoding = encoding
            best_chinese_count = chinese_count
    
    return best_encoding, best_score, best_chinese_count

def convert_file_to_utf8(filepath, from_encoding):
    """Convert a file from one encoding to UTF-8."""
    try:
        with open(filepath, 'r', encoding=from_encoding, errors='ignore') as f:
            content = f.read()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error converting {filepath}: {e}")
        return False

def fix_chinese_file(filepath):
    """Fix encoding for a single file."""
    try:
        # Find the best encoding
        best_encoding, score, chinese_count = find_best_encoding(filepath)
        
        # If the best encoding is not UTF-8 and has Chinese characters, convert it
        if best_encoding != 'utf-8' and chinese_count > 10:
            print(f"Converting {filepath} from {best_encoding} to UTF-8 (found {chinese_count} Chinese chars)")
            return convert_file_to_utf8(filepath, best_encoding)
        
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main function to fix Chinese encoding in all HTML files."""
    # Find all HTML files
    html_files = []
    for pattern in ['*.html', '**/*.html']:
        html_files.extend(glob.glob(pattern, recursive=True))
    
    print(f"Found {len(html_files)} HTML files")
    
    converted_count = 0
    for filepath in html_files:
        if fix_chinese_file(filepath):
            converted_count += 1
    
    print(f"\nConverted {converted_count} files from Chinese encodings to UTF-8")

if __name__ == "__main__":
    main() 