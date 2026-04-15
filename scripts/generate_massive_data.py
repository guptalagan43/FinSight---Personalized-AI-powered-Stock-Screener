#!/usr/bin/env python3
"""Generate ~30,000 financial instruments for FinSight."""
import random, os, sys

random.seed(42)

# ── Helpers ──────────────────────────────────────────────────
def gp(lo, hi): return round(random.uniform(lo, hi), 2)
def gchg(p):
    pct = round(random.uniform(-3.0, 3.0), 2)
    return round(p * pct / 100, 2), pct
def g52(p): return round(p * random.uniform(1.05, 1.40), 2), round(p * random.uniform(0.60, 0.95), 2)
def mk(id, sym, name, typ, exch, sec, ind, mcap, price):
    chg, pct = gchg(price)
    h, l = g52(price)
    return {"id":id,"symbol":sym,"name":name,"type":typ,"exchange":exch,"sector":sec,"industry":ind,"market_cap":mcap,"current_price":price,"day_change":chg,"day_change_pct":pct,"high_52w":h,"low_52w":l,"is_active":True}

def fund_row(id, price):
    pe=gp(5,80); pb=gp(0.5,20); roe=gp(2,45); roce=gp(3,50); eps=gp(1,200)
    de=gp(0,2.5); npm=gp(1,30); ph=gp(0,75); sg=gp(-5,35); pg=gp(-10,40)
    rev=gp(500,80000); np=gp(50,15000)
    return (id, pe, pb, roe, roce, eps, de, npm, ph, sg, pg, rev, np)

# ── Read existing data ───────────────────────────────────────
proj = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, proj)
from generated_data import GENERATED_INSTRUMENTS as EXISTING, GENERATED_FUND_DATA as EXISTING_FUND

ALL = list(EXISTING)
ALL_FUND = list(EXISTING_FUND)
existing_ids = {i["id"] for i in ALL}
existing_fund_ids = {f[0] for f in ALL_FUND}
NID = 1000

