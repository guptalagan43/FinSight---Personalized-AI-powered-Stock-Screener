import re

js_file = r"d:\WD Lab Project\frontend\static\js\main.js"

with open(js_file, 'r', encoding='utf-8') as f:
    js_content = f.read()

new_indices_array = """[
            {name: 'NIFTY 50', id: 492}, {name: 'SENSEX', id: 493}, {name: 'NIFTY BANK', id: 494}, {name: 'India VIX', id: 495},
            {name: 'NIFTY Midcap 100', id: 496}, {name: 'NIFTY Smallcap 100', id: 497}, {name: 'NIFTY MIDCAP 150', id: 498}, {name: 'NIFTY Pharma', id: 499},
            {name: 'NIFTY 100', id: 500}, {name: 'NIFTY Auto', id: 501}, {name: 'KOSPI Index', id: 502}, {name: 'HANG SENG Index', id: 503},
            {name: 'US Tech 100', id: 504}, {name: 'Dow Jones Futures', id: 505}, {name: 'Dow Jones Index', id: 506}, {name: 'BSE 100', id: 507},
            {name: 'NIFTY Realty', id: 508}, {name: 'NIFTY PSU Bank', id: 509}, {name: 'Gift Nifty', id: 510}, {name: 'FTSE 100 Index', id: 511},
            {name: 'Nikkei Index', id: 512}, {name: 'NIFTY FMCG', id: 513}, {name: 'BSE BANKEX', id: 514}, {name: 'S&P 500', id: 515},
            {name: 'NIFTY NEXT 50', id: 516}, {name: 'NIFTY Metal', id: 517}, {name: 'DAX Index', id: 518}, {name: 'NIFTY Fin Service', id: 519},
            {name: 'CAC Index', id: 520}, {name: 'Nifty Pvt Bank', id: 521}
        ]"""

new_etfs_array = """[
            {name: 'Nippon Nifty 50 BeES', id: 314}, {name: 'Nippon Bank BeES', id: 315}, {name: 'Nippon Gold BeES', id: 316}, {name: 'Nippon Silver BeES', id: 317},
            {name: 'Nippon IT BeES', id: 318}, {name: 'Nippon Pharma BeES', id: 319}, {name: 'Nippon Nifty Next 50 BeES', id: 320}, {name: 'Nippon Liquid BeES', id: 321},
            {name: 'CPSE ETF', id: 322}, {name: 'Bharat 22 ETF', id: 323}, {name: 'SBI Nifty 50 ETF', id: 324}, {name: 'SBI Nifty Next 50 ETF', id: 325},
            {name: 'SBI Gold ETF', id: 326}, {name: 'HDFC Nifty 50 ETF', id: 327}, {name: 'HDFC Sensex ETF', id: 328}, {name: 'HDFC Gold ETF', id: 329},
            {name: 'ICICI Nifty 50 ETF', id: 330}, {name: 'ICICI Bank Nifty ETF', id: 331}, {name: 'Kotak Nifty ETF', id: 332}, {name: 'Kotak Gold ETF', id: 333}
        ]"""

# Replace the Indices array
js_content = re.sub(
    r"'Indices': \[\s*.*?\](?:,)?",
    f"'Indices': {new_indices_array},",
    js_content,
    flags=re.DOTALL
)

# Replace the ETFs array
js_content = re.sub(
    r"'ETFs': \[\s*.*?\]",
    f"'ETFs': {new_etfs_array}",
    js_content,
    flags=re.DOTALL
)

# Update getLink, since items might now be objects
new_getLink = """    function getLink(item) {
        if (typeof item === 'object' && item.id) {
            return `/pages/instrument_detail.html?id=${item.id}`;
        }
        if (calcLinks[item]) return calcLinks[item];
        return '/pages/screeners.html';
    }"""
js_content = re.sub(
    r"    function getLink\(name\) \{\s*if \(calcLinks\[name\]\) return calcLinks\[name\];\s*return '/pages/screeners\.html';\s*\}",
    new_getLink,
    js_content,
    flags=re.DOTALL
)

# Also update the loop that builds the <a> tags to use item.name if item is an object
new_loop = """            items.forEach(item => {
                const itemName = typeof item === 'object' ? item.name : item;
                const a = document.createElement('a');
                a.href = getLink(item);
                a.textContent = itemName;
                grid.appendChild(a);
            });"""
js_content = re.sub(
    r"            items\.forEach\(item => \{\s*const a = document\.createElement\('a'\);\s*a\.href = getLink\(item\);\s*a\.textContent = item;\s*grid\.appendChild\(a\);\s*\}\);",
    new_loop,
    js_content,
    flags=re.DOTALL
)

with open(js_file, 'w', encoding='utf-8') as f:
    f.write(js_content)
    
print("Updated main.js with objects and IDs")
