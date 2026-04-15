import os
import glob

# Step 1: Extract the footer from about.html and remove "Calculators" from Products
with open('frontend/pages/about.html', 'r', encoding='utf-8') as f:
    html = f.read()
    start = html.find('<footer class="footer">')
    # Use find to capture up to </footer>
    end = html.find('</footer>', start) + len('</footer>')
    footer_html = html[start:end]

# Remove the calculators link from the products column
calc_link = '<a href="/pages/calculators.html">Calculators</a>'
calc_link_with_newlines1 = calc_link + '\n'
calc_link_with_newlines2 = '                ' + calc_link + '\n'

products_start = footer_html.find('<h4>Products</h4>')
products_end = footer_html.find('</div>', products_start)

products_chunk = footer_html[products_start:products_end]
new_products_chunk = products_chunk.replace(calc_link_with_newlines2, '').replace(calc_link_with_newlines1, '').replace(calc_link, '')
footer_html = footer_html[:products_start] + new_products_chunk + footer_html[products_end:]

# Step 2: Apply this footer to ALL html files
html_files = glob.glob('frontend/**/*.html', recursive=True)
count = 0

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    start_tag = '<footer class="footer">'
    end_tag = '</footer>'
    idx1 = content.find(start_tag)
    idx2 = content.find(end_tag)
    
    # If a page doesn't have a <footer> tag, skip or append?
    # Usually it's right before <script src="/static/js/main.js"></script>
    if idx1 != -1 and idx2 != -1:
        new_content = content[:idx1] + footer_html + content[idx2 + len(end_tag):]
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
    elif '<script src="/static/js/main.js">' in content:
        # insert footer before scripts
        idx = content.find('<script src="/static/js/main.js">')
        new_content = content[:idx] + footer_html + '\n    ' + content[idx:]
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f'Updated {count} files with the correct footer.')
