"""
Generator: Creates 1000+ instruments data for FinSight
Outputs: generated_data.py and generated_seed.sql
"""
import random, os
random.seed(42)

# (symbol, name, sector, industry, price, mcap_cr)
# mcap=None for ETFs/MFs
RAW = """TCS|Tata Consultancy Services|Information Technology|IT Services|3845|1380000
INFY|Infosys Ltd|Information Technology|IT Services|1520|620000
WIPRO|Wipro Ltd|Information Technology|IT Services|445|230000
HCLTECH|HCL Technologies|Information Technology|IT Services|1410|380000
TECHM|Tech Mahindra|Information Technology|IT Services|1280|125000
LTIM|LTIMindtree Ltd|Information Technology|IT Services|5200|155000
PERSISTENT|Persistent Systems|Information Technology|IT Services|4850|72000
COFORGE|Coforge Ltd|Information Technology|IT Services|5680|34000
MPHASIS|Mphasis Ltd|Information Technology|IT Services|2450|46000
LTTS|L&T Technology Services|Information Technology|IT Services|4520|47000
TATAELXSI|Tata Elxsi Ltd|Information Technology|IT Services|6850|42000
CYIENT|Cyient Ltd|Information Technology|IT Services|1680|18000
BIRLASOFT|Birlasoft Ltd|Information Technology|IT Services|560|15500
ZENSAR|Zensar Technologies|Information Technology|IT Services|485|11000
SONATA|Sonata Software|Information Technology|IT Services|620|8500
NIIT|NIIT Technologies|Information Technology|IT Services|380|5000
HAPPSTMNDS|Happiest Minds|Information Technology|IT Services|780|11500
KPITTECH|KPIT Technologies|Information Technology|IT Services|1380|37000
TANLA|Tanla Platforms|Information Technology|Cloud Comms|850|11500
MASTEK|Mastek Ltd|Information Technology|IT Services|2580|7800
NEWGEN|Newgen Software|Information Technology|IT Services|920|6500
INTELLECT|Intellect Design Arena|Information Technology|IT Services|680|9200
ROUTE|Route Mobile|Information Technology|Cloud Comms|1650|10500
AFFLE|Affle India|Information Technology|Digital Advertising|1120|15000
LATENTVIEW|Latent View Analytics|Information Technology|Data Analytics|380|7800
ECLERX|eClerx Services|Information Technology|IT Services|2450|12000
QUICKHEAL|Quick Heal Technologies|Information Technology|Cybersecurity|420|2800
DATAPATTR|Data Patterns|Information Technology|Defence Electronics|2100|8000
RATEGAIN|RateGain Travel Tech|Information Technology|Travel Tech|580|6500
ORACLE|Oracle Financial|Information Technology|IT Products|5200|89000
HDFCBANK|HDFC Bank Ltd|Banking|Private Bank|1680|870000
ICICIBANK|ICICI Bank Ltd|Banking|Private Bank|1125|650000
SBIN|State Bank of India|Banking|Public Bank|585|520000
KOTAKBANK|Kotak Mahindra Bank|Banking|Private Bank|1780|354000
AXISBANK|Axis Bank Ltd|Banking|Private Bank|1080|332000
INDUSINDBK|IndusInd Bank|Banking|Private Bank|1420|110000
BANDHANBNK|Bandhan Bank|Banking|Private Bank|225|36000
FEDERALBNK|Federal Bank|Banking|Private Bank|148|31000
IDFCFIRSTB|IDFC First Bank|Banking|Private Bank|72|47000
AUBANK|AU Small Finance Bank|Banking|Small Finance Bank|620|46000
RBLBANK|RBL Bank|Banking|Private Bank|168|10000
CSBBANK|CSB Bank|Banking|Private Bank|290|5000
CITYUNIONBK|City Union Bank|Banking|Private Bank|135|10000
KARURVYSYA|Karur Vysya Bank|Banking|Private Bank|158|12700
TMBLIMITED|Tamilnad Mercantile Bank|Banking|Private Bank|480|7600
BANKBARODA|Bank of Baroda|Banking|Public Bank|245|126000
PNB|Punjab National Bank|Banking|Public Bank|98|108000
CANBK|Canara Bank|Banking|Public Bank|108|98000
UNIONBANK|Union Bank of India|Banking|Public Bank|118|82000
IOB|Indian Overseas Bank|Banking|Public Bank|52|98000
INDIANB|Indian Bank|Banking|Public Bank|480|58000
BANKINDIA|Bank of India|Banking|Public Bank|115|52000
MAHABANK|Bank of Maharashtra|Banking|Public Bank|55|38000
CENTRALBK|Central Bank of India|Banking|Public Bank|54|47000
UCOBANK|UCO Bank|Banking|Public Bank|42|50000
YESBANK|Yes Bank|Banking|Private Bank|22|68000
UJJIVANSFB|Ujjivan SFB|Banking|Small Finance Bank|42|8200
EQUITASBNK|Equitas SFB|Banking|Small Finance Bank|82|9400
IDBI|IDBI Bank|Banking|Public Bank|82|72000
SUNPHARMA|Sun Pharmaceutical|Pharma|Pharmaceuticals|1285|310000
DRREDDY|Dr Reddys Laboratories|Pharma|Pharmaceuticals|6320|105000
CIPLA|Cipla Ltd|Pharma|Pharmaceuticals|1302|105000
DIVISLAB|Divis Laboratories|Pharma|API Manufacturer|3680|97000
LUPIN|Lupin Ltd|Pharma|Pharmaceuticals|1650|75000
AUROPHARMA|Aurobindo Pharma|Pharma|Pharmaceuticals|1080|63000
TORNTPHARM|Torrent Pharmaceuticals|Pharma|Pharmaceuticals|2350|44000
ZYDUSLIFE|Zydus Lifesciences|Pharma|Pharmaceuticals|680|68000
BIOCON|Biocon Ltd|Pharma|Biopharmaceuticals|285|34000
ALKEM|Alkem Laboratories|Pharma|Pharmaceuticals|4950|59000
GLENMARK|Glenmark Pharmaceuticals|Pharma|Pharmaceuticals|1180|33000
IPCALAB|Ipca Laboratories|Pharma|Pharmaceuticals|1320|33000
LAURUSLABS|Laurus Labs|Pharma|API Manufacturer|420|22600
GRANULES|Granules India|Pharma|Pharmaceuticals|380|9200
NATCOPHARM|Natco Pharma|Pharma|Pharmaceuticals|780|14000
ABBOTINDIA|Abbott India|Pharma|MNC Pharma|24500|52000
PFIZER|Pfizer India|Pharma|MNC Pharma|4200|19200
SANOFI|Sanofi India|Pharma|MNC Pharma|6800|15600
GLAXO|GSK Pharma|Pharma|MNC Pharma|1780|30000
AJANTPHARM|Ajanta Pharma|Pharma|Pharmaceuticals|2250|28000
JBCHEPHARM|JB Chemicals|Pharma|Pharmaceuticals|1650|25600
AARTIDRUGS|Aarti Drugs|Pharma|API Manufacturer|480|4400
APOLLOHOSP|Apollo Hospitals|Pharma|Healthcare Services|5800|83000
MAXHEALTH|Max Healthcare|Pharma|Healthcare Services|720|70000
FORTIS|Fortis Healthcare|Pharma|Healthcare Services|380|28500
METROPOLIS|Metropolis Healthcare|Pharma|Diagnostics|1580|8100
DRPATHLABS|Dr Lal PathLabs|Pharma|Diagnostics|2350|19500
MANKIND|Mankind Pharma|Pharma|Pharmaceuticals|1980|79000
ERIS|Eris Lifesciences|Pharma|Pharmaceuticals|880|12000
RELIANCE|Reliance Industries|Energy|Conglomerate|2450|1650000
ONGC|Oil and Natural Gas Corp|Energy|Oil and Gas|245|280000
POWERGRID|Power Grid Corp|Energy|Power Transmission|268|230000
NTPC|NTPC Ltd|Energy|Power Generation|362|350000
BPCL|Bharat Petroleum|Energy|Oil and Gas|348|75000
IOC|Indian Oil Corporation|Energy|Oil and Gas|128|90500
GAIL|GAIL India|Energy|Natural Gas|148|98000
TATAPOWER|Tata Power|Energy|Power Generation|285|91000
ADANIGREEN|Adani Green Energy|Energy|Renewable Energy|1450|230000
ADANIENT|Adani Enterprises|Energy|Conglomerate|2580|295000
HINDPETRO|Hindustan Petroleum|Energy|Oil and Gas|285|42000
PETRONET|Petronet LNG|Energy|Natural Gas|245|36700
COALINDIA|Coal India Ltd|Energy|Coal Mining|385|237000
NHPC|NHPC Ltd|Energy|Hydropower|68|68000
SJVN|SJVN Ltd|Energy|Hydropower|98|38500
IREDA|IREDA|Energy|Green Finance|145|52000
JSWENERGY|JSW Energy|Energy|Power Generation|480|84000
TORNTPOWER|Torrent Power|Energy|Power Distribution|620|29800
CESC|CESC Ltd|Energy|Power Distribution|142|18800
IEX|Indian Energy Exchange|Energy|Power Exchange|148|13200
ADANIPOWER|Adani Power|Energy|Power Generation|480|186000
HINDUNILVR|Hindustan Unilever|FMCG|Personal Care|2420|570000
ITC|ITC Ltd|FMCG|Diversified FMCG|428|530000
NESTLEIND|Nestle India|FMCG|Food Products|22850|220000
BRITANNIA|Britannia Industries|FMCG|Food Products|5080|122000
DABUR|Dabur India|FMCG|Personal Care|535|95000
MARICO|Marico Ltd|FMCG|Personal Care|565|73000
GODREJCP|Godrej Consumer Products|FMCG|Personal Care|1280|130000
COLPAL|Colgate Palmolive India|FMCG|Oral Care|2680|72800
EMAMILTD|Emami Ltd|FMCG|Personal Care|520|22900
TATACONSUM|Tata Consumer Products|FMCG|Food Products|880|85000
JUBLFOOD|Jubilant Foodworks|FMCG|Quick Service Restaurant|520|34400
VBL|Varun Beverages|FMCG|Beverages|1380|180000
PGHH|P and G Hygiene|FMCG|Personal Care|14200|46000
MCDOWELL|United Spirits|FMCG|Alcoholic Beverages|1180|85800
UBL|United Breweries|FMCG|Alcoholic Beverages|1680|44300
RADICO|Radico Khaitan|FMCG|Alcoholic Beverages|1520|20300
BIKAJI|Bikaji Foods|FMCG|Snack Foods|680|16800
GODFRYPHLP|Godfrey Phillips India|FMCG|Tobacco|3200|16600
JYOTHYLAB|Jyothy Labs|FMCG|Personal Care|380|14000
ZYDUSWELL|Zydus Wellness|FMCG|Health Food|1680|10700
MARUTI|Maruti Suzuki|Automobile|Passenger Vehicles|10850|327000
TATAMOTORS|Tata Motors|Automobile|Commercial Vehicles|680|250000
MAHINDRA|Mahindra and Mahindra|Automobile|SUVs and Tractors|1580|196000
BAJAJ_AUTO|Bajaj Auto|Automobile|Two Wheelers|5280|148000
HEROMOTOCO|Hero MotoCorp|Automobile|Two Wheelers|3850|77000
EICHERMOT|Eicher Motors|Automobile|Two Wheelers|3680|101000
TVSMOTOR|TVS Motor Company|Automobile|Two Wheelers|1780|84500
ASHOKLEY|Ashok Leyland|Automobile|Commercial Vehicles|168|49300
BALKRISIND|Balkrishna Industries|Automobile|Tyres|2480|47900
BHARATFORG|Bharat Forge|Automobile|Auto Components|1180|55000
MOTHERSON|Motherson Sumi|Automobile|Auto Components|108|75000
BOSCHLTD|Bosch Ltd|Automobile|Auto Components|18500|54600
EXIDEIND|Exide Industries|Automobile|Batteries|280|23800
AMARAJABAT|Amara Raja Energy|Automobile|Batteries|620|10600
TIINDIA|Tube Investments|Automobile|Auto Components|3580|68800
SUNDRMFAST|Sundram Fasteners|Automobile|Auto Components|1020|21500
MRF|MRF Ltd|Automobile|Tyres|105000|44500
APOLLOTYRE|Apollo Tyres|Automobile|Tyres|420|26700
CEATLTD|CEAT Ltd|Automobile|Tyres|2450|9900
ESCORTS|Escorts Kubota|Automobile|Tractors|2850|32700
FORCEMOT|Force Motors|Automobile|Commercial Vehicles|5800|7700
OLECTRA|Olectra Greentech|Automobile|Electric Buses|1380|11300
SWARAJENG|Swaraj Engines|Automobile|Engines|2180|2700
SAMVARDHNA|Samvardhana Motherson|Automobile|Auto Components|125|85000
BAJFINANCE|Bajaj Finance|Financial Services|NBFC|6580|407000
BAJAJFINSV|Bajaj Finserv|Financial Services|Financial Holding|1580|252000
SBILIFE|SBI Life Insurance|Financial Services|Life Insurance|1380|138000
HDFCLIFE|HDFC Life Insurance|Financial Services|Life Insurance|620|133000
ICICIPRULI|ICICI Prudential Life|Financial Services|Life Insurance|580|83400
MUTHOOTFIN|Muthoot Finance|Financial Services|Gold Finance|1580|63400
MANAPPURAM|Manappuram Finance|Financial Services|Gold Finance|168|14200
CHOLAFIN|Cholamandalam Finance|Financial Services|Vehicle Finance|1180|98000
SHRIRAMFIN|Shriram Finance|Financial Services|Vehicle Finance|2280|85700
MMFIN|M and M Financial|Financial Services|Vehicle Finance|268|33100
POONAWALLA|Poonawalla Fincorp|Financial Services|NBFC|380|29200
LICHSGFIN|LIC Housing Finance|Financial Services|Housing Finance|420|23100
CANFINHOME|Can Fin Homes|Financial Services|Housing Finance|720|9600
PFC|Power Finance Corp|Financial Services|Infra Finance|380|126000
RECLTD|REC Ltd|Financial Services|Infra Finance|428|113000
IRFC|IRFC|Financial Services|Infra Finance|128|167000
ICICIGI|ICICI Lombard|Financial Services|General Insurance|1480|72700
SBICARD|SBI Cards|Financial Services|Credit Cards|720|68000
HDFCAMC|HDFC AMC|Financial Services|Asset Management|3280|70000
NAUKRI|Info Edge Naukri|Financial Services|Internet Platform|5480|70500
CAMS|CAMS Ltd|Financial Services|Registrar|2880|14000
ANGELONE|Angel One|Financial Services|Stockbroking|2280|19000
CDSL|CDSL|Financial Services|Depository|1780|37200
SUNDLIFE|SUN TV Network|Financial Services|Insurance|580|22900
TATASTEEL|Tata Steel|Metals and Mining|Steel|128|157000
JSWSTEEL|JSW Steel|Metals and Mining|Steel|780|189000
HINDALCO|Hindalco Industries|Metals and Mining|Aluminium|520|116000
VEDL|Vedanta Ltd|Metals and Mining|Diversified Metals|285|106000
NMDC|NMDC Ltd|Metals and Mining|Iron Ore|168|49200
SAIL|Steel Authority of India|Metals and Mining|Steel|108|44600
NATIONALUM|National Aluminium|Metals and Mining|Aluminium|118|21700
HINDUCOPPER|Hindustan Copper|Metals and Mining|Copper|168|16200
MOIL|MOIL Ltd|Metals and Mining|Manganese Ore|280|5600
HINDZINC|Hindustan Zinc|Metals and Mining|Zinc|320|135000
APLAPOLLO|APL Apollo Tubes|Metals and Mining|Steel Tubes|1380|34300
RATNAMANI|Ratnamani Metals|Metals and Mining|Steel Tubes|2850|8200
JINDALSTEEL|Jindal Steel and Power|Metals and Mining|Steel|680|69400
WELCORP|Welspun Corp|Metals and Mining|Steel Pipes|480|13100
MISHRA|Mishra Dhatu Nigam|Metals and Mining|Special Steel|280|5200
KIRLFER|Kirloskar Ferrous|Metals and Mining|Pig Iron|420|5800
DLF|DLF Ltd|Real Estate|Residential|580|143000
GODREJPROP|Godrej Properties|Real Estate|Residential|2180|60600
OBEROIRLTY|Oberoi Realty|Real Estate|Residential|1380|50200
PHOENIXLTD|Phoenix Mills|Real Estate|Commercial Property|2850|50500
PRESTIGE|Prestige Estates|Real Estate|Diversified RE|1280|53400
BRIGADE|Brigade Enterprises|Real Estate|Diversified RE|1080|25000
SOBHA|Sobha Ltd|Real Estate|Residential|1450|14500
LODHA|Macrotech Developers|Real Estate|Residential|1180|113000
SUNTECK|Sunteck Realty|Real Estate|Residential|420|5900
RAYMOND|Raymond Ltd|Real Estate|Diversified|1680|11200
MAHLIFE|Mahindra Lifespace|Real Estate|Residential|480|7400
SIGNATURE|Signature Global|Real Estate|Affordable Housing|1120|16800
LT|Larsen and Toubro|Infrastructure|Engineering|3450|474000
ADANIPORTS|Adani Ports and SEZ|Infrastructure|Ports|1180|255000
ULTRACEMCO|UltraTech Cement|Infrastructure|Cement|9850|284000
AMBUJACEM|Ambuja Cements|Infrastructure|Cement|580|141000
ACC|ACC Ltd|Infrastructure|Cement|2280|42800
SHREECEM|Shree Cement|Infrastructure|Cement|25800|93000
DALMIACEM|Dalmia Bharat|Infrastructure|Cement|1780|33400
JKCEMENT|JK Cement|Infrastructure|Cement|3480|26800
RAMCOCEM|Ramco Cements|Infrastructure|Cement|820|19400
IRBINFRA|IRB Infrastructure|Infrastructure|Roads|42|25000
KNR|KNR Constructions|Infrastructure|Roads|280|7900
NCC|NCC Ltd|Infrastructure|Construction|218|13600
NBCC|NBCC India|Infrastructure|Construction|98|17600
PEL|Piramal Enterprises|Infrastructure|Diversified|920|21900
ENGINERSIN|Engineers India|Infrastructure|Engineering|168|9400
RVNL|RVNL|Infrastructure|Railway|178|37200
IRCON|Ircon International|Infrastructure|Infrastructure|178|16700
RITES|RITES Ltd|Infrastructure|Railway|520|12500
BEL|Bharat Electronics|Infrastructure|Defence Electronics|218|159000
BHARTIARTL|Bharti Airtel|Telecom|Telecom Services|1280|720000
IDEA|Vodafone Idea|Telecom|Telecom Services|12|81500
TATACOMM|Tata Communications|Telecom|Enterprise Telecom|1780|50800
INDUSTOWER|Indus Towers|Telecom|Telecom Infra|285|76700
STLTECH|Sterlite Technologies|Telecom|Fibre Optic|148|5800
HFCL|HFCL Ltd|Telecom|Telecom Equipment|82|11800
TEJAS|Tejas Networks|Telecom|Telecom Equipment|850|14500
ZEEL|Zee Entertainment|Media|Broadcasting|148|14200
PVRINOX|PVR INOX|Media|Multiplex|1480|14500
SUNTV|Sun TV Network|Media|Broadcasting|580|22900
SAREGAMA|Saregama India|Media|Music|420|8100
TIPS|Tips Industries|Media|Music|480|3100
NAZARA|Nazara Technologies|Media|Gaming|780|5300
NETWORK18|Network18 Media|Media|Media|68|7200
PIDILITE|Pidilite Industries|Chemicals|Specialty Chemicals|2680|136000
ASIANPAINT|Asian Paints|Chemicals|Paints|2880|276000
BERGEPAINT|Berger Paints|Chemicals|Paints|520|50800
UPL|UPL Ltd|Chemicals|Agrochemicals|480|36100
SRF|SRF Ltd|Chemicals|Specialty Chemicals|2280|67600
AARTIIND|Aarti Industries|Chemicals|Specialty Chemicals|580|21000
DEEPAKNTR|Deepak Nitrite|Chemicals|Specialty Chemicals|2080|28400
CLEAN|Clean Science|Chemicals|Specialty Chemicals|1280|13600
FLUOROCHEM|Gujarat Fluorochem|Chemicals|Fluorochemicals|2880|31700
ALKYLAMINE|Alkyl Amines|Chemicals|Specialty Chemicals|2180|11000
GALAXYSURF|Galaxy Surfactants|Chemicals|Surfactants|2680|9500
FINEORG|Fine Organic Industries|Chemicals|Oleochemicals|4580|14100
PIIND|PI Industries|Chemicals|Agrochemicals|3480|52700
SUMICHEM|Sumitomo Chemical India|Chemicals|Agrochemicals|380|19000
NAVINFLUO|Navin Fluorine|Chemicals|Fluorochemicals|3280|16200
ANURAS|Anupam Rasayan|Chemicals|Specialty Chemicals|680|7300
TATACHEM|Tata Chemicals|Chemicals|Commodity Chemicals|1080|27500
GNFC|GNFC|Chemicals|Commodity Chemicals|580|9000
GSFC|GSFC|Chemicals|Fertilizers|168|6700
CHAMBALFERT|Chambal Fertilisers|Chemicals|Fertilizers|320|13300
COROMANDEL|Coromandel International|Chemicals|Fertilizers|1180|34600
TITAN|Titan Company|Consumer Durables|Jewellery|3280|291000
HAVELLS|Havells India|Consumer Durables|Electricals|1380|86400
VOLTAS|Voltas Ltd|Consumer Durables|AC and Cooling|1080|35700
BLUESTARLT|Blue Star Ltd|Consumer Durables|AC and Cooling|1180|27200
CROMPTON|Crompton Greaves|Consumer Durables|Electricals|320|20400
DIXON|Dixon Technologies|Consumer Durables|Electronics Mfg|5480|32700
KAYNES|Kaynes Technology|Consumer Durables|Electronics Mfg|3280|19600
AMBER|Amber Enterprises|Consumer Durables|AC Components|3880|13100
WHIRLPOOL|Whirlpool India|Consumer Durables|Home Appliances|1280|16200
VGUARD|V-Guard Industries|Consumer Durables|Electricals|380|16400
ORIENTELEC|Orient Electric|Consumer Durables|Fans|280|5900
BATAINDIA|Bata India|Consumer Durables|Footwear|1480|19000
RELAXO|Relaxo Footwears|Consumer Durables|Footwear|880|21900
POLYCAB|Polycab India|Consumer Durables|Cables|5280|79100
KEIRES|KEI Industries|Consumer Durables|Cables|3480|31400
LICI|LIC of India|Insurance|Life Insurance|880|556000
SBILIFE2|SBI Life Insurance|Insurance|Life Insurance|1380|138000
HDFCLIFE2|HDFC Life Insurance|Insurance|Life Insurance|620|133000
STARHEALTH|Star Health Insurance|Insurance|Health Insurance|580|33600
NIACL|New India Assurance|Insurance|General Insurance|168|27600
GICRE|GIC Re|Insurance|Reinsurance|320|56000
PAGEIND|Page Industries|Diversified|Innerwear|38500|43000
TRENT|Trent Ltd|Diversified|Retail|3280|116000
DMART|Avenue Supermarts|Diversified|Retail|3880|252000
ZOMATO|Zomato Ltd|Diversified|Food Delivery|148|128000
NYKAA|FSN E-Commerce Nykaa|Diversified|E-Commerce|168|48000
PAYTM|One97 Communications|Diversified|Fintech|580|36800
POLICYBZR|PB Fintech PolicyBazaar|Diversified|Insurtech|1120|50400
IRCTC|IRCTC|Diversified|Travel|780|62400
INDIGO|InterGlobe Aviation|Diversified|Airlines|3280|126500
HAL|Hindustan Aeronautics|Diversified|Defence|3480|232600
BDL|Bharat Dynamics|Diversified|Defence|1280|47000
MAZAGON|Mazagon Dock|Diversified|Defence Shipyard|2880|58100
COCHINSHIP|Cochin Shipyard|Diversified|Shipyard|780|20500
GRSE|Garden Reach Shipbuilders|Diversified|Defence Shipyard|1580|18100
MCX|Multi Commodity Exchange|Diversified|Exchange|2580|13200
BSE|BSE Ltd|Diversified|Exchange|2380|32200
CRISIL|CRISIL Ltd|Diversified|Credit Rating|4280|31200
IGL|Indraprastha Gas|Diversified|City Gas|420|29400
MGL|Mahanagar Gas|Diversified|City Gas|1180|11700
GUJGAS|Gujarat Gas|Diversified|City Gas|480|33000
SIEMENS|Siemens India|Diversified|Industrial|4580|163000
ABB|ABB India|Diversified|Industrial|5480|116000
HONAUT|Honeywell Automation|Diversified|Industrial|42000|37300
TRIDENT|Trident Ltd|Diversified|Textiles|32|16300
ARVIND|Arvind Ltd|Diversified|Textiles|280|7300
JKPAPER|JK Paper|Diversified|Paper|380|6600
BALRAMCHIN|Balrampur Chini|Diversified|Sugar|380|7700
TRIVENI|Triveni Engineering|Diversified|Sugar|380|8300
EIDPARRY|EID Parry|Diversified|Sugar|580|10200
WELSPUNIND|Welspun India|Diversified|Home Textiles|128|8500
DEEPIND|Deep Industries|Diversified|Oil Field Services|380|5200
MINDAIND|Minda Industries|Diversified|Auto Components|680|18500
CARTRADE|CarTrade Tech|Diversified|Auto Marketplace|680|3200"""

