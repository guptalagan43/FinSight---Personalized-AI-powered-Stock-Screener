-- ============================================================
-- Screener.AI – Database Schema (PostgreSQL)
-- ============================================================

-- Enum types
CREATE TYPE risk_profile AS ENUM ('Conservative', 'Moderate', 'Aggressive');
CREATE TYPE experience_level AS ENUM ('Beginner', 'Intermediate', 'Professional');
CREATE TYPE instrument_type AS ENUM ('stock', 'etf', 'mf', 'commodity');
CREATE TYPE user_role AS ENUM ('user', 'admin');

-- ============================================================
-- USERS
-- ============================================================
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    name            VARCHAR(150) NOT NULL,
    age             INTEGER,
    dob             VARCHAR(20),
    mobile_number   VARCHAR(20),
    marital_status  VARCHAR(50),
    gender          VARCHAR(50),
    income_range    VARCHAR(50),
    occupation      VARCHAR(50),
    fathers_name    VARCHAR(150),
    country         VARCHAR(100) DEFAULT 'India',
    risk_profile    risk_profile DEFAULT 'Moderate',
    experience_level experience_level DEFAULT 'Beginner',
    monthly_investment_capacity NUMERIC(12,2),
    yearly_investment_capacity  NUMERIC(14,2),
    goals           TEXT,                          -- JSON string: ["Wealth creation","Retirement"]
    is_email_verified BOOLEAN DEFAULT FALSE,
    is_active       BOOLEAN DEFAULT TRUE,
    role            user_role DEFAULT 'user',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- OTP TABLE
-- ============================================================
CREATE TABLE otps (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    otp_code    VARCHAR(10) NOT NULL,
    expires_at  TIMESTAMP NOT NULL,
    is_used     BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_otps_user ON otps(user_id);

-- ============================================================
-- INSTRUMENTS
-- ============================================================
CREATE TABLE instruments (
    id                SERIAL PRIMARY KEY,
    symbol            VARCHAR(30) NOT NULL,
    name              VARCHAR(255) NOT NULL,
    type              instrument_type DEFAULT 'stock',
    exchange          VARCHAR(30) DEFAULT 'NSE',
    sector            VARCHAR(100),
    industry          VARCHAR(150),
    api_reference_id  VARCHAR(100),    -- external API identifier
    market_cap        NUMERIC(18,2),
    current_price     NUMERIC(12,2),
    day_change        NUMERIC(8,2),
    day_change_pct    NUMERIC(6,2),
    high_52w          NUMERIC(12,2),
    low_52w           NUMERIC(12,2),
    updated_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_instruments_symbol ON instruments(symbol);
CREATE INDEX idx_instruments_sector ON instruments(sector);

-- ============================================================
-- INSTRUMENT FUNDAMENTALS (one row per fiscal year)
-- ============================================================
CREATE TABLE instrument_fundamentals (
    id              SERIAL PRIMARY KEY,
    instrument_id   INTEGER NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    fiscal_year     VARCHAR(10) NOT NULL,       -- e.g. 'FY2024'
    revenue         NUMERIC(18,2),
    net_profit      NUMERIC(18,2),
    eps             NUMERIC(10,2),
    debt            NUMERIC(18,2),
    equity          NUMERIC(18,2),
    roe             NUMERIC(8,2),
    roce            NUMERIC(8,2),
    pe              NUMERIC(8,2),
    pb              NUMERIC(8,2),
    debt_to_equity  NUMERIC(8,2),
    promoter_holding NUMERIC(6,2),
    net_profit_margin NUMERIC(8,2),
    sales_growth    NUMERIC(8,2),
    profit_growth   NUMERIC(8,2),
    UNIQUE(instrument_id, fiscal_year)
);
CREATE INDEX idx_fundamentals_instr ON instrument_fundamentals(instrument_id);

-- ============================================================
-- WATCHLISTS
-- ============================================================
CREATE TABLE watchlists (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name        VARCHAR(100) NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_watchlists_user ON watchlists(user_id);

-- ============================================================
-- WATCHLIST ITEMS
-- ============================================================
CREATE TABLE watchlist_items (
    id              SERIAL PRIMARY KEY,
    watchlist_id    INTEGER NOT NULL REFERENCES watchlists(id) ON DELETE CASCADE,
    instrument_id   INTEGER NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    added_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(watchlist_id, instrument_id)
);

-- ============================================================
-- PORTFOLIO POSITIONS (simulated)
-- ============================================================
CREATE TABLE portfolio_positions (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    instrument_id   INTEGER NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    quantity        NUMERIC(12,4) NOT NULL,
    buy_price       NUMERIC(12,2) NOT NULL,
    buy_date        DATE NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_positions_user ON portfolio_positions(user_id);

-- ============================================================
-- SCREENERS
-- ============================================================
CREATE TABLE screeners (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users(id) ON DELETE CASCADE,  -- NULL = predefined
    name            VARCHAR(200) NOT NULL,
    description     TEXT,
    definition_json TEXT NOT NULL,          -- JSON filter rules
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_screeners_user ON screeners(user_id);

-- ============================================================
-- CHAT LOGS
-- ============================================================
CREATE TABLE chat_logs (
    id                  SERIAL PRIMARY KEY,
    user_id             INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    instrument_id       INTEGER REFERENCES instruments(id) ON DELETE SET NULL,
    user_message        TEXT NOT NULL,
    ai_response_summary TEXT,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_chatlogs_user ON chat_logs(user_id);

-- ============================================================
-- SETTINGS (key-value store for admin config)
-- ============================================================
CREATE TABLE settings (
    id      SERIAL PRIMARY KEY,
    key     VARCHAR(100) UNIQUE NOT NULL,
    value   TEXT NOT NULL
);
