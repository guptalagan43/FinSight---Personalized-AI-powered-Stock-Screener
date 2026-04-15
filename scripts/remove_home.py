import os, glob

pages_dir = r"d:\WD Lab Project\frontend\pages"
files = glob.glob(os.path.join(pages_dir, "**", "*.html"), recursive=True)

patterns = [
    '<a href="/" class="nav-link">Home</a>',
    '<a href="/" class="nav-link active">Home</a>',
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    cleaned_lines = []
    changed = False
    
    for line in lines:
        if line.strip() in patterns:
            changed = True
            continue
        cleaned_lines.append(line)
        
    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cleaned_lines))
        print(f"Removed Home link from {os.path.basename(file_path)}")

print("Done")