# ── Indian Sectors ──────────────────────────────────────────
IN_SECTORS = {
    "Information Technology": (["Digi","Info","Tech","Cyber","Cloud","Data","Net","Logic","Code","Soft","AI","Algo","Pixel","Byte","Prime","Nova","Core","Apex","Edge","Zen","Nex","Smart","Rapid","Quick","Hyper"],["Solutions","Systems","Technologies","Services","Labs","Infotech","Software","Computing","Innovations","Digital","Platforms","Networks"]),
    "Banking": (["Metro","Capital","United","Premier","Citizens","Heritage","Growth","Progress","National","Pioneer","Liberty","Frontier","Trust","Coastal","Valley","Summit","Crown","Royal","Elite","Prime","Urban","Rural","Central","Western","Eastern"],["Bank","Financial Bank","Credit Bank","Commercial Bank","Cooperative Bank"]),
    "Pharma": (["Heal","Bio","Medi","Vita","Life","Cure","Care","Zena","Pharma","Neo","Gen","Astra","Novo","Ever","Regen","Alba","Cura","Sana","Tera","Vivo","Flux","Apex","Orion","Pura","Ultra"],["Pharma","Laboratories","Healthcare","Life Sciences","Biotech","Therapeutics","Medical"]),
    "Energy": (["Solar","Green","Wind","Power","Hydro","Thermal","Atomic","Sun","Star","Light","Volt","Amp","Watt","Spark","Flash","Blaze","Ray","Glow","Shine","Bright","Nova","Aura","Flame","Surge","Pulse"],["Energy","Power","Utilities","Resources","Renewables","Electric","Systems"]),
    "FMCG": (["Fresh","Pure","Natural","Golden","Royal","Heritage","Classic","Prime","Choice","Select","Crystal","Pearl","Silver","Ruby","Coral","Jade","Ivory","Amber","Maple","Cedar","Pine","Lotus","Lily","Rose","Orchid"],["Foods","Consumer","Products","Brands","Nutrition","Essentials","Home Care"]),
    "Automobile": (["Speed","Motor","Auto","Drive","Wheel","Gear","Turbo","Nitro","Cruiser","Rider","Swift","Flash","Ace","Victor","King","Tiger","Eagle","Hawk","Lion","Panther","Viper","Cobra","Mustang","Falcon","Thunder"],["Motors","Automotive","Vehicles","Auto Parts","Mobility","Engineering"]),
    "Financial Services": (["Asset","Wealth","Fortune","Capital","Equity","Fund","Invest","Credit","Trust","Shield","Guard","Safe","Secure","Value","Growth","Yield","Alpha","Beta","Delta","Sigma","Omega","Gamma","Theta","Kappa","Lambda"],["Finance","Capital","Services","Advisors","Holdings","Investments","Securities"]),
    "Metals and Mining": (["Iron","Steel","Copper","Zinc","Alloy","Metal","Forge","Cast","Mold","Smelt","Mine","Ore","Rock","Stone","Crystal","Diamond","Ruby","Sapphire","Emerald","Gold","Silver","Platinum","Titanium","Chrome","Nickel"],["Metals","Mining","Steel","Industries","Alloys","Foundry","Resources"]),
    "Real Estate": (["Urban","City","Metro","Town","Home","Estate","Land","Green","Park","Garden","Lake","River","Hill","Valley","Sky","Cloud","Sun","Star","Moon","Crown","Royal","Elite","Grand","Prestige","Heritage"],["Realty","Properties","Developers","Estates","Infrastructure","Builders","Housing"]),
    "Infrastructure": (["Build","Construct","Bridge","Road","Rail","Port","Tower","Plan","Design","Arch","Struct","Frame","Core","Base","Found","Pave","Lay","Erect","Raise","Forge","Shape","Mold","Craft","Make","Form"],["Infrastructure","Construction","Engineering","Projects","Developers","Builders","Works"]),
    "Telecom": (["Tele","Comm","Signal","Wave","Link","Connect","Wire","Fiber","Beam","Pulse","Net","Grid","Hub","Node","Point","Gate","Path","Route","Line","Band","Broad","Air","Sky","Cloud","Digi"],["Telecom","Communications","Networks","Connectivity","Wireless","Broadband","Services"]),
    "Chemicals": (["Chem","Poly","Synth","Organic","React","Catalyst","Formula","Element","Compound","Molecular","Ionic","Carbon","Hydro","Fluoro","Nitro","Sulfo","Phospho","Chloro","Ether","Ester","Acid","Base","Pure","Fine","Special"],["Chemicals","Industries","Polymers","Petrochemicals","Specialties","Compounds","Solutions"]),
    "Consumer Durables": (["Home","Smart","Cool","Bright","Shine","Glow","Comfort","Luxe","Elite","Premium","Classic","Modern","Style","Design","Craft","Art","Fine","Supreme","Ultra","Mega","Super","Max","Pro","Plus","Prime"],["Electronics","Appliances","Durables","Consumer","Home Products","Electricals","Lifestyle"]),
    "Insurance": (["Shield","Guard","Safe","Secure","Trust","Assure","Protect","Cover","Life","Care","Promise","Haven","Anchor","Fortress","Sentinel","Aegis","Bastion","Citadel","Rampart","Bulwark","Harbor","Refuge","Shelter","Beacon","Compass"],["Insurance","Life Insurance","General Insurance","Assurance","Re Insurance"]),
    "Media": (["Star","Sun","Moon","Sky","Cloud","Dream","Vision","Pixel","Frame","Scene","Studio","Stage","Screen","Lens","Focus","Zoom","Flash","Snap","Click","Stream","Play","Show","Cast","Air","Live"],["Media","Entertainment","Broadcasting","Studios","Digital","Content","Productions"]),
    "Textiles": (["Silk","Cotton","Linen","Wool","Weave","Thread","Yarn","Fabric","Cloth","Stitch","Knit","Loom","Spin","Dye","Print","Pattern","Design","Style","Fashion","Trend","Couture","Vogue","Chic","Elegance","Grace"],["Textiles","Fabrics","Industries","Mills","Garments","Fashions","Clothing"]),
    "Cement": (["Rock","Stone","Sand","Lime","Clay","Granite","Marble","Slate","Basalt","Quartz","Concrete","Mortar","Plaster","Gypsum","Ite","Block","Brick","Tile","Slab","Panel","Beam","Column","Pillar","Arch","Wall"],["Cement","Industries","Building Materials","Concrete","Products"]),
    "Agriculture": (["Agri","Farm","Crop","Seed","Harvest","Green","Fertile","Organic","Nature","Earth","Soil","Root","Bloom","Grow","Plant","Field","Ranch","Meadow","Pasture","Orchard","Grove","Garden","Forest","Timber","Wood"],["Agri","Agriculture","Farming","Seeds","Commodities","Products","Foods"]),
    "Hospitality": (["Grand","Royal","Crown","Palace","Heritage","Luxury","Premier","Elite","Classic","Vintage","Platinum","Gold","Silver","Crystal","Pearl","Sapphire","Ruby","Emerald","Diamond","Opal","Topaz","Jade","Ivory","Coral","Amber"],["Hotels","Hospitality","Resorts","Tourism","Leisure","Travel","Entertainment"]),
}

