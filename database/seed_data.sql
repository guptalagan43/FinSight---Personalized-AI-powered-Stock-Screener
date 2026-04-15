-- ============================================================
-- Screener.AI – Seed Data
-- ============================================================
-- NOTE: Password hash below is for "Password@123" using bcrypt
-- In production, generate proper hashes via the app.

-- ============================================================
-- USERS (1 admin + 2 regular)
-- ============================================================
INSERT INTO users (email, password_hash, name, age, country, risk_profile, experience_level, monthly_investment_capacity, yearly_investment_capacity, goals, is_email_verified, role) VALUES
('admin@screener.ai',  '$2b$12$LJ3m6Zq1E5sK8v2HdW1oAeYbX3cN6rP9tQ4wU7vZaS0dF8gHjKlMn', 'Admin User',    30, 'India', 'Moderate',     'Professional', 50000, 600000, '["Platform Management"]', TRUE,  'admin'),
('rahul@example.com',  '$2b$12$LJ3m6Zq1E5sK8v2HdW1oAeYbX3cN6rP9tQ4wU7vZaS0dF8gHjKlMn', 'Rahul Sharma',  28, 'India', 'Aggressive',   'Intermediate', 25000, 300000, '["Wealth creation","Trading"]', TRUE, 'user'),
('priya@example.com',  '$2b$12$LJ3m6Zq1E5sK8v2HdW1oAeYbX3cN6rP9tQ4wU7vZaS0dF8gHjKlMn', 'Priya Patel',   24, 'India', 'Conservative', 'Beginner',     10000, 120000, '["Retirement","Wealth creation"]', TRUE, 'user');

-- ============================================================
-- INSTRUMENTS (~15 across 5 sectors)
-- ============================================================
INSERT INTO instruments (symbol, name, type, exchange, sector, industry, market_cap, current_price, day_change, day_change_pct, high_52w, low_52w) VALUES
-- IT
('TCS',       'Tata Consultancy Services',  'stock', 'NSE', 'Information Technology', 'IT Services',       1380000.00, 3845.50,  32.10,  0.84, 4250.00, 3300.00),
('INFY',      'Infosys Ltd',                'stock', 'NSE', 'Information Technology', 'IT Services',        620000.00, 1520.75, -12.30, -0.80, 1780.00, 1280.00),
('WIPRO',     'Wipro Ltd',                  'stock', 'NSE', 'Information Technology', 'IT Services',        230000.00,  445.20,   5.60,  1.27,  520.00,  380.00),
-- Banking
('HDFCBANK',  'HDFC Bank Ltd',              'stock', 'NSE', 'Banking',               'Private Bank',       870000.00, 1680.30,  18.90,  1.14, 1880.00, 1420.00),
('ICICIBANK', 'ICICI Bank Ltd',             'stock', 'NSE', 'Banking',               'Private Bank',       650000.00, 1125.40,  -8.60, -0.76, 1310.00,  940.00),
('SBIN',      'State Bank of India',        'stock', 'NSE', 'Banking',               'Public Bank',        520000.00,  585.90,   7.40,  1.28,  680.00,  490.00),
-- Pharma
('SUNPHARMA', 'Sun Pharmaceutical',         'stock', 'NSE', 'Pharma',                'Pharmaceuticals',    310000.00, 1285.60,  15.20,  1.20, 1450.00, 1050.00),
('DRREDDY',   'Dr. Reddy''s Laboratories',  'stock', 'NSE', 'Pharma',                'Pharmaceuticals',    105000.00, 6320.00, -45.00, -0.71, 6800.00, 5200.00),
-- Energy
('RELIANCE',  'Reliance Industries Ltd',    'stock', 'NSE', 'Energy',                'Conglomerate',      1650000.00, 2450.80,  28.50,  1.18, 2850.00, 2100.00),
('ONGC',      'Oil & Natural Gas Corp',     'stock', 'NSE', 'Energy',                'Oil & Gas',          280000.00,  245.30,   3.10,  1.28,  295.00,  185.00),
('POWERGRID', 'Power Grid Corp',            'stock', 'NSE', 'Energy',                'Power',              230000.00,  268.40,   2.80,  1.05,  320.00,  210.00),
-- FMCG
('HINDUNILVR','Hindustan Unilever Ltd',     'stock', 'NSE', 'FMCG',                  'Personal Care',      570000.00, 2420.10, -18.50, -0.76, 2780.00, 2150.00),
('ITC',       'ITC Ltd',                    'stock', 'NSE', 'FMCG',                  'Diversified FMCG',   530000.00,  428.90,   6.20,  1.47,  500.00,  360.00),
-- ETFs & MFs
('NIFTYBEES', 'Nippon Nifty BeES',          'etf',   'NSE', 'Index',                 'Index ETF',           NULL,       245.60,   2.10,  0.86,  275.00,  210.00),
('GOLDBEES',  'Nippon Gold BeES',           'etf',   'NSE', 'Commodity',             'Gold ETF',            NULL,        52.40,   0.35,  0.67,   58.00,   42.00);

