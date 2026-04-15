"""
Revert SVG insertions in chatbot_service.py back to plain emoji characters.
The backend should emit emojis; the frontend formatChatMarkdown() converts them to SVGs.
"""
import re

filepath = r"d:\Claude Projects\WD Lab Project\backend\services\chatbot_service.py"

# Map each SVG pattern back to its original emoji
# We match both single-quote and double-quote variants of SVG attributes
svg_to_emoji = [
    # Order matters: match longer/more-specific patterns first
    # Warning icon (18x18)
    (r"""<svg\s+width=['"]18['"]\s+height=['"]18['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]1\.5['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>.*?</svg>""", "⚠️"),

    # Trend up (polyline 22 7 ... 16 7 22 7 22 13)
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<polyline\s+points=['"]22 7 13\.5 15\.5 8\.5 10\.5 2 17['"]\s*>\s*</polyline>\s*<polyline\s+points=['"]16 7 22 7 22 13['"]\s*>\s*</polyline>\s*</svg>""", "📈"),

    # Trend down (polyline 22 17 ... 16 17 22 17 22 11)
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<polyline\s+points=['"]22 17 13\.5 8\.5 8\.5 13\.5 2 7['"]\s*>\s*</polyline>\s*<polyline\s+points=['"]16 17 22 17 22 11['"]\s*>\s*</polyline>\s*</svg>""", "📉"),

    # Checkmark
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<polyline\s+points=['"]20 6 9 17 4 12['"]\s*>\s*</polyline>\s*</svg>""", "✅"),

    # Trophy
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<path d=['"]M6 9H4\.5.*?</svg>""", "🏆"),

    # Lightbulb
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<path d=['"]M9 18h6.*?</svg>""", "💡"),

    # Search / magnifying glass
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<circle\s+cx=['"]11['"]\s+cy=['"]11['"]\s+r=['"]8['"]\s*>\s*</circle>.*?</svg>""", "🔍"),

    # Coffee cup / wave (M18 8h1a4...)
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<path d=['"]M18 8h1a4.*?</svg>""", "👋"),

    # Globe
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<circle\s+cx=['"]12['"]\s+cy=['"]12['"]\s+r=['"]10['"]\s*>\s*</circle>\s*<path d=['"]M2 12h20.*?</svg>""", "🌍"),

    # Graduation cap
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<path d=['"]M22 10v6.*?</svg>""", "🎓"),

    # Dollar/money circle (cx=12 cy=12 r=10 + M12 8v8 + M8 12h8)
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<circle\s+cx=['"]12['"]\s+cy=['"]12['"]\s+r=['"]10['"]\s*>\s*</circle>\s*<path d=['"]M12 8v8['"]\s*>\s*</path>\s*<path d=['"]M8 12h8.*?</svg>""", "💰"),

    # Document/receipt (M14 2H6a2...)
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<path d=['"]M14 2H6a2.*?</svg>""", "🧾"),

    # Package/box (line 16.5...)
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<line\s+x1=['"]16\.5.*?</svg>""", "📦"),

    # Ruler/scale (M21.3...)
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<path d=['"]M21\.3.*?</svg>""", "📐"),

    # Money/bill (rect x=2 y=6...)
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<rect\s+x=['"]2.*?</svg>""", "💸"),

    # X-circle / stop
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<circle\s+cx=['"]12['"]\s+cy=['"]12['"]\s+r=['"]10['"]\s*>\s*</circle>\s*<line\s+x1=['"]15['"]\s+y1=['"]9.*?</svg>""", "🛑"),

    # Inbox / mailbox
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<polyline\s+points=['"]22 12 16 12.*?</svg>""", "📭"),

    # Brain
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<path d=['"]M12 2C7\.58.*?</svg>""", "🧠"),

    # Info/alert circle (cx=12 cy=12 r=10 + M12 8v4 + M12 16h.01 -- orange)
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<circle\s+cx=['"]12['"]\s+cy=['"]12['"]\s+r=['"]10['"]\s*>\s*</circle>\s*<path d=['"]M12 8v4.*?</svg>""", "🟠"),

    # Alert circle with lines (cx=12 cy=12 r=10 + line 12,8->12,12 + line 12,16->12.01,16 -- yellow/pin)
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"]\s+fill=['"]none['"]\s+stroke=['"]currentColor['"]\s+stroke-width=['"]2['"]\s+stroke-linecap=['"]round['"]\s+stroke-linejoin=['"]round['"]\s+style=['"]vertical-align:\s*middle;?['"]\s*>\s*<circle\s+cx=['"]12['"]\s+cy=['"]12['"]\s+r=['"]10['"]\s*>\s*</circle>\s*<line\s+x1=['"]12['"]\s+y1=['"]8.*?</svg>""", "📌"),

    # Catch-all: any remaining 16x16 SVG
    (r"""<svg\s+width=['"]16['"]\s+height=['"]16['"]\s+viewBox=['"]0 0 24 24['"].*?</svg>""", "📊"),
]

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

count = 0
for pattern, emoji in svg_to_emoji:
    matches = list(re.finditer(pattern, content, re.DOTALL))
    if matches:
        print(f"  Found {len(matches)} SVG blocks to revert")
        content = re.sub(pattern, emoji, content, flags=re.DOTALL)
        count += len(matches)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nReverted {count} SVG blocks back to emojis in chatbot_service.py")

# Verify it parses
import ast
try:
    ast.parse(content)
    print("OK - Python syntax is VALID")
except SyntaxError as e:
    print(f"FAIL - SyntaxError remains at line {e.lineno}: {e.msg}")