def gen_indian_stocks(start_id, target=4700):
    instruments = []; funds = []; nid = start_id
    sectors = list(IN_SECTORS.keys())
    per_sector = target // len(sectors)
    for sec in sectors:
        prefixes, suffixes = IN_SECTORS[sec]
        count = 0
        for p in prefixes:
            for s in suffixes:
                if count >= per_sector: break
                name = f"{p} {s}"
                sym = (p[:3] + s[:3]).upper()
                sym = sym + str(nid % 100)
                mcap = random.choice([None, gp(100, 500000)])
                price = gp(5, 25000)
                instruments.append(mk(nid, sym, name, "stock", random.choice(["NSE","BSE"]), sec, s, mcap, price))
                funds.append(fund_row(nid, price))
                nid += 1; count += 1
            if count >= per_sector: break
    return instruments, funds, nid

# ── US Stocks ────────────────────────────────────────────────
US_SECTORS = {
    "Technology":(["Apex","Nova","Quantum","Stellar","Vertex","Zenith","Nexus","Pulse","Prism","Helix","Cipher","Vector","Matrix","Photon","Quark","Proton","Neutron","Boson","Plasma","Fusion","Ionic","Tesla","Dynamo","Oracle","Sage"],["Tech","Systems","Computing","Digital","Software","Platforms","AI","Robotics","Semiconductor","Corp"]),
    "Healthcare":(["Vital","Medix","Genex","BioVia","CureGen","HealthPro","MedCore","LifeSpan","WellPath","NeuroGen","CardioTech","OncoMed","ImmunoGen","CellTech","GeneWorks","PharmaCo","BioPharma","MedTech","HealthTech","BioMed","CurePath","VitaGen","PharmaGen","MedLab","BioLab"],["Therapeutics","Pharmaceuticals","Biosciences","Medical","Health","Devices","Diagnostics"]),
    "Finance":(["First","Prime","Global","National","Pacific","Atlantic","Summit","Peak","Crest","Ridge","Harbor","Bay","Coast","Shore","River","Lake","Spring","Valley","Canyon","Mesa","Butte","Plateau","Prairie","Savanna","Tundra"],["Financial","Bancorp","Capital","Group","Holdings","Partners","Advisors","Trust","Securities","Corp"]),
    "Energy":(["Sun","Wind","Wave","Tide","Storm","Thunder","Lightning","Blaze","Inferno","Ember","Flame","Spark","Volt","Amp","Watt","Joule","Tesla","Edison","Faraday","Newton","Kelvin","Curie","Planck","Bohr","Maxwell"],["Energy","Oil","Gas","Petroleum","Resources","Power","Renewables","Solar","Wind Corp"]),
    "Consumer":(["Blue","Red","Green","Gold","Silver","Bronze","Platinum","Diamond","Crystal","Pearl","Ruby","Sapphire","Emerald","Opal","Topaz","Jade","Ivory","Coral","Amber","Onyx","Garnet","Aqua","Turquoise","Citrine","Peridot"],["Brands","Consumer","Retail","Products","Goods","Lifestyle","Home","Foods","Beverages"]),
    "Industrial":(["Iron","Steel","Forge","Anvil","Hammer","Wrench","Bolt","Gear","Piston","Valve","Pump","Crane","Lift","Hoist","Drill","Saw","Lathe","Mill","Press","Roll","Cast","Weld","Rivet","Solder","Braze"],["Industries","Manufacturing","Industrial","Engineering","Machinery","Equipment","Systems"]),
    "Communication":(["Echo","Signal","Pulse","Wave","Beam","Link","Connect","Bridge","Gate","Port","Hub","Node","Mesh","Grid","Cloud","Stream","Flow","Pipe","Channel","Band","Spectrum","Frequency","Resonance","Harmony","Symphony"],["Communications","Media","Networks","Entertainment","Broadcasting","Digital","Streaming"]),
    "Real Estate":(["Urban","Metro","City","Town","Village","Borough","County","State","Union","Federal","National","Colonial","Imperial","Royal","Noble","Grand","Majestic","Regal","Sovereign","Paramount","Supreme","Ultimate","Pinnacle","Apex","Zenith"],["Realty","Properties","REIT","Real Estate","Development","Housing","Trust"]),
    "Materials":(["Carbon","Silicon","Lithium","Cobalt","Nickel","Copper","Zinc","Tin","Lead","Iron","Gold","Silver","Platinum","Palladium","Rhodium","Iridium","Osmium","Ruthenium","Rhenium","Tungsten","Molybdenum","Vanadium","Chromium","Manganese","Titanium"],["Materials","Resources","Mining","Metals","Minerals","Chemicals","Composites"]),
    "Utilities":(["Clear","Pure","Fresh","Clean","Bright","Light","White","Blue","Azure","Aqua","Marine","Ocean","Lake","River","Spring","Brook","Creek","Stream","Falls","Rapids","Cascade","Torrent","Current","Flow","Tide"],["Utilities","Water","Electric","Gas","Power","Services","Infrastructure"]),
}

