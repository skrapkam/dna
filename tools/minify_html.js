const fs = require('fs');
const path = require('path');

const SRC_DIR = path.join(__dirname, '../content/auto-migrated');

function getAllHtmlFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getAllHtmlFiles(filePath));
    } else if (file.endsWith('.html')) {
      results.push(filePath);
    }
  });
  return results;
}

function minifyHtml(html) {
  return html
    .replace(/\n+/g, ' ') // Remove newlines
    .replace(/\s{2,}/g, ' ') // Collapse whitespace
    .replace(/>\s+</g, '><') // Remove whitespace between tags
    .replace(/<!--.*?-->/g, '') // Remove comments
    .trim();
}

function processAll() {
  const htmlFiles = getAllHtmlFiles(SRC_DIR);
  htmlFiles.forEach(file => {
    let html = fs.readFileSync(file, 'utf8');
    const minified = minifyHtml(html);
    fs.writeFileSync(file, minified, 'utf8');
    console.log(`Minified: ${file}`);
  });
}

processAll(); 