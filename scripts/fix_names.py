import os

REPLACEMENTS = [
    # Fix the brand name HTML
    ('FinSIght<span class="text-gradient">.AI</span>', 'Fin<span class="text-gradient">Sight</span>'),
    ('FinSIght<span class="text-gradient">.ai</span>', 'Fin<span class="text-gradient">Sight</span>'),
    
    # Fix the exact "not FinSight.AI"
    ('FinSIght.AI', 'FinSight'),
    ('FinSIght.ai', 'FinSight'),
    ('FinSight.AI', 'FinSight'),
    ('FinSight.ai', 'FinSight'),

    # Fix bad replacements of "screener"
    ('FinSIghts', 'Screeners'),
    ('FinSights', 'Screeners'),
    ('Custom FinSIght', 'Custom Screener'),
    ('Stock FinSIght', 'Stock Screener'),
    ('Explore FinSIght', 'Explore Screener'),
    ('Predefined FinSIght', 'Predefined Screener'),
    ('finsight_routes', 'screener_routes'),
    ('finsight_bp', 'screener_bp'),

    # Fix the project name spelling
    ('FinSIght', 'FinSight')
]

# Rename the file if it exists
try:
    routes_old = os.path.join("backend", "routes", "finsight_routes.py")
    routes_new = os.path.join("backend", "routes", "screener_routes.py")
    if os.path.exists(routes_old):
        os.rename(routes_old, routes_new)
        print(f"Renamed {routes_old} to {routes_new}")
except Exception as e:
    print(f"Error renaming file: {e}")

search_dirs = ['frontend', 'backend', 'generate_instruments.py']
files_updated = 0

for d in search_dirs:
    if os.path.isfile(d):
        roots = [(os.path.dirname(d), [], [os.path.basename(d)])]
    else:
        roots = os.walk(d)
        
    for root, dirs, files in roots:
        if 'node_modules' in root or '.git' in root or '__pycache__' in root:
            continue
        for f in files:
            if f.endswith(('.html', '.js', '.css', '.py', '.sql', '.md')):
                fpath = os.path.join(root, f)
                try:
                    with open(fpath, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    new_content = content
                    for old_text, new_text in REPLACEMENTS:
                        new_content = new_content.replace(old_text, new_text)
                        
                    if new_content != content:
                        with open(fpath, 'w', encoding='utf-8') as file:
                            file.write(new_content)
                        print(f"Updated {fpath}")
                        files_updated += 1
                except Exception as e:
                    print(f"Error processing {fpath}: {e}")

print(f"Total files updated: {files_updated}")