-- ============================================================
-- INSTRUMENT FUNDAMENTALS (latest 3 fiscal years for key stocks)
-- ============================================================
INSERT INTO instrument_fundamentals (instrument_id, fiscal_year, revenue, net_profit, eps, debt, equity, roe, roce, pe, pb, debt_to_equity, promoter_holding, net_profit_margin, sales_growth, profit_growth) VALUES
-- TCS (id=1)
(1, 'FY2024', 241987.00, 46502.00, 127.50, 12500.00, 89500.00, 48.50, 62.30, 30.15, 14.20, 0.14, 72.30, 19.22, 8.50,  9.20),
(1, 'FY2023', 225458.00, 42147.00, 115.40, 11200.00, 82000.00, 47.20, 60.80, 31.50, 13.80, 0.14, 72.30, 18.69, 17.60, 14.80),
(1, 'FY2022', 191754.00, 38327.00, 104.80, 10800.00, 75000.00, 46.80, 59.20, 35.40, 15.60, 0.14, 72.30, 20.01, 15.90, 18.20),
-- INFY (id=2)
(2, 'FY2024', 161324.00, 26233.00, 63.40,  8200.00, 68500.00, 32.40, 40.10, 23.98, 7.80, 0.12, 31.20, 16.26, 4.70,  6.80),
(2, 'FY2023', 153670.00, 24095.00, 58.20,  7800.00, 63000.00, 31.80, 39.50, 25.10, 8.20, 0.12, 31.20, 15.68, 20.70, 15.40),
(2, 'FY2022', 127380.00, 22110.00, 53.40,  7200.00, 58000.00, 30.90, 38.40, 30.20, 9.60, 0.12, 31.20, 17.36, 19.80, 12.60),
-- HDFCBANK (id=4)
(4, 'FY2024', 285340.00, 57061.00, 75.10, 420000.00, 345000.00, 17.50, 2.10, 22.38, 3.60, 1.22, 26.10, 20.00, 38.50, 39.20),
(4, 'FY2023', 206000.00, 45997.00, 60.50, 380000.00, 310000.00, 16.80, 2.00, 24.10, 3.80, 1.23, 26.10, 22.33, 20.50, 21.40),
-- RELIANCE (id=9)
(9, 'FY2024', 966280.00, 79020.00, 116.80, 315000.00, 520000.00, 9.20, 10.80, 20.98, 2.40, 0.61, 50.30,  8.18, 2.60,  7.90),
(9, 'FY2023', 941480.00, 73200.00, 108.20, 298000.00, 480000.00, 8.80, 10.20, 22.50, 2.60, 0.62, 50.30,  7.78, 23.80, 11.30),
-- HINDUNILVR (id=12)
(12, 'FY2024', 60580.00, 10282.00, 43.80, 2200.00, 42000.00, 24.50, 32.80, 55.25, 11.20, 0.05, 61.90, 16.97, 2.30,  1.80),
(12, 'FY2023', 59220.00, 10100.00, 43.00, 2100.00, 40500.00, 24.20, 32.10, 56.80, 11.80, 0.05, 61.90, 17.06, 16.00, 13.50),
-- ITC (id=13)
(13, 'FY2024', 70919.00, 20051.00, 16.10, 1500.00, 65000.00, 28.40, 36.50, 26.64, 7.80, 0.02, 0.00, 28.27, 5.20,  9.60),
(13, 'FY2023', 67420.00, 18820.00, 15.12, 1400.00, 60000.00, 27.80, 35.20, 28.10, 8.20, 0.02, 0.00, 27.91, 17.80, 24.30);

