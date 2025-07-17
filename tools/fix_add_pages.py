#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Chinese character encoding in all HTML files listed in ADD.html
"""

import os
import sys
import re

# List of files from ADD.html that need to be fixed
FILES_TO_FIX = [
    "T18-ZFYEND.html",
    "T18-7HUMAN.html", 
    "T18-1END.html",
    "T18-2END.html",
    "T18-5END.html",
    "T18-3END.html",
    "T18-4END.html",
    "T18-6END.html",
    "T16-1-4PAN.html",
    "T16-2COW.html",
    "T16-3PIG.html",
    "T16-4TRI.html",
    "H2.htm",
    "YY.html",
    "T10-6COI.html"  # Already fixed, but included for completeness
]

# Chinese character mappings for common garbled text
CHINESE_FIXES = {
    # Title fixes
    "˵ZFYǺ͡һǡ": "人染色体ZFY标记和第一标记",
    "--⨺COIDNAоĲ": "人-黑猩猩-猕猴：COI基因DNA编码序列有巨大的差异",
    
    # Common word fixes
    "": "人",
    "": "黑猩猩", 
    "⨺": "猕猴",
    "": "基因",
    "": "编码",
    "": "样本",
    "Ⱦɫ": "染色体",
    "Ǻ": "标记和",
    "һǡ": "第一标记",
    "": "编码序列",
    "оĲ": "有巨大的差异",
    "": "个人",
    "": "样本的",
    "": "个",
    "мһ": "编码序列极其一致",
    "": "（线粒体基因）",
    "": "样本",
    "": "：",
    "ӻվ鿴": "从基因银行网站查看此",
    "": "编码",
    "": "非常一致",
    "": "完全一致",
    "": "黄牛",
    "": "野牛",
    "": "线粒体",
    "": "四个地方",
    "": "猪的",
    "": "三个品种",
    "": "小麦的",
    "": "人类",
    "": "比较",
    "": "Y染色体",
    "": "差异变化",
    "": "样本",
    "ͻ䡣": "样本发生了突变。",
    "": "男人",
    "": "女人",
    "": "男人和女人的",
    "": "第一标记",
    "": "编码序列",
    "": "完全一致"
}

def fix_chinese_characters(content):
    """Fix garbled Chinese characters in the content"""
    for garbled, correct in CHINESE_FIXES.items():
        content = content.replace(garbled, correct)
    return content

def fix_html_file(file_path):
    """Fix a single HTML file"""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Fix Chinese characters
        fixed_content = fix_chinese_characters(content)
        
        # Ensure proper charset declaration
        if 'charset=utf-8' not in fixed_content:
            fixed_content = fixed_content.replace('charset=gb2312', 'charset=utf-8')
            fixed_content = fixed_content.replace('charset=gbk', 'charset=utf-8')
            fixed_content = fixed_content.replace('charset=gb18030', 'charset=utf-8')
        
        # Write back the fixed content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"Fixed: {file_path}")
        return True
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Main function to fix all files"""
    print("Fixing Chinese character encoding in ADD.html pages...")
    
    fixed_count = 0
    total_count = len(FILES_TO_FIX)
    
    for filename in FILES_TO_FIX:
        if fix_html_file(filename):
            fixed_count += 1
    
    print(f"\nCompleted! Fixed {fixed_count}/{total_count} files.")
    print("All Chinese characters should now display correctly.")

if __name__ == "__main__":
    main() 