def gen_us_stocks(start_id, target=8000):
    instruments = []; funds = []; nid = start_id
    sectors = list(US_SECTORS.keys())
    per_sector = target // len(sectors)
    for sec in sectors:
        prefixes, suffixes = US_SECTORS[sec]
        count = 0
        for p in prefixes:
            for s in suffixes:
                if count >= per_sector: break
                name = f"{p} {s}"
                sym = (p[:2] + s[:2]).upper() + str(nid % 1000)
                mcap = gp(500, 3000000)
                price = gp(5, 5000)
                instruments.append(mk(nid, sym, name, "stock", random.choice(["NYSE","NASDAQ"]), sec, s, mcap, price))
                funds.append(fund_row(nid, price))
                nid += 1; count += 1
            if count >= per_sector: break
    return instruments, funds, nid

# ── European Stocks ──────────────────────────────────────────
EU_PREFIXES = ["Nord","Süd","Ost","West","Euro","Pan","Trans","Inter","Multi","Uni","Primo","Alto","Bel","Magna","Viva","Terra","Aqua","Aero","Techno","Pharma","Agri","Bio","Eco","Geo","Solar"]
EU_SUFFIXES = ["AG","SE","NV","SA","SpA","GmbH","PLC","Group","Holdings","Corp","Industries","International","Global","Partners","Ventures"]
EU_SECTORS = ["Technology","Healthcare","Finance","Energy","Consumer","Industrial","Automotive","Luxury","Aerospace","Telecom"]

def gen_eu_stocks(start_id, target=2000):
    instruments = []; funds = []; nid = start_id; count = 0
    for p in EU_PREFIXES:
        for s in EU_SUFFIXES:
            if count >= target: break
            sec = random.choice(EU_SECTORS)
            name = f"{p} {s}"
            sym = (p[:3] + s[:2]).upper() + str(nid % 100)
            mcap = gp(200, 800000)
            price = gp(5, 3000)
            instruments.append(mk(nid, sym, name, "stock", random.choice(["LSE","XETRA","EURONEXT"]), sec, sec, mcap, price))
            funds.append(fund_row(nid, price))
            nid += 1; count += 1
        if count >= target: break
    return instruments, funds, nid

# ── Asian Stocks ─────────────────────────────────────────────
ASIA_PREFIXES = ["Nippon","Tokyo","Osaka","Samsung","Hyundai","LG","SK","Ping","Hua","Zhi","Bao","Jin","Tai","Ming","Feng","Long","Xin","Hai","Shan","Yi","Hong","Guang","Shen","Cheng","Hang"]
ASIA_SUFFIXES = ["Holdings","Corp","Industries","Electric","Chemical","Heavy Industries","Electronics","Motors","Pharma","Financial","Steel","Cement","Shipping","Airlines","Telecom"]
ASIA_SECTORS = ["Technology","Automotive","Electronics","Finance","Energy","Materials","Consumer","Healthcare","Industrial","Telecom"]