ETF_RAW = """NIFTYBEES|Nippon Nifty 50 BeES|ETF|Index ETF|245
BANKBEES|Nippon Bank BeES|ETF|Banking ETF|420
GOLDBEES|Nippon Gold BeES|ETF|Gold ETF|52
SILVERBEES|Nippon Silver BeES|ETF|Silver ETF|68
ITBEES|Nippon IT BeES|ETF|IT Sector ETF|38
PHARMABEES|Nippon Pharma BeES|ETF|Pharma ETF|18
JUNIORBEES|Nippon Nifty Next 50 BeES|ETF|Index ETF|520
LIQUIDBEES|Nippon Liquid BeES|ETF|Liquid ETF|1000
CPSEETF|CPSE ETF|ETF|PSU ETF|68
BHARAT22|Bharat 22 ETF|ETF|Diversified ETF|92
SETFNIF50|SBI Nifty 50 ETF|ETF|Index ETF|220
SETFNN50|SBI Nifty Next 50 ETF|ETF|Index ETF|580
SETFGOLD|SBI Gold ETF|ETF|Gold ETF|48
HDFCNIFTY|HDFC Nifty 50 ETF|ETF|Index ETF|215
HDFCSENSEX|HDFC Sensex ETF|ETF|Index ETF|620
HDFCGOLD|HDFC Gold ETF|ETF|Gold ETF|50
ICICINIF50|ICICI Nifty 50 ETF|ETF|Index ETF|218
ICICIBNKETF|ICICI Bank Nifty ETF|ETF|Banking ETF|410
KOTAKNIFTY|Kotak Nifty ETF|ETF|Index ETF|210
KOTAKGOLD|Kotak Gold ETF|ETF|Gold ETF|46
MOTILAL50|Motilal NASDAQ 100 ETF|ETF|International ETF|185
MON100|Motilal S and P 500 ETF|ETF|International ETF|35
MAFANG|Mirae FANG Plus ETF|ETF|International ETF|52
AUTOETF|Nippon Auto ETF|ETF|Auto Sector ETF|180
INFRAETF|Nippon Infra ETF|ETF|Infra Sector ETF|680
CONSUMETF|Nippon Consumption ETF|ETF|Consumption ETF|72
DIVOPPBEES|Nippon Dividend Opp ETF|ETF|Dividend ETF|38
EBBETF0425|Bharat Bond ETF Apr 2025|ETF|Bond ETF|1180
EBBETF0430|Bharat Bond ETF Apr 2030|ETF|Bond ETF|1350
EBBETF0431|Bharat Bond ETF Apr 2031|ETF|Bond ETF|1120
LOWVOLIETF|ICICI Low Vol 30 ETF|ETF|Factor ETF|142
QUAL30IETF|ICICI Quality 30 ETF|ETF|Factor ETF|280
ALPHAIETF|ICICI Alpha Low Vol ETF|ETF|Factor ETF|42
MIDCAPETF|Nippon Midcap 150 ETF|ETF|Midcap ETF|148
SMALLCAPETF|Nippon Smallcap 250 ETF|ETF|Smallcap ETF|82
MOM50ETF|Motilal Midcap ETF|ETF|Midcap ETF|28
PSUBNKBEES|Nippon PSU Bank BeES|ETF|PSU Bank ETF|68
PVTBNKBEES|Nippon Private Bank BeES|ETF|Private Bank ETF|320
MAKEINDIA|Mirae Make In India ETF|ETF|Thematic ETF|22
HEALTHETF|Mirae Healthcare ETF|ETF|Healthcare ETF|28
COMMOETF|Nippon Commodities ETF|ETF|Commodity ETF|185
FINBEES|Nippon Financial ETF|ETF|Financial ETF|290
SHARIABEES|Nippon Shariah BeES|ETF|Shariah ETF|320
MOM30ETF|Motilal Momentum 30 ETF|ETF|Momentum ETF|38
ABSLNN50ET|ABSL Nifty Next 50 ETF|ETF|Index ETF|540
HNGSNGBEES|Nippon Hang Seng BeES|ETF|International ETF|228
ITETF|Nippon Nifty IT ETF|ETF|IT Sector ETF|35
NETF|Nippon Nifty ETF|ETF|Index ETF|225
SENSEXETF|HDFC Sensex 30 ETF|ETF|Index ETF|680
SILVERETF|HDFC Silver ETF|ETF|Silver ETF|72"""

