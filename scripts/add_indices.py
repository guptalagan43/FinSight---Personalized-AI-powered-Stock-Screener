import os, re

indices = [
    'NIFTY 50', 'SENSEX', 'NIFTY BANK', 'India VIX',
    'NIFTY Midcap 100', 'NIFTY Smallcap 100', 'NIFTY MIDCAP 150', 'NIFTY Pharma',
    'NIFTY 100', 'NIFTY Auto', 'KOSPI Index', 'HANG SENG Index',
    'US Tech 100', 'Dow Jones Futures', 'Dow Jones Index', 'BSE 100',
    'NIFTY Realty', 'NIFTY PSU Bank', 'Gift Nifty', 'FTSE 100 Index',
    'Nikkei Index', 'NIFTY FMCG', 'BSE BANKEX', 'S&P 500',
    'NIFTY NEXT 50', 'NIFTY Metal', 'DAX Index', 'NIFTY Fin Service',
    'CAC Index', 'Nifty Pvt Bank'
]

gen_file = r"d:\WD Lab Project\generated_data.py"
with open(gen_file, "r") as f:
    gen_content = f.read()

max_id = 491
matches = re.findall(r'{"id":\s*(\d+)', gen_content)
if matches:
    max_id = max(int(m) for m in matches)

new_id = max_id + 1
new_instruments_py = []
new_instruments_sql = []

for idx_name in indices:
    symbol = idx_name.replace(" ", "_").upper()
    py_line = f'    {{"id":{new_id},"symbol":"{symbol}","name":"{idx_name}","type":"index","exchange":"NSE","sector":"Index","industry":"Index","market_cap":None,"current_price":20000.0,"day_change":100.0,"day_change_pct":0.5,"high_52w":25000.0,"low_52w":15000.0,"is_active":True}},'
    new_instruments_py.append(py_line)
    
    # Notice: no `id` column because PostgreSQL auto-increments
    sql_line = f"('{symbol}', '{idx_name}', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true)"
    new_instruments_sql.append(sql_line)
    
    new_id += 1

# Append to GENERATED_INSTRUMENTS list
parts = gen_content.split("GENERATED_FUND_DATA")
if len(parts) > 1:
    # First part is GENERATED_INSTRUMENTS with its closing `]` and some newlines and the word `GENERATED_FUND_DATA`
    # We find the last `]` in parts[0]
    last_bracket_idx = parts[0].rfind("]")
    if last_bracket_idx != -1:
        py_add = "\n".join(new_instruments_py) + "\n"
        new_gen_content = parts[0][:last_bracket_idx] + py_add + parts[0][last_bracket_idx:] + "GENERATED_FUND_DATA" + parts[1]
        with open(gen_file, "w") as f:
            f.write(new_gen_content)
        print("Updated generated_data.py")
else:
    print("Failed to find injection point in generated_data.py")

sql_file = r"d:\WD Lab Project\database\seed_data.sql"
with open(sql_file, "r") as f:
    sql_content = f.read()

sql_add_full = "\nINSERT INTO instruments (symbol, name, type, exchange, sector, industry, market_cap, current_price, day_change, day_change_pct, high_52w, low_52w, is_active) VALUES\n" + ",\n".join(new_instruments_sql) + ";\n"
with open(sql_file, "a") as f:
    f.write(sql_add_full)
print("Updated seed_data.sql")
