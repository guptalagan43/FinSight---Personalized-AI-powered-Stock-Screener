import os
import glob
import re

html_files = glob.glob(r'd:\WD Lab Project\frontend\pages\**\*.html', recursive=True)

base_items = """
    <div class="ticker-item up"><span>NIFTY 50</span> 22,514.20 (+0.45%)</div>
    <div class="ticker-item down"><span>SENSEX</span> 73,400.10 (-0.12%)</div>
    <div class="ticker-item up"><span>BANKNIFTY</span> 48,930.55 (+0.80%)</div>
    <div class="ticker-item down"><span>RELIANCE</span> 2,895.10 (-0.35%)</div>
    <div class="ticker-item up"><span>TCS</span> 3,925.00 (+1.20%)</div>
    <div class="ticker-item up"><span>HDFC BANK</span> 1,510.45 (+0.65%)</div>
    <div class="ticker-item down"><span>INFY</span> 1,425.20 (-1.10%)</div>
    <div class="ticker-item up"><span>ITC</span> 435.50 (+0.25%)</div>
"""

# Duplicate 4 times to ensure it fills any screen, making 2 identical halves.
half = base_items * 4
full_content = half + half

ticker_html = f"""<div class="ticker-wrap"><div class="ticker-move">
{full_content}
</div></div>"""

pattern = r'<div class="ticker-wrap">.*?</div>\s*</div>'

for f in html_files:
    if not os.path.isfile(f): continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if '<div class="ticker-wrap">' in content:
        # Replace existing
        new_content = re.sub(pattern, ticker_html, content, flags=re.DOTALL)
    else:
        # Should not happen since we injected to all 28 pages previously, but just in case
        new_content = re.sub(r'(<body[^>]*>)', r'\1\n' + ticker_html, content, count=1)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_content)
    print(f"Patched ticker in {os.path.basename(f)}")

print("Continuous Ticker setup completed.")
