#!/usr/bin/env python3
"""
Attempt to recover index.html by reading it as GBK and saving as UTF-8.
"""

def recover_html(input_file, source_encoding):
    output_file = input_file
    try:
        with open(input_file, 'r', encoding=source_encoding, errors='ignore') as f:
            content = f.read()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Recovered {input_file} from {source_encoding} to UTF-8.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    recover_html('index.html', 'gbk') 