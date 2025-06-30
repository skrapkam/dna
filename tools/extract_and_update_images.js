const fs = require('fs');
const path = require('path');

const SRC_DIR = path.join(__dirname, '../content/auto-migrated');
const IMG_DEST = path.join(__dirname, '../assets/images');

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

function extractImagePaths(html) {
  const regex = /<img[^>]+src=["']([^"'>]+)["']/gi;
  let match;
  const paths = new Set();
  while ((match = regex.exec(html)) !== null) {
    let src = match[1];
    if (!src.startsWith('http') && !src.startsWith('data:')) {
      paths.add(src);
    }
  }
  return Array.from(paths);
}

function copyAndUpdateImages(htmlFile, imgPaths) {
  let html = fs.readFileSync(htmlFile, 'utf8');
  imgPaths.forEach(imgPath => {
    // Find the image file relative to the HTML file
    const htmlDir = path.dirname(htmlFile);
    const absImgPath = path.resolve(htmlDir, imgPath);
    if (fs.existsSync(absImgPath)) {
      const imgName = path.basename(imgPath);
      const destPath = path.join(IMG_DEST, imgName);
      if (!fs.existsSync(IMG_DEST)) fs.mkdirSync(IMG_DEST, { recursive: true });
      fs.copyFileSync(absImgPath, destPath);
      // Update HTML to use new path
      const regex = new RegExp(imgPath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
      html = html.replace(regex, `/assets/images/${imgName}`);
      console.log(`Copied: ${imgPath} -> /assets/images/${imgName}`);
    }
  });
  fs.writeFileSync(htmlFile, html, 'utf8');
}

function processAll() {
  const htmlFiles = getAllHtmlFiles(SRC_DIR);
  htmlFiles.forEach(file => {
    const html = fs.readFileSync(file, 'utf8');
    const imgPaths = extractImagePaths(html);
    if (imgPaths.length > 0) {
      copyAndUpdateImages(file, imgPaths);
    }
  });
}

processAll(); 