import os
import glob

html_files = glob.glob('frontend/**/*.html', recursive=True)
count = 0

old_str = '<a href="/pages/top-funds.html">Mutual Funds</a>'
new_str = '''<a href="/pages/top-funds.html">Mutual Funds</a>
                <a href="/pages/commodities.html">Commodities</a>
                <a href="/pages/currencies.html">Currencies</a>'''

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_str in content and '<a href="/pages/commodities.html">Commodities</a>' not in content:
        content = content.replace(old_str, new_str)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f'Updated {count} files.')
