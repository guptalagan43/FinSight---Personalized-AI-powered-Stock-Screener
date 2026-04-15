import os
import re

filepath = 'd:/Claude Projects/WD Lab Project/backend/services/chatbot_service.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

def replacer(match):
    return match.group(0).replace('"', "'")

# Replace any double quotes inside <svg> tags with single quotes
new_content = re.sub(r'<svg.*?</svg>', replacer, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Fixed SVG quotes in chatbot_service.py')
