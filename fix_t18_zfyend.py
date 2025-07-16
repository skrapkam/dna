#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def fix_t18_zfyend():
    # Read the current file with gb2312 encoding
    with open('T18-ZFYEND.html', 'r', encoding='gb2312') as f:
        content = f.read()
    
    # Extract the title and body content
    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    title = title_match.group(1) if title_match else "ZFY基因和人类基因"
    
    # Find the body content (everything between <div class=Section1> and </div>)
    body_match = re.search(r'<div class=Section1>(.*?)</div>', content, re.DOTALL)
    body_content = body_match.group(1) if body_match else ""
    
    # Clean up the body content - remove Microsoft Word artifacts
    body_content = re.sub(r'<div align=center>', '', body_content)
    body_content = re.sub(r'</div>', '', body_content)
    body_content = re.sub(r'<p class=MsoNormal>', '<p>', body_content)
    body_content = re.sub(r'<span style=[^>]*>', '', body_content)
    body_content = re.sub(r'</span>', '', body_content)
    body_content = re.sub(r'<o:p></o:p>', '', body_content)
    body_content = re.sub(r'<o:p>', '', body_content)
    body_content = re.sub(r'</o:p>', '', body_content)
    
    # Create modern HTML5 structure
    modern_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', 'SimSun', Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h3 {{
            color: #34495e;
            margin-top: 25px;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        p {{
            margin-bottom: 15px;
            text-align: justify;
            text-indent: 2em;
        }}
        .highlight {{
            background-color: #fff3cd;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        .back-link {{
            display: inline-block;
            margin-top: 30px;
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }}
        .back-link:hover {{
            background-color: #2980b9;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        {body_content}
        <a href="ADD.html" class="back-link">返回主页</a>
    </div>
</body>
</html>'''
    
    # Write the modern HTML
    with open('T18-ZFYEND.html', 'w', encoding='utf-8') as f:
        f.write(modern_html)
    
    print("T18-ZFYEND.html has been updated with modern styling!")

if __name__ == "__main__":
    fix_t18_zfyend() 