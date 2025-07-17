#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update HTML files to match the modern styling of T18-ZFYEND.html
"""

import os
import sys
import re

# List of files to update
FILES_TO_UPDATE = [
    "T18-1END.html",
    "T18-2END.html", 
    "T18-3END.html",
    "T18-4END.html",
    "T18-5END.html",
    "T18-6END.html",
    "T18-7HUMAN.html",
    "T16-1-4PAN.html",
    "T16-2COW.html",
    "T16-3PIG.html",
    "T16-4TRI.html",
    "H2.htm",
    "YY.html",
    "T10-6COI.html"
]

def update_file_styling(file_path):
    """Update a single file to match T18-ZFYEND.html styling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        title = title_match.group(1) if title_match else "Untitled"
        
        # Extract main content (simplified approach)
        # Find the main content area
        content_match = re.search(r'<div[^>]*align=center[^>]*>(.*?)</div>', content, re.DOTALL | re.IGNORECASE)
        if content_match:
            main_content = content_match.group(1)
        else:
            # Fallback: get everything between body tags
            body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
            main_content = body_match.group(1) if body_match else ""
        
        # Clean up the content
        main_content = re.sub(r'<o:p>.*?</o:p>', '', main_content)
        main_content = re.sub(r'<span[^>]*class="[^"]*"[^>]*>', '', main_content)
        main_content = re.sub(r'</span>', '', main_content)
        main_content = re.sub(r'<p[^>]*class="[^"]*"[^>]*>', '<p>', main_content)
        main_content = re.sub(r'<div[^>]*class="[^"]*"[^>]*>', '<div>', main_content)
        main_content = re.sub(r'<table[^>]*class="[^"]*"[^>]*>', '<table>', main_content)
        main_content = re.sub(r'<td[^>]*style="[^"]*"[^>]*>', '<td>', main_content)
        main_content = re.sub(r'<tr[^>]*style="[^"]*"[^>]*>', '<tr>', main_content)
        main_content = re.sub(r'<b[^>]*style="[^"]*"[^>]*>', '<b>', main_content)
        main_content = re.sub(r'<span[^>]*style="[^"]*"[^>]*>', '', main_content)
        main_content = re.sub(r'<span[^>]*lang="[^"]*"[^>]*>', '', main_content)
        main_content = re.sub(r'<span[^>]*color="[^"]*"[^>]*>', '', main_content)
        main_content = re.sub(r'<span[^>]*mso-[^>]*>', '', main_content)
        main_content = re.sub(r'<o:[^>]*>', '', main_content)
        main_content = re.sub(r'</o:[^>]*>', '', main_content)
        main_content = re.sub(r'<w:[^>]*>', '', main_content)
        main_content = re.sub(r'</w:[^>]*>', '', main_content)
        main_content = re.sub(r'<v:[^>]*>', '', main_content)
        main_content = re.sub(r'</v:[^>]*>', '', main_content)
        main_content = re.sub(r'<mso-[^>]*>', '', main_content)
        main_content = re.sub(r'</mso-[^>]*>', '', main_content)
        main_content = re.sub(r'<![^>]*>', '', main_content)
        main_content = re.sub(r'<!--[^>]*-->', '', main_content)
        main_content = re.sub(r'<xml[^>]*>.*?</xml>', '', main_content, flags=re.DOTALL)
        main_content = re.sub(r'<style[^>]*>.*?</style>', '', main_content, flags=re.DOTALL)
        main_content = re.sub(r'<head[^>]*>.*?</head>', '', main_content, flags=re.DOTALL)
        main_content = re.sub(r'<html[^>]*>', '', main_content)
        main_content = re.sub(r'</html>', '', main_content)
        main_content = re.sub(r'<body[^>]*>', '', main_content)
        main_content = re.sub(r'</body>', '', main_content)
        main_content = re.sub(r'<div[^>]*class="Section1"[^>]*>', '', main_content)
        main_content = re.sub(r'<p[^>]*>&nbsp;</p>', '', main_content)
        main_content = re.sub(r'<p[^>]*><o:p>&nbsp;</o:p></p>', '', main_content)
        
        # Create new modern structure
        new_content = f'''<!DOCTYPE html>
<html lang="zh">
<head>
    <link rel="stylesheet" href="/assets/css/main.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>{title}</title>
</head>
<body>
    <div class="container">
        <header class="article-header">
            <h1 class="article-title">{title}</h1>
            <div class="article-line"></div>
        </header>
        
        <main class="article-content">
            <div class="content-wrapper">
                {main_content}
            </div>
        </main>
    </div>
</body>
</html>'''
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main function to update all files"""
    print("🔄 Updating HTML files to match modern styling...")
    
    success_count = 0
    total_count = len(FILES_TO_UPDATE)
    
    for file_path in FILES_TO_UPDATE:
        if os.path.exists(file_path):
            if update_file_styling(file_path):
                success_count += 1
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print(f"\n📊 Results: {success_count}/{total_count} files updated successfully")
    
    if success_count == total_count:
        print("🎉 All files updated successfully!")
    else:
        print("⚠️  Some files could not be updated. Check the errors above.")

if __name__ == "__main__":
    main() 