-- ============================================================
-- PREDEFINED SCREENERS
-- ============================================================
INSERT INTO screeners (user_id, name, description, definition_json) VALUES
(NULL, 'High ROE Blue Chips', 'Companies with ROE > 20% and market cap > 100000 Cr', '{"conditions":[{"field":"roe","op":">","value":20},{"field":"market_cap","op":">","value":100000}],"logic":"AND"}'),
(NULL, 'Low Debt Growth Stocks', 'Low leverage companies with strong profit growth', '{"conditions":[{"field":"debt_to_equity","op":"<","value":0.3},{"field":"profit_growth","op":">","value":10}],"logic":"AND"}'),
(NULL, 'Value Picks', 'Undervalued stocks with PE < 15 and ROE > 15%', '{"conditions":[{"field":"pe","op":"<","value":15},{"field":"roe","op":">","value":15}],"logic":"AND"}'),
(NULL, 'High Margin Leaders', 'Companies with net profit margin > 20%', '{"conditions":[{"field":"net_profit_margin","op":">","value":20}],"logic":"AND"}'),
(NULL, 'Growth Champions', 'High sales and profit growth stocks', '{"conditions":[{"field":"sales_growth","op":">","value":12},{"field":"profit_growth","op":">","value":15}],"logic":"AND"}'),
(NULL, 'Large Cap Compounders', 'Large caps with consistent growth and high ROE', '{"conditions":[{"field":"market_cap","op":">","value":50000},{"field":"roe","op":">","value":15},{"field":"sales_growth","op":">","value":10}],"logic":"AND"}'),
(NULL, 'Debt-Free Compounders', 'Companies with almost no debt and high ROCE', '{"conditions":[{"field":"debt_to_equity","op":"<","value":0.1},{"field":"roce","op":">","value":20}],"logic":"AND"}'),
(NULL, 'Deep Value', 'Extremely cheap stocks based on earnings and book value', '{"conditions":[{"field":"pe","op":"<","value":10},{"field":"pb","op":"<","value":1.5}],"logic":"AND"}'),
(NULL, 'Midcap Growth Stars', 'Mid-sized companies showing strong profit growth', '{"conditions":[{"field":"market_cap","op":">","value":5000},{"field":"profit_growth","op":">","value":20}],"logic":"AND"}'),
(NULL, 'Efficient Capital Allocators', 'Companies generating high returns on capital', '{"conditions":[{"field":"roce","op":">","value":25},{"field":"roe","op":">","value":20}],"logic":"AND"}'),
(NULL, 'Rapid Profit Growers', 'Companies growing profits at an exceptional rate', '{"conditions":[{"field":"profit_growth","op":">","value":30},{"field":"sales_growth","op":">","value":20}],"logic":"AND"}'),
(NULL, 'Microcap Gems', 'Small companies with explosive growth metrics', '{"conditions":[{"field":"market_cap","op":"<","value":5000},{"field":"profit_growth","op":">","value":25},{"field":"roe","op":">","value":15}],"logic":"AND"}');

-- ============================================================
-- DEFAULT SETTINGS
-- ============================================================
INSERT INTO settings (key, value) VALUES
('data_refresh_interval_seconds', '60'),
('ai_chatbot_enabled',            'true'),
('calculators_enabled',            'true'),
('max_watchlists_per_user',        '10'),
('otp_expiry_minutes',             '10');

INSERT INTO instruments (symbol, name, type, exchange, sector, industry, market_cap, current_price, day_change, day_change_pct, high_52w, low_52w, is_active) VALUES
('NIFTY_50', 'NIFTY 50', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('SENSEX', 'SENSEX', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('NIFTY_BANK', 'NIFTY BANK', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('INDIA_VIX', 'India VIX', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('NIFTY_MIDCAP_100', 'NIFTY Midcap 100', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('NIFTY_SMALLCAP_100', 'NIFTY Smallcap 100', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('NIFTY_MIDCAP_150', 'NIFTY MIDCAP 150', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('NIFTY_PHARMA', 'NIFTY Pharma', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('NIFTY_100', 'NIFTY 100', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('NIFTY_AUTO', 'NIFTY Auto', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('KOSPI_INDEX', 'KOSPI Index', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('HANG_SENG_INDEX', 'HANG SENG Index', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('US_TECH_100', 'US Tech 100', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('DOW_JONES_FUTURES', 'Dow Jones Futures', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('DOW_JONES_INDEX', 'Dow Jones Index', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('BSE_100', 'BSE 100', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('NIFTY_REALTY', 'NIFTY Realty', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('NIFTY_PSU_BANK', 'NIFTY PSU Bank', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('GIFT_NIFTY', 'Gift Nifty', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('FTSE_100_INDEX', 'FTSE 100 Index', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('NIKKEI_INDEX', 'Nikkei Index', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('NIFTY_FMCG', 'NIFTY FMCG', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('BSE_BANKEX', 'BSE BANKEX', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('S&P_500', 'S&P 500', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('NIFTY_NEXT_50', 'NIFTY NEXT 50', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('NIFTY_METAL', 'NIFTY Metal', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('DAX_INDEX', 'DAX Index', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('NIFTY_FIN_SERVICE', 'NIFTY Fin Service', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('CAC_INDEX', 'CAC Index', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true),
('NIFTY_PVT_BANK', 'Nifty Pvt Bank', 'index', 'NSE', 'Index', 'Index', NULL, 20000.0, 100.0, 0.5, 25000.0, 15000.0, true);
