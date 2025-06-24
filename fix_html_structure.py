#!/usr/bin/env python3
"""
Fix HTML structure issues that prevent proper encoding recognition.
Addresses malformed HTML structure and ensures proper UTF-8 encoding.
"""

import os
import re
import glob

def fix_html_structure(filepath):
    """Fix HTML structure and encoding issues in a single HTML file."""
    try:
        # Read file with UTF-8 encoding, ignore errors
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Ensure proper DOCTYPE and HTML structure
        if not content.strip().startswith('<!DOCTYPE'):
            # Add DOCTYPE if missing
            if content.strip().startswith('<html'):
                content = '<!DOCTYPE html>\n' + content
            elif '<html' in content:
                # Find html tag and add DOCTYPE before it
                html_pos = content.find('<html')
                content = '<!DOCTYPE html>\n' + content[:html_pos] + content[html_pos:]
        
        # Fix 2: Ensure proper head structure with charset
        if '<head' in content:
            # Check if charset is already properly declared
            if 'charset=utf-8' not in content.lower():
                # Find head tag
                head_match = re.search(r'<head[^>]*>', content, re.IGNORECASE)
                if head_match:
                    # Add charset meta tag right after head opening
                    charset_meta = '\n<meta charset="utf-8">'
                    content = content[:head_match.end()] + charset_meta + content[head_match.end():]
        
        # Fix 3: Remove malformed early closing tags
        # Find if there are early </body></html> tags
        body_close_match = re.search(r'</body>\s*</html>', content, re.IGNORECASE)
        if body_close_match:
            # Check if there's content after the closing tags
            after_close = content[body_close_match.end():].strip()
            if after_close:
                # Remove the early closing tags
                content = content[:body_close_match.start()] + after_close
        
        # Fix 4: Ensure proper closing tags at the end
        if not content.strip().endswith('</html>'):
            # Add missing closing tags
            if '</body>' not in content:
                content += '\n</body>'
            if '</html>' not in content:
                content += '\n</html>'
        
        # Fix 5: Clean up any remaining encoding issues
        patterns = [
            # Fix various encoding declarations
            (r'charset=gb2312', 'charset=utf-8'),
            (r'charset=gb18030', 'charset=utf-8'),
            (r'charset=big5', 'charset=utf-8'),
            # Fix Content-Type declarations
            (r'<meta http-equiv=Content-Type content="text/html; charset=gb2312">', 
             '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'),
            (r'<meta http-equiv=Content-Type content="text/html; charset=gb18030">', 
             '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'),
            (r'<meta http-equiv=Content-Type content="text/html; charset=big5">', 
             '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'),
            # Fix META declarations
            (r'<META http-equiv=Content-Type content="text/html; charset=gb2312">', 
             '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'),
            (r'<META http-equiv=Content-Type content="text/html; charset=gb18030">', 
             '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'),
            (r'<META http-equiv=Content-Type content="text/html; charset=big5">', 
             '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
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
    """Main function to fix HTML structure in all HTML files."""
    # Find all HTML files
    html_files = []
    for pattern in ['*.html', '**/*.html']:
        html_files.extend(glob.glob(pattern, recursive=True))
    
    print(f"Found {len(html_files)} HTML files")
    
    fixed_count = 0
    for filepath in html_files:
        if fix_html_structure(filepath):
            print(f"Fixed structure in: {filepath}")
            fixed_count += 1
    
    print(f"\nFixed structure in {fixed_count} files")

if __name__ == "__main__":
    main() 