MF_RAW = """SBILCRF|SBI Bluechip Fund|Mutual Fund|Large Cap|72
SBISMCF|SBI Small Cap Fund|Mutual Fund|Small Cap|128
SBIELSS|SBI Long Term Equity Fund|Mutual Fund|ELSS|252
SBIFLXI|SBI Flexicap Fund|Mutual Fund|Flexi Cap|78
SBIBALF|SBI Balanced Advantage Fund|Mutual Fund|Hybrid|35
SBIEQUITY|SBI Equity Hybrid Fund|Mutual Fund|Hybrid|218
SBIMIDCAP|SBI Magnum Midcap Fund|Mutual Fund|Mid Cap|188
SBIFOCUSED|SBI Focused Equity Fund|Mutual Fund|Focused|280
SBIDBT|SBI Magnum Gilt Fund|Mutual Fund|Debt|52
SBIMULTI|SBI Multi Asset Allocation|Mutual Fund|Multi Asset|45
HDFCTOP100|HDFC Top 100 Fund|Mutual Fund|Large Cap|880
HDFCMIDOPP|HDFC Mid-Cap Opportunities|Mutual Fund|Mid Cap|148
HDFCSMALL|HDFC Small Cap Fund|Mutual Fund|Small Cap|82
HDFCFLXI|HDFC Flexi Cap Fund|Mutual Fund|Flexi Cap|1480
HDFCBAL|HDFC Balanced Advantage|Mutual Fund|Hybrid|368
HDFCEQUITY|HDFC Equity Fund|Mutual Fund|Multi Cap|1080
HDFCELSS|HDFC ELSS Tax Saver|Mutual Fund|ELSS|880
HDFCRETIRE|HDFC Retirement Savings|Mutual Fund|Retirement|28
HDFCDBT|HDFC Corporate Bond Fund|Mutual Fund|Debt|28
HDFCMULTI|HDFC Multi Asset Fund|Mutual Fund|Multi Asset|52
ICICIBCHIP|ICICI Pru Bluechip Fund|Mutual Fund|Large Cap|82
ICICIMID|ICICI Pru Midcap Fund|Mutual Fund|Mid Cap|218
ICICISML|ICICI Pru Smallcap Fund|Mutual Fund|Small Cap|62
ICICIFLXI|ICICI Pru Flexicap Fund|Mutual Fund|Flexi Cap|52
ICICIVAL|ICICI Pru Value Discovery|Mutual Fund|Value|350
ICICIELSS|ICICI Pru ELSS Tax Saver|Mutual Fund|ELSS|178
ICICIBALF|ICICI Pru Balanced Advantage|Mutual Fund|Hybrid|55
ICICIMULTI|ICICI Pru Multi Asset|Mutual Fund|Multi Asset|520
ICICIDBT|ICICI Pru All Seasons Bond|Mutual Fund|Debt|32
ICICITECH|ICICI Pru Technology Fund|Mutual Fund|Sectoral|148
AXISBCHIP|Axis Bluechip Fund|Mutual Fund|Large Cap|48
AXISMID|Axis Midcap Fund|Mutual Fund|Mid Cap|82
AXISSML|Axis Small Cap Fund|Mutual Fund|Small Cap|72
AXISFLXI|Axis Flexi Cap Fund|Mutual Fund|Flexi Cap|18
AXISELSS|Axis ELSS Tax Saver|Mutual Fund|ELSS|38
AXISFOCUS|Axis Focused 25 Fund|Mutual Fund|Focused|48
AXISMULTI|Axis Multi Asset Fund|Mutual Fund|Multi Asset|22
KOTAKBCHIP|Kotak Bluechip Fund|Mutual Fund|Large Cap|420
KOTAKMID|Kotak Emerging Equity Fund|Mutual Fund|Mid Cap|88
KOTAKSML|Kotak Small Cap Fund|Mutual Fund|Small Cap|178
KOTAKFLXI|Kotak Flexicap Fund|Mutual Fund|Flexi Cap|62
KOTAKELSS|Kotak ELSS Tax Saver|Mutual Fund|ELSS|82
KOTAKBAL|Kotak Balanced Advantage|Mutual Fund|Hybrid|15
KOTAKMULTI|Kotak Multi Asset Fund|Mutual Fund|Multi Asset|18
NIPPONLCF|Nippon India Large Cap|Mutual Fund|Large Cap|68
NIPPONMID|Nippon India Growth Fund|Mutual Fund|Mid Cap|2880
NIPPONSML|Nippon India Small Cap|Mutual Fund|Small Cap|128
NIPPONFLXI|Nippon India Flexi Cap|Mutual Fund|Flexi Cap|15
NIPPONELSS|Nippon India ELSS Tax Saver|Mutual Fund|ELSS|92
NIPPONPHRM|Nippon India Pharma Fund|Mutual Fund|Sectoral|320
NIPPONBANK|Nippon India Banking Fund|Mutual Fund|Sectoral|480
NIPPONMULT|Nippon India Multi Asset|Mutual Fund|Multi Asset|14
ABSLFRONT|ABSL Frontline Equity|Mutual Fund|Large Cap|380
ABSLMID|ABSL Midcap Fund|Mutual Fund|Mid Cap|580
ABSLSML|ABSL Small Cap Fund|Mutual Fund|Small Cap|62
ABSLFLXI|ABSL Flexi Cap Fund|Mutual Fund|Flexi Cap|1280
ABSLELSS|ABSL ELSS Tax Saver|Mutual Fund|ELSS|42
ABSLBAL|ABSL Balanced Advantage|Mutual Fund|Hybrid|68
ABSLMULTI|ABSL Multi Asset Fund|Mutual Fund|Multi Asset|78
DSPLARGE|DSP Top 100 Fund|Mutual Fund|Large Cap|365
DSPMID|DSP Midcap Fund|Mutual Fund|Mid Cap|82
DSPSML|DSP Small Cap Fund|Mutual Fund|Small Cap|135
DSPFLXI|DSP Flexi Cap Fund|Mutual Fund|Flexi Cap|62
DSPELSS|DSP ELSS Tax Saver|Mutual Fund|ELSS|92
DSPMULTI|DSP Multi Asset Fund|Mutual Fund|Multi Asset|18
MOTILLARGE|Motilal Large Cap Fund|Mutual Fund|Large Cap|38
MOTILMID|Motilal Midcap Fund|Mutual Fund|Mid Cap|52
MOTILFLXI|Motilal Flexi Cap Fund|Mutual Fund|Flexi Cap|42
MOTILELSS|Motilal ELSS Fund|Mutual Fund|ELSS|32
MOTILNASDAQ|Motilal NASDAQ 100 FoF|Mutual Fund|International|28
MOTILSP500|Motilal S and P 500 FoF|Mutual Fund|International|18
PPFLARGE|PPFAS Flexi Cap Fund|Mutual Fund|Flexi Cap|58
PPFASFLXI|Parag Parikh Flexi Cap|Mutual Fund|Flexi Cap|62
PPFASELSS|Parag Parikh ELSS Tax Saver|Mutual Fund|ELSS|22
MIRAILARGE|Mirae Large Cap Fund|Mutual Fund|Large Cap|82
MIRAEMID|Mirae Midcap Fund|Mutual Fund|Mid Cap|22
MIRAESML|Mirae Emerging Bluechip|Mutual Fund|Large Mid Cap|118
MIRAIELSS|Mirae ELSS Tax Saver|Mutual Fund|ELSS|38
FRANKLARGE|Franklin India Bluechip|Mutual Fund|Large Cap|720
FRANKMID|Franklin India Prima Fund|Mutual Fund|Mid Cap|1680
FRANKSML|Franklin Smaller Companies|Mutual Fund|Small Cap|108
FRANKELSS|Franklin ELSS Tax Saver|Mutual Fund|ELSS|82
FRANKFOCUS|Franklin Focused Equity|Mutual Fund|Focused|82
TATALARGE|Tata Large Cap Fund|Mutual Fund|Large Cap|380
TATAMID|Tata Midcap Growth Fund|Mutual Fund|Mid Cap|280
TATASML|Tata Small Cap Fund|Mutual Fund|Small Cap|22
TATAFLXI|Tata Flexi Cap Fund|Mutual Fund|Flexi Cap|18
TATAELSS|Tata ELSS Tax Saver|Mutual Fund|ELSS|35
TATABAL|Tata Balanced Advantage|Mutual Fund|Hybrid|15
INVLARGE|Invesco India Largecap|Mutual Fund|Large Cap|48
INVMID|Invesco India Midcap|Mutual Fund|Mid Cap|105
INVSML|Invesco India Smallcap|Mutual Fund|Small Cap|22
INVELSS|Invesco India ELSS|Mutual Fund|ELSS|82
QUANTSML|Quant Small Cap Fund|Mutual Fund|Small Cap|178
QUANTMID|Quant Mid Cap Fund|Mutual Fund|Mid Cap|148
QUANTFLXI|Quant Flexi Cap Fund|Mutual Fund|Flexi Cap|72
QUANTELSS|Quant ELSS Tax Saver|Mutual Fund|ELSS|252
QUANTACT|Quant Active Fund|Mutual Fund|Multi Cap|480
QUANTINFRA|Quant Infrastructure Fund|Mutual Fund|Sectoral|32
UTIMID|UTI Mid Cap Fund|Mutual Fund|Mid Cap|248
UTISML|UTI Small Cap Fund|Mutual Fund|Small Cap|18
UTIFLXI|UTI Flexi Cap Fund|Mutual Fund|Flexi Cap|282
UTIELSS|UTI ELSS Tax Saver|Mutual Fund|ELSS|178
UTINIFTY|UTI Nifty 50 Index Fund|Mutual Fund|Index|148
CANRLARGE|Canara Robeco Bluechip|Mutual Fund|Large Cap|42
CANRMID|Canara Robeco Midcap|Mutual Fund|Mid Cap|38
CANRSML|Canara Robeco Small Cap|Mutual Fund|Small Cap|22
CANRELSS|Canara Robeco ELSS|Mutual Fund|ELSS|118
BANDHANCORE|Bandhan Core Equity|Mutual Fund|Large Cap|92
BANDHANMID|Bandhan Midcap Fund|Mutual Fund|Mid Cap|18
BANDHANSML|Bandhan Small Cap|Mutual Fund|Small Cap|22
WHITEOAK|WhiteOak Capital Flexi Cap|Mutual Fund|Flexi Cap|15
WHITEOAKSML|WhiteOak Capital Small Cap|Mutual Fund|Small Cap|18
JMFLEXICAP|JM Flexicap Fund|Mutual Fund|Flexi Cap|78
JMVALUE|JM Value Fund|Mutual Fund|Value|68
IDFC_CORE|IDFC Core Equity Fund|Mutual Fund|Large Cap|72
EDELFLXI|Edelweiss Flexi Cap|Mutual Fund|Flexi Cap|28
EDELSML|Edelweiss Small Cap|Mutual Fund|Small Cap|22
EDELMID|Edelweiss Mid Cap|Mutual Fund|Mid Cap|52
EDELELSS|Edelweiss ELSS|Mutual Fund|ELSS|32
SUNLARGE|Sundaram Large Cap|Mutual Fund|Large Cap|48
SUNMID|Sundaram Mid Cap|Mutual Fund|Mid Cap|780
SUNSML|Sundaram Small Cap|Mutual Fund|Small Cap|148
SUNELSS|Sundaram ELSS|Mutual Fund|ELSS|68
TAURUSLARGE|Taurus Largecap Fund|Mutual Fund|Large Cap|22
PGIMFLEXI|PGIM India Flexi Cap|Mutual Fund|Flexi Cap|28
PGIMMID|PGIM India Midcap Opp|Mutual Fund|Mid Cap|42
MAHINDRAMF|Mahindra Manulife Mid Cap|Mutual Fund|Mid Cap|18"""

