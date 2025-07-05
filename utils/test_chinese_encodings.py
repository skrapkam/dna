#!/usr/bin/env python3
"""
Test different Chinese encodings to find which one produces readable text.
"""

import chardet
import os

def test_encodings(filepath):
    """Test different encodings on a file."""
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
    # Test on a few problematic files
    test_files = ['WHY1.html', 'index.html', 'video1.html']
    
    for file in test_files:
        if os.path.exists(file):
            test_encodings(file)
            print("\n" + "="*80 + "\n") 