def gen_asia_stocks(start_id, target=2000):
    instruments = []; funds = []; nid = start_id; count = 0
    for p in ASIA_PREFIXES:
        for s in ASIA_SUFFIXES:
            if count >= target: break
            sec = random.choice(ASIA_SECTORS)
            name = f"{p} {s}"
            sym = (p[:3] + s[:2]).upper() + str(nid % 100)
            mcap = gp(300, 1200000)
            price = gp(10, 80000)
            instruments.append(mk(nid, sym, name, "stock", random.choice(["TSE","KRX","HKEX","SSE","SZSE"]), sec, sec, mcap, price))
            funds.append(fund_row(nid, price))
            nid += 1; count += 1
        if count >= target: break
    return instruments, funds, nid

# ── ETFs ─────────────────────────────────────────────────────
ETF_AMCS = ["Nippon","SBI","HDFC","ICICI","Kotak","Axis","Motilal","Mirae","ABSL","DSP","UTI","Invesco","Edelweiss","Tata","Franklin","Vanguard","iShares","SPDR","Schwab","ARK","WisdomTree","ProShares","Direxion","First Trust","Global X"]
ETF_STRATEGIES = ["Nifty 50","Nifty Next 50","Sensex","Bank Nifty","Nifty IT","Nifty Pharma","Gold","Silver","S&P 500","NASDAQ 100","Midcap","Smallcap","Dividend","Low Vol","Momentum","Quality","Value","Growth","ESG","Infrastructure","Auto","FMCG","Energy","Metal","PSU Bank","Private Bank","Healthcare","Real Estate","Consumption","Financial","International","Bond","Liquid","Overnight","Gilt","Corporate Bond","Crypto","Blockchain","Clean Energy","Robotics & AI","Semiconductor","Metaverse","Cloud Computing","Cybersecurity","Electric Vehicle","Genomics","Space","AgriTech","FinTech","Gaming","Water","Carbon","Hydrogen","Battery","Lithium","Copper","Uranium","Timber","Commodity","Multi Asset","Dynamic","Balanced","Aggressive","Conservative","Tactical","Strategic"]

def gen_etfs(start_id, target=3000):
    instruments = []; nid = start_id; count = 0
    for amc in ETF_AMCS:
        for strat in ETF_STRATEGIES:
            if count >= target: break
            name = f"{amc} {strat} ETF"
            sym = (amc[:3] + strat.replace(" ","")[:4]).upper() + str(nid % 100)
            price = gp(5, 2000)
            instruments.append(mk(nid, sym, name, "etf", random.choice(["NSE","NYSE","NASDAQ"]), "ETF", strat.split()[0] + " ETF", None, price))
            nid += 1; count += 1
        if count >= target: break
    return instruments, nid

# ── Mutual Funds ─────────────────────────────────────────────
MF_AMCS = ["SBI","HDFC","ICICI Prudential","Kotak","Axis","Motilal Oswal","Mirae Asset","ABSL","DSP","UTI","Invesco India","Edelweiss","Tata","Franklin Templeton","Nippon India","Canara Robeco","Bandhan","WhiteOak","JM","PGIM India","Mahindra Manulife","Quant","Sundaram","HSBC","Baroda BNP","Union","IDFC","Quantum","PPFAS","ITI","360 ONE","Samco","NJ","Bajaj Finserv","LIC"]
MF_CATS = ["Large Cap Fund","Mid Cap Fund","Small Cap Fund","Flexi Cap Fund","Multi Cap Fund","ELSS Tax Saver","Large & Mid Cap","Focused Fund","Value Fund","Contra Fund","Dividend Yield","Balanced Advantage","Equity Hybrid","Aggressive Hybrid","Conservative Hybrid","Arbitrage Fund","Overnight Fund","Liquid Fund","Ultra Short Duration","Low Duration","Short Duration","Medium Duration","Long Duration","Dynamic Bond","Corporate Bond","Credit Risk","Banking & PSU","Gilt Fund","Multi Asset","Children's Fund","Retirement Fund","Index Fund - Nifty 50","Index Fund - Sensex","Index Fund - Nifty Next 50","Index Fund - Nifty Midcap 150","Pharma & Healthcare","Banking & Financial","Technology Fund","Infrastructure Fund","ESG Fund","International Fund","NASDAQ FoF","S&P 500 FoF","European Fund","Emerging Markets","Global Innovation","Thematic Consumption","Nifty 50 Index","Nifty Auto","Nifty Metal"]

