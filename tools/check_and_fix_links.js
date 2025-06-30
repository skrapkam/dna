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

function extractLinks(html) {
  const regex = /<a[^>]+href=["']([^"'>]+)["']/gi;
  let match;
  const links = new Set();
  while ((match = regex.exec(html)) !== null) {
    let href = match[1];
    if (!href.startsWith('http') && !href.startsWith('mailto:') && !href.startsWith('#') && !href.startsWith('javascript:')) {
      links.add(href.split('?')[0].split('#')[0]);
    }
  }
  return Array.from(links);
}

function checkAndFixLinks() {
  const htmlFiles = getAllHtmlFiles(SRC_DIR);
  const allFiles = new Set(htmlFiles.map(f => path.basename(f)));
  let brokenLinks = [];
  htmlFiles.forEach(file => {
    let html = fs.readFileSync(file, 'utf8');
    const links = extractLinks(html);
    links.forEach(link => {
      const linkFile = link.split('/').pop();
      if (link.endsWith('.html') && !allFiles.has(linkFile)) {
        brokenLinks.push({ file, link });
        // Optionally, comment out or mark broken links in HTML
        const regex = new RegExp(`<a([^>]+)href=["']${link}["']`, 'g');
        html = html.replace(regex, `<span style="color:red" title="Broken link">`);
      }
    });
    fs.writeFileSync(file, html, 'utf8');
  });
  if (brokenLinks.length > 0) {
    console.log('Broken links found:');
    brokenLinks.forEach(({ file, link }) => {
      console.log(`In ${file}: ${link}`);
    });
  } else {
    console.log('No broken links found.');
  }
}

checkAndFixLinks(); 