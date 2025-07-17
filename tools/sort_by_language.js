const fs = require('fs');
const path = require('path');

const SRC_DIR = path.join(__dirname, '../content/auto-migrated');
const DEST_DIRS = {
  english: path.join(SRC_DIR, 'english'),
  chinese: path.join(SRC_DIR, 'chinese'),
  multilingual: path.join(SRC_DIR, 'multilingual'),
  other: path.join(SRC_DIR, 'other'),
};

// Heuristic: filename or content
function detectLanguage(filename, content) {
  // Filename patterns
  if (/CHT|zh|chinese|WHY|DUTY|Gaogen|變語音|視頻|中文|\u4e00-\u9fff/i.test(filename)) return 'chinese';
  if (/EN|english|western|russian|french|german|italian|japanese|NAMEtoEN|ENGLISH/i.test(filename)) return 'english';
  if (/CH-EN|multilingual|indexChEn|BBCH|CH-ENT|CH-EN-WHY|CH-EN\d/i.test(filename)) return 'multilingual';
  // Content-based (look for Chinese characters)
  if (/[\u4e00-\u9fff]/.test(content)) return 'chinese';
  // Content-based (look for English words)
  if (/(the|and|DNA|science|origin|species|human|book|chapter|guide)/i.test(content)) return 'english';
  return 'other';
}

function ensureDirs() {
  Object.values(DEST_DIRS).forEach(dir => {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  });
}

function sortFiles() {
  ensureDirs();
  const files = fs.readdirSync(SRC_DIR).filter(f => f.endsWith('.html'));
  files.forEach(file => {
    const filePath = path.join(SRC_DIR, file);
    const content = fs.readFileSync(filePath, 'utf8');
    const lang = detectLanguage(file, content);
    const destPath = path.join(DEST_DIRS[lang], file);
    fs.renameSync(filePath, destPath);
    console.log(`Moved: ${file} -> ${lang}/`);
  });
}

sortFiles(); 