def gen_mfs(start_id, target=4000):
    instruments = []; nid = start_id; count = 0
    for amc in MF_AMCS:
        for cat in MF_CATS:
            if count >= target: break
            name = f"{amc} {cat}"
            sym = (amc.split()[0][:3] + cat.replace(" ","")[:5]).upper() + str(nid % 100)
            price = gp(8, 3000)
            ind = cat.split("Fund")[0].strip() if "Fund" in cat else cat.split()[0]
            instruments.append(mk(nid, sym, name, "mf", "NSE", "Mutual Fund", ind, None, price))
            nid += 1; count += 1
        if count >= target: break
    return instruments, nid

# ── Commodities (Spot) ───────────────────────────────────────
COMMODITIES = [
    # Precious Metals
    ("GOLD","Gold Spot","Precious Metals",58000),("SILVER","Silver Spot","Precious Metals",72000),("PLATINUM","Platinum Spot","Precious Metals",28000),("PALLADIUM","Palladium Spot","Precious Metals",35000),("RHODIUM","Rhodium Spot","Precious Metals",145000),
    # Energy
    ("CRUDEOIL","Crude Oil WTI","Energy",6200),("BRENTOIL","Brent Crude","Energy",6500),("NATURALGAS","Natural Gas","Energy",180),("HEATING","Heating Oil","Energy",5800),("GASOLINE","Gasoline RBOB","Energy",5200),("COAL","Coal","Energy",2800),("ETHANOL","Ethanol","Energy",4200),("PROPANE","Propane","Energy",2400),("URANIUM","Uranium Spot","Energy",5800),
    # Base Metals
    ("COPPER","Copper","Base Metals",740),("ALUMINIUM","Aluminium","Base Metals",210),("ZINC","Zinc","Base Metals",260),("NICKEL","Nickel","Base Metals",1450),("LEAD","Lead","Base Metals",188),("TIN","Tin","Base Metals",2350),("COBALT","Cobalt","Base Metals",2280),("LITHIUM","Lithium Carbonate","Base Metals",42000),("MOLYBDENUM","Molybdenum","Base Metals",3800),("MANGANESE","Manganese","Base Metals",1200),("IRON","Iron Ore","Base Metals",8200),("STEEL","Steel HRC","Base Metals",45000),
    # Agriculture
    ("WHEAT","Wheat","Agriculture",2100),("CORN","Corn","Agriculture",1650),("SOYBEAN","Soybean","Agriculture",4200),("RICE","Rice","Agriculture",1800),("COTTON","Cotton","Agriculture",15000),("SUGAR","Sugar","Agriculture",3200),("COFFEE","Coffee Arabica","Agriculture",18500),("COCOA","Cocoa","Agriculture",8200),("PALM","Palm Oil","Agriculture",7800),("RUBBER","Natural Rubber","Agriculture",15500),("PEPPER","Black Pepper","Agriculture",42000),("CARDAMOM","Cardamom","Agriculture",125000),("TURMERIC","Turmeric","Agriculture",8500),("JEERA","Jeera (Cumin)","Agriculture",35000),("CASTOR","Castor Seed","Agriculture",5200),("MUSTARD","Mustard Seed","Agriculture",4800),("MENTHA","Mentha Oil","Agriculture",980),("GUARSEED","Guar Seed","Agriculture",5400),("GUARGUM","Guar Gum","Agriculture",9800),("JUTE","Jute","Agriculture",6500),
    # Livestock
    ("LIVECATTLE","Live Cattle","Livestock",14200),("FEEDERCATTLE","Feeder Cattle","Livestock",16800),("LEANHOGS","Lean Hogs","Livestock",6800),
]

def gen_commodities():
    instruments = []; nid = 50000
    for sym, name, ind, price in COMMODITIES:
        base = gp(price*0.9, price*1.1)
        instruments.append(mk(nid, sym, name, "commodity", "MCX" if ind in ["Precious Metals","Base Metals","Energy"] else "NCDEX", "Commodity", ind, None, base))
        nid += 1
    return instruments, nid

