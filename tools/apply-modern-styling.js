const fs = require('fs');
const path = require('path');

// Function to recursively find all HTML files
function findHtmlFiles(dir, fileList = []) {
    const files = fs.readdirSync(dir);
    
    files.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        
        if (stat.isDirectory()) {
            findHtmlFiles(filePath, fileList);
        } else if (file.endsWith('.html') || file.endsWith('.htm')) {
            fileList.push(filePath);
        }
    });
    
    return fileList;
}

// Function to update HTML file with modern styling
function updateHtmlFile(filePath) {
    try {
        let content = fs.readFileSync(filePath, 'utf8');
        let updated = false;
        
        // Check if file already has modern CSS reference
        if (content.includes('/assets/css/main.css')) {
            console.log(`✓ ${filePath} - Already has modern CSS`);
            return false;
        }
        
        // Remove old CSS references
        content = content.replace(/<link[^>]*href=["'][^"']*\.css["'][^>]*>/gi, '');
        content = content.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '');
        
        // Add viewport meta tag if missing
        if (!content.includes('viewport')) {
            content = content.replace(
                /<head[^>]*>/i,
                '<head>\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
            );
        }
        
        // Add modern CSS reference
        if (!content.includes('/assets/css/main.css')) {
            content = content.replace(
                /<head[^>]*>/i,
                '<head>\n    <link rel="stylesheet" href="/assets/css/main.css">'
            );
        }
        
        // Add modern JavaScript reference if missing
        if (!content.includes('/assets/js/main.js')) {
            content = content.replace(
                /<\/body>/i,
                '    <script src="/assets/js/main.js"></script>\n</body>'
            );
        }
        
        // Ensure proper HTML5 structure
        if (!content.includes('<!DOCTYPE html>')) {
            content = content.replace(/<html[^>]*>/i, '<!DOCTYPE html>\n<html lang="zh">');
        }
        
        // Add responsive wrapper classes to main content
        if (!content.includes('class="container"') && !content.includes('class="main"')) {
            // Find body content and wrap it
            const bodyMatch = content.match(/<body[^>]*>([\s\S]*)<\/body>/i);
            if (bodyMatch) {
                const bodyContent = bodyMatch[1];
                const wrappedContent = `
    <main class="main">
        <div class="container">
            <div class="content-grid">
                <section class="main-content">
                    ${bodyContent}
                </section>
            </div>
        </div>
    </main>`;
                content = content.replace(bodyMatch[0], `<body>${wrappedContent}</body>`);
            }
        }
        
        // Write updated content
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`✓ ${filePath} - Updated with modern styling`);
        return true;
        
    } catch (error) {
        console.error(`✗ Error updating ${filePath}:`, error.message);
        return false;
    }
}

// Main execution
console.log('🚀 Applying modern CSS styling to all subpages...\n');

// Find all HTML files in content directories
const contentDirs = [
    'content/auto-migrated',
    'content/chinese', 
    'content/english',
    'content/multilingual'
];

let allHtmlFiles = [];
contentDirs.forEach(dir => {
    if (fs.existsSync(dir)) {
        const files = findHtmlFiles(dir);
        allHtmlFiles = allHtmlFiles.concat(files);
    }
});

console.log(`Found ${allHtmlFiles.length} HTML files to process\n`);

// Process each file
let updatedCount = 0;
allHtmlFiles.forEach(filePath => {
    if (updateHtmlFile(filePath)) {
        updatedCount++;
    }
});

console.log(`\n✅ Completed! Updated ${updatedCount} files with modern styling.`);
console.log(`📁 Files are now using /assets/css/main.css for responsive design.`); 