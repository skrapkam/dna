#!/usr/bin/env python3
"""
Test the specific CHT7-P1.html file to see what encoding it has.
"""

import chardet

def test_specific_file(filepath):
    """Test different encodings on a specific file."""
    try:
        with open(filepath, 'rb') as f:
            raw_data = f.read()
        
        # Test different Chinese encodings
        encodings_to_test = ['gb2312', 'gb18030', 'gbk', 'big5', 'utf-8', 'utf-8-sig']
        
        print(f"Testing encodings for {filepath}:")
        print("=" * 50)
        
        for encoding in encodings_to_test:
            try:
                decoded = raw_data.decode(encoding, errors='ignore')
                # Look for Chinese characters
                chinese_chars = [char for char in decoded if '\u4e00' <= char <= '\u9fff']
                if chinese_chars:
                    print(f"\n{encoding}: Found {len(chinese_chars)} Chinese characters")
                    # Show first few Chinese characters
                    sample = ''.join(chinese_chars[:20])
                    print(f"Sample: {sample}")
                    
                    # Also show the title if it contains Chinese
                    title_match = re.search(r'<title>(.*?)</title>', decoded, re.IGNORECASE)
                    if title_match:
                        title = title_match.group(1)
                        print(f"Title: {title}")
                else:
                    print(f"\n{encoding}: No Chinese characters found")
            except Exception as e:
                print(f"\n{encoding}: Error - {e}")
        
        # Also try chardet
        result = chardet.detect(raw_data)
        print(f"\nChardet detected: {result['encoding']} (confidence: {result['confidence']:.2f})")
        
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    import re
    test_specific_file('CHT7-P1.html') 