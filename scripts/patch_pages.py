import os

files = [
    'top-gainers.html', 'top-losers.html', 'most-traded.html',
    '52-weeks-high.html', '52-weeks-low.html',
    'stocks-feed.html', 'market-calendar.html'
]

for fn in files:
    path = os.path.join('frontend', 'pages', fn)
    if not os.path.exists(path):
        print(f"Skipping {fn}, not found.")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Shift to normal background
    content = content.replace('<body>', '<body class="page">')
    content = content.replace('<body class="">', '<body class="page">')
    
    # 2. Remove animations script initialization
    content = content.replace('<script src="/static/js/animations.js"></script>', '')
    
    script_to_remove = '''<script>
        document.addEventListener('DOMContentLoaded', () => {
            if (typeof initAnimations === 'function') {
                initAnimations();
            }
        });
    </script>'''
    
    # Simple heuristic to wipe out the specific animation init if block fails
    idx = content.find("initAnimations()")
    if idx != -1:
        start_script = content.rfind('<script>', 0, idx)
        end_script = content.find('</script>', idx) + 9
        content = content[:start_script] + content[end_script:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {fn}")
