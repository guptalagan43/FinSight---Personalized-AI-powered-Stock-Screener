const fs = require('fs');
const path = require('path');

function removeThemeToggle(dir) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
            removeThemeToggle(fullPath);
        } else if (fullPath.endsWith('.html')) {
            let content = fs.readFileSync(fullPath, 'utf8');
            const originalLength = content.length;
            // The button tag can be multi-line or single-line
            content = content.replace(/<button[^>]*id="theme-toggle"[^>]*>.*?<\/button>/g, '');
            // Some pages might have a hard-coded data-theme="dark" on the <html> tag, let's remove it if it exists.
            content = content.replace(/data-theme="dark"/g, '');
            
            if (content.length !== originalLength) {
                fs.writeFileSync(fullPath, content, 'utf8');
                console.log(`Updated: ${fullPath}`);
            }
        }
    }
}

removeThemeToggle(path.join(__dirname, 'frontend'));
console.log('Done!');