# ── Currencies ───────────────────────────────────────────────
CURRENCIES = [
    ("USDINR","USD/INR",83.25),("EURINR","EUR/INR",90.15),("GBPINR","GBP/INR",105.40),("JPYINR","JPY/INR",0.56),
    ("EURUSD","EUR/USD",1.082),("GBPUSD","GBP/USD",1.266),("USDJPY","USD/JPY",149.5),("USDCHF","USD/CHF",0.882),
    ("AUDUSD","AUD/USD",0.655),("NZDUSD","NZD/USD",0.612),("USDCAD","USD/CAD",1.355),("USDSGD","USD/SGD",1.342),
    ("USDHKD","USD/HKD",7.82),("USDCNY","USD/CNY",7.24),("USDKRW","USD/KRW",1325.0),("USDTWD","USD/TWD",31.5),
    ("USDTHB","USD/THB",35.2),("USDMYR","USD/MYR",4.68),("USDIDR","USD/IDR",15650.0),("USDPHP","USD/PHP",55.8),
    ("USDBRL","USD/BRL",4.95),("USDMXN","USD/MXN",17.1),("USDZAR","USD/ZAR",18.2),("USDTRY","USD/TRY",28.5),
    ("USDRUB","USD/RUB",91.5),("USDPLN","USD/PLN",4.05),("USDCZK","USD/CZK",22.8),("USDHUF","USD/HUF",355.0),
    ("USDSEK","USD/SEK",10.45),("USDNOK","USD/NOK",10.55),("USDDKK","USD/DKK",6.88),("USDILS","USD/ILS",3.65),
    ("USDAED","USD/AED",3.673),("USDSAR","USD/SAR",3.75),("USDQAR","USD/QAR",3.64),("USDKWD","USD/KWD",0.308),
    ("USDBHD","USD/BHD",0.376),("USDOMR","USD/OMR",0.385),("USDJOD","USD/JOD",0.709),("USDEGP","USD/EGP",30.9),
    ("EURGBP","EUR/GBP",0.855),("EURJPY","EUR/JPY",161.8),("EURCHF","EUR/CHF",0.955),("EURAUD","EUR/AUD",1.652),
    ("EURNZD","EUR/NZD",1.768),("EURCAD","EUR/CAD",1.467),("EURSEK","EUR/SEK",11.31),("EURNOK","EUR/NOK",11.42),
    ("GBPJPY","GBP/JPY",189.2),("GBPCHF","GBP/CHF",1.116),("GBPAUD","GBP/AUD",1.932),("GBPCAD","GBP/CAD",1.716),
    ("AUDJPY","AUD/JPY",97.9),("AUDNZD","AUD/NZD",1.071),("AUDCAD","AUD/CAD",0.888),("AUDCHF","AUD/CHF",0.578),
    ("NZDJPY","NZD/JPY",91.5),("NZDCAD","NZD/CAD",0.830),("CADJPY","CAD/JPY",110.3),("CADCHF","CAD/CHF",0.651),
    ("CHFJPY","CHF/JPY",169.5),("SGDJPY","SGD/JPY",111.5),("HKDJPY","HKD/JPY",19.1),("CNYJPY","CNY/JPY",20.6),
    # Crypto pairs
    ("BTCUSD","Bitcoin/USD",42500),("ETHUSD","Ethereum/USD",2280),("XRPUSD","Ripple/USD",0.62),
    ("SOLUSD","Solana/USD",98.5),("ADAUSD","Cardano/USD",0.58),("DOTUSD","Polkadot/USD",7.2),
    ("DOGEUSD","Dogecoin/USD",0.082),("BNBUSD","BNB/USD",305.0),("MATICUSD","Polygon/USD",0.82),
    ("LINKUSD","Chainlink/USD",14.8),("AVAXUSD","Avalanche/USD",35.2),("UNIUSD","Uniswap/USD",6.1),
]

def gen_currencies():
    instruments = []; nid = 55000
    for sym, name, price in CURRENCIES:
        base = gp(price*0.98, price*1.02)
        instruments.append(mk(nid, sym, name, "currency", "FOREX", "Currency", "Forex" if "USD" in sym and "INR" not in sym else ("Crypto" if any(c in sym for c in ["BTC","ETH","XRP","SOL","ADA","DOT","DOGE","BNB","MATIC","LINK","AVAX","UNI"]) else "INR Pairs"), None, base))
        nid += 1
    return instruments, nid