def parse_stocks(raw):
    items = []
    for line in raw.strip().split("\n"):
        parts = line.split("|")
        sym, name, sector, industry, price, mcap = parts[0], parts[1], parts[2], parts[3], float(parts[4]), float(parts[5])
        items.append((sym, name, "stock", sector, industry, price, mcap))
    return items

def parse_etf_mf(raw, typ):
    items = []
    for line in raw.strip().split("\n"):
        parts = line.split("|")
        sym, name, sector, industry, price = parts[0], parts[1], parts[2], parts[3], float(parts[4])
        items.append((sym, name, typ, sector, industry, price, None))
    return items

# Parse all
all_raw = parse_stocks(RAW) + parse_etf_mf(ETF_RAW, "etf") + parse_etf_mf(MF_RAW, "mf")

# Deduplicate by symbol
seen = set()
instruments = []
iid = 0
for sym, name, typ, sector, industry, price, mcap in all_raw:
    if sym in seen:
        continue
    seen.add(sym)
    iid += 1
    instruments.append((iid, sym, name, typ, sector, industry, price, mcap))

print(f"Total unique instruments: {len(instruments)}")

# ── Write Python data ──
outdir = r"d:\WD Lab Project"
with open(os.path.join(outdir, "generated_data.py"), "w", encoding="utf-8") as f:
    f.write("# Auto-generated: %d instruments\n\n" % len(instruments))
    f.write("GENERATED_INSTRUMENTS = [\n")
    for (id_, sym, name, typ, sector, industry, price, mcap) in instruments:
        dc = round(random.uniform(-price*0.03, price*0.03), 2)
        dcp = round((dc/price)*100, 2)
        h52 = round(price * random.uniform(1.10, 1.30), 2)
        l52 = round(price * random.uniform(0.65, 0.88), 2)
        sn = name.replace("'", "\\'")
        ms = str(int(mcap)) if mcap else "None"
        f.write(f'    {{"id":{id_},"symbol":"{sym}","name":"{sn}","type":"{typ}","exchange":"NSE","sector":"{sector}","industry":"{industry}","market_cap":{ms},"current_price":{price},"day_change":{dc},"day_change_pct":{dcp},"high_52w":{h52},"low_52w":{l52},"is_active":True}},\n')
    f.write("]\n\n")
    
    # Fundamentals for stocks only
    f.write("GENERATED_FUND_DATA = [\n")
    for (id_, sym, name, typ, sector, industry, price, mcap) in instruments:
        if typ != "stock" or not mcap:
            continue
        pe = round(random.uniform(5, 80), 1)
        pb = round(random.uniform(0.5, 30), 1)
        roe = round(random.uniform(5, 45), 1)
        roce = round(random.uniform(5, 55), 1)
        eps = round(price/pe if pe > 0 else 10, 1)
        de = round(random.uniform(0, 2), 2)
        npm = round(random.uniform(3, 30), 1)
        ph = round(random.uniform(0, 75), 1)
        sg = round(random.uniform(-5, 30), 1)
        pg = round(random.uniform(-10, 40), 1)
        rev = int(mcap * random.uniform(0.1, 0.8))
        np_val = int(rev * npm / 100)
        f.write(f"    ({id_},{pe},{pb},{roe},{roce},{eps},{de},{npm},{ph},{sg},{pg},{rev},{np_val}),\n")
    f.write("]\n")

# ── Write SQL seed ──
with open(os.path.join(outdir, "generated_seed.sql"), "w", encoding="utf-8") as f:
    f.write("-- Auto-generated: %d instruments\n\n" % len(instruments))
    f.write("INSERT INTO instruments (symbol, name, type, exchange, sector, industry, market_cap, current_price, day_change, day_change_pct, high_52w, low_52w) VALUES\n")
    rows = []
    for (id_, sym, name, typ, sector, industry, price, mcap) in instruments:
        dc = round(random.uniform(-price*0.03, price*0.03), 2)
        dcp = round((dc/price)*100, 2)
        h52 = round(price * random.uniform(1.10, 1.30), 2)
        l52 = round(price * random.uniform(0.65, 0.88), 2)
        sn = name.replace("'", "''")
        si = industry.replace("'", "''")
        ms = "%.2f" % mcap if mcap else "NULL"
        rows.append(f"('{sym}','{sn}','{typ}','NSE','{sector}','{si}',{ms},{price},{dc},{dcp},{h52},{l52})")
    f.write(",\n".join(rows) + ";\n")

print(f"Done! Output: generated_data.py, generated_seed.sql")
