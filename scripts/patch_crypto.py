import re

fname = 'generated_data.py'
with open(fname, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any 'industry': 'Forex' with 'industry': 'Crypto' for the specific symbols
crypto_syms = ['BTCUSD', 'ETHUSD', 'XRPUSD', 'SOLUSD', 'ADAUSD', 'DOTUSD', 'DOGEUSD', 'BNBUSD', 'MATICUSD', 'LINKUSD', 'AVAXUSD', 'UNIUSD']

for sym in crypto_syms:
    # Pattern to match the specific symbol's dictionary and replace Forex with Crypto
    # "symbol": "BTCUSD".*?"industry": "Forex"
    pattern = r'(\'symbol\': \'' + sym + r'\'.*?\'industry\': )\'Forex\''
    content = re.sub(pattern, r"\g<1>'Crypto'", content)
    
    pattern2 = r'("symbol": "' + sym + r'".*?"industry": )"Forex"'
    content = re.sub(pattern2, r'\g<1>"Crypto"', content)

with open(fname, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched crypto currencies in generated_data.py")
