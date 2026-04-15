"""
Update footer links across all HTML pages.
Replaces href="#" placeholders in the Company footer section with actual page links.
"""
import os
import re

PAGES_DIR = r"d:\WD Lab Project\frontend\pages"

# Map of link text -> actual URL
LINK_MAP = {
    'Help & Support': '/pages/help.html',
    'Help &amp; Support': '/pages/help.html',
    'Trust & Safety': '/pages/trust.html',
    'Trust &amp; Safety': '/pages/trust.html',
    'Community Guidelines': '/pages/guidelines.html',
    'Disclosures': '/pages/disclosures.html',
    'Privacy Policy': '/pages/privacy.html',
}

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    for link_text, url in LINK_MAP.items():
        # Match <a href="#"> with the specific link text
        pattern = r'<a\s+href="#"\s*>' + re.escape(link_text) + r'</a>'
        replacement = f'<a href="{url}">{link_text}</a>'
        content = re.sub(pattern, replacement, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    updated = []
    skipped = []
    
    for root, dirs, files in os.walk(PAGES_DIR):
        for fname in files:
            if fname.endswith('.html'):
                fpath = os.path.join(root, fname)
                if update_file(fpath):
                    updated.append(os.path.relpath(fpath, PAGES_DIR))
                else:
                    skipped.append(os.path.relpath(fpath, PAGES_DIR))
    
    print(f"\n=== Footer Link Update Complete ===")
    print(f"Updated: {len(updated)} files")
    for f in updated:
        print(f"  ✓ {f}")
    print(f"Skipped (no changes needed): {len(skipped)} files")

if __name__ == '__main__':
    main()
