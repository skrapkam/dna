const fs = require('fs');
const path = require('path');

const SRC_DIR = path.join(__dirname, '../content/auto-migrated');
const SITEMAP_PATH = path.join(__dirname, '../content/auto-migrated/sitemap.xml');
const BASE_URL = 'https://bydnacoding.org';

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

function toUrl(filePath) {
  // Get relative path from SRC_DIR, replace backslashes, and prepend BASE_URL
  let rel = path.relative(SRC_DIR, filePath).replace(/\\/g, '/');
  return `${BASE_URL}/${rel}`;
}

function generateSitemap() {
  const htmlFiles = getAllHtmlFiles(SRC_DIR);
  const urls = htmlFiles.map(toUrl);
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
    urls.map(url => `  <url><loc>${url}</loc></url>`).join('\n') +
    '\n</urlset>';
  fs.writeFileSync(SITEMAP_PATH, xml, 'utf8');
  console.log(`Sitemap generated at ${SITEMAP_PATH}`);
}

generateSitemap(); 