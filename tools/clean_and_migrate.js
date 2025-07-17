const fs = require('fs');
const path = require('path');

// Directories to scan for HTML files
const SCAN_DIRS = ['.'];
const OUTPUT_DIR = 'content/auto-migrated';
const BASE_LAYOUT_PATH = path.join(__dirname, '../layouts/base.html');

// Helper: Recursively get all HTML files in a directory
function getHtmlFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    if (stat && stat.isDirectory() && !file.startsWith('.')) {
      results = results.concat(getHtmlFiles(filePath));
    } else if (file.endsWith('.html')) {
      results.push(filePath);
    }
  });
  return results;
}

// Helper: Remove Word/Office XML and deprecated tags
function cleanHtml(content) {
  // Remove Word/Office XML
  content = content.replace(/<\?xml[^>]*>/g, '');
  content = content.replace(/<\!--\[if gte mso [^>]*>[\s\S]*?<\!\[endif\]-->/g, '');
  content = content.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '');
  content = content.replace(/<meta[^>]*ProgId[^>]*>/gi, '');
  content = content.replace(/<meta[^>]*Generator[^>]*>/gi, '');
  content = content.replace(/<meta[^>]*Originator[^>]*>/gi, '');
  content = content.replace(/<link[^>]*File-List[^>]*>/gi, '');
  content = content.replace(/<link[^>]*themeData[^>]*>/gi, '');
  content = content.replace(/<link[^>]*colorSchemeMapping[^>]*>/gi, '');
  // Remove deprecated tags
  content = content.replace(/<font[^>]*>/gi, '');
  content = content.replace(/<\/font>/gi, '');
  content = content.replace(/<marquee[^>]*>[\s\S]*?<\/marquee>/gi, '');
  // Remove inline styles
  content = content.replace(/ style="[^"]*"/gi, '');
  // Remove Word comments
  content = content.replace(/<!--\[if !supportLists\]-->/g, '');
  content = content.replace(/<!--\[endif\]-->/g, '');
  // Remove empty tags
  content = content.replace(/<p>\s*<\/p>/g, '');
  // Remove table-based layout (replace with <section> or <div>)
  content = content.replace(/<table[^>]*>/gi, '<section>');
  content = content.replace(/<\/table>/gi, '</section>');
  content = content.replace(/<tr[^>]*>/gi, '<div>');
  content = content.replace(/<\/tr>/gi, '</div>');
  content = content.replace(/<td[^>]*>/gi, '<div>');
  content = content.replace(/<\/td>/gi, '</div>');
  // Ensure images have alt attributes
  content = content.replace(/<img([^>]*)>/gi, (match, attrs) => {
    if (/alt\s*=/.test(attrs)) return `<img${attrs}>`;
    return `<img alt="Image"${attrs}>`;
  });
  // Remove multiple blank lines
  content = content.replace(/\n{3,}/g, '\n\n');
  return content;
}

// Helper: Wrap content in base layout
function wrapInLayout(content, title = 'DNA Decoding Science Alliance') {
  let layout = fs.readFileSync(BASE_LAYOUT_PATH, 'utf8');
  // Insert title
  layout = layout.replace(/{% block title %}DNA Decoding Science Alliance{% endblock %}/, title);
  // Insert content
  layout = layout.replace(/{% block content %}{% endblock %}/, content);
  return layout;
}

// Main automation
function automateMigration() {
  if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  const htmlFiles = getHtmlFiles('.');
  htmlFiles.forEach(file => {
    if (file.startsWith('assets') || file.startsWith('layouts') || file.startsWith('content') || file.startsWith('node_modules') || file.startsWith('tools')) return;
    const raw = fs.readFileSync(file, 'utf8');
    const cleaned = cleanHtml(raw);
    const titleMatch = raw.match(/<title>(.*?)<\/title>/i);
    const title = titleMatch ? titleMatch[1] : 'DNA Decoding Science Alliance';
    const wrapped = wrapInLayout(cleaned, title);
    const outName = path.basename(file);
    const outPath = path.join(OUTPUT_DIR, outName);
    fs.writeFileSync(outPath, wrapped, 'utf8');
    console.log(`Migrated: ${file} -> ${outPath}`);
  });
}

automateMigration(); 