# ── Additional Indices ───────────────────────────────────────
EXTRA_INDICES = [
    ("FTSE100","FTSE 100","LSE",7500),("DAX","DAX 40","XETRA",16200),("CAC40","CAC 40","EURONEXT",7400),
    ("IBEX35","IBEX 35","BME",9800),("FTSEMIB","FTSE MIB","BIT",30500),("AEX","AEX 25","EURONEXT",780),
    ("SMI","Swiss Market Index","SIX",11200),("OMX30","OMX Stockholm 30","OSEAX",2350),
    ("N225","Nikkei 225","TSE",33500),("TOPIX","TOPIX","TSE",2380),("HSI","Hang Seng","HKEX",17200),
    ("SSE","Shanghai Composite","SSE",3050),("SZSE","Shenzhen Composite","SZSE",1920),("KOSPI","KOSPI","KRX",2520),
    ("TAIEX","TAIEX","TWSE",17100),("STI","Straits Times","SGX",3250),("KLCI","KLCI","BURSA",1480),
    ("SET","SET Index","SET",1420),("JCI","Jakarta Composite","IDX",6900),("PSEI","PSEi","PSE",6400),
    ("ASX200","ASX 200","ASX",7250),("NZX50","NZX 50","NZX",11800),("BOVESPA","Bovespa","B3",128000),
    ("IPC","IPC Mexico","BMV",54000),("TSX","S&P/TSX Composite","TSX",20500),("MOEX","MOEX Russia","MOEX",3150),
    ("BIST100","BIST 100","BIST",8200),("TADAWUL","Tadawul","TADAWUL",11500),("DFMGI","DFM General","DFM",4100),
    ("EGX30","EGX 30","EGX",24500),("NSE20","NSE 20 Kenya","NSE_KE",1750),("JSE40","JSE Top 40","JSE",72000),
]

def gen_extra_indices():
    instruments = []; nid = 60000
    for sym, name, exch, price in EXTRA_INDICES:
        base = gp(price*0.95, price*1.05)
        instruments.append(mk(nid, sym, name, "index", exch, "Index", "Broad Market", None, base))
        nid += 1
    return instruments, nid

# ═══════════════════════════════════════════════════════════════
#  MAIN: Generate everything and write to generated_data.py
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating instruments...")

    nid = NID
    # Indian stocks
    in_stocks, in_funds, nid = gen_indian_stocks(nid, 4700)
    print(f"  Indian stocks: {len(in_stocks)}")
    # US stocks
    us_stocks, us_funds, nid = gen_us_stocks(nid, 8000)
    print(f"  US stocks: {len(us_stocks)}")
    # EU stocks
    eu_stocks, eu_funds, nid = gen_eu_stocks(nid, 2000)
    print(f"  EU stocks: {len(eu_stocks)}")
    # Asia stocks
    asia_stocks, asia_funds, nid = gen_asia_stocks(nid, 2000)
    print(f"  Asia stocks: {len(asia_stocks)}")
    # ETFs
    etfs, nid = gen_etfs(nid, 3000)
    print(f"  ETFs: {len(etfs)}")
    # Mutual Funds
    mfs, nid = gen_mfs(nid, 4000)
    print(f"  Mutual Funds: {len(mfs)}")
    # Commodities
    commodities, _ = gen_commodities()
    print(f"  Commodities: {len(commodities)}")
    # Currencies
    currencies, _ = gen_currencies()
    print(f"  Currencies: {len(currencies)}")
    # Extra Indices
    extra_idx, _ = gen_extra_indices()
    print(f"  Extra Indices: {len(extra_idx)}")

    # Merge all
    new_instruments = in_stocks + us_stocks + eu_stocks + asia_stocks + etfs + mfs + commodities + currencies + extra_idx
    new_funds = in_funds + us_funds + eu_funds + asia_funds

    all_instruments = ALL + new_instruments
    all_funds = ALL_FUND + new_funds

    total = len(all_instruments)
    print(f"\nTotal instruments: {total}")
    print(f"Total fund data rows: {len(all_funds)}")

    # Write output
    outpath = os.path.join(proj, "generated_data.py")
    print(f"Writing to {outpath}...")

    with open(outpath, "w", encoding="utf-8") as f:
        f.write(f"# Auto-generated: {total} instruments\n\n")
        f.write("GENERATED_INSTRUMENTS = [\n")
        for inst in all_instruments:
            f.write(f"    {inst},\n")
        f.write("]\n\n")
        f.write("GENERATED_FUND_DATA = [\n")
        for fd in all_funds:
            f.write(f"    {fd},\n")
        f.write("]\n")

    size_mb = os.path.getsize(outpath) / (1024*1024)
    print(f"Done! File size: {size_mb:.1f} MB")
