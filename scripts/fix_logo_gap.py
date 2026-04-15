import os
import glob

# Search in frontend pages
html_files = glob.glob(r'd:\WD Lab Project\frontend\pages\*.html')
html_files.append(r'd:\WD Lab Project\frontend\static\js\main.js') # Just in case

replaced_count = 0

for file_path in html_files:
    if not os.path.exists(file_path): continue
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The gap issue happens because `.navbar-brand` uses `display: flex; gap: 10px;`.
    # 'Fin' is a separate text node from '<span class="text-gradient">Sight</span>'.
    # We will wrap "FinSight" entirely in a single <span> so they belong to the same flex child.
    
    new_content = content.replace(
        '<span class="logo-dot"></span> Fin<span class="text-gradient">Sight</span>',
        '<span class="logo-dot"></span> <span class="brand-text">Fin<span class="text-gradient">Sight</span></span>'
    )
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        replaced_count += 1
        print(f"Fixed logo spacing in {os.path.basename(file_path)}")

print(f"\nDone. Updated {replaced_count} files.")
