"""
Market Routes – Live market data endpoints.
Fetches real-time quotes from the configured data provider (yfinance).
"""
from flask import Blueprint, request, jsonify
from services.data_provider_service import get_data_provider

market_bp = Blueprint("market", __name__)

# ── Symbol mapping for Yahoo Finance ─────────────────────────
# Maps our internal/display names to Yahoo Finance ticker symbols
SYMBOL_MAP = {
    # Indian Indices
    "NIFTY 50": "^NSEI",
    "NIFTY_50": "^NSEI",
    "SENSEX": "^BSESN",
    "BANKNIFTY": "^NSEBANK",
    "NIFTY_BANK": "^NSEBANK",
    "NIFTY IT": "^CNXIT",
    "NIFTY MIDCAP 100": "NIFTY_MIDCAP_100.NS",
    "NIFTY SMALLCAP": "^CNXSC",
    "FINNIFTY": "NIFTY_FIN_SERVICE.NS",
    "NIFTY AUTO": "^CNXAUTO",
    "NIFTY METAL": "^CNXMETAL",
    "NIFTY PHARMA": "^CNXPHARMA",
    "NIFTY FMCG": "^CNXFMCG",
    "NIFTY REALTY": "^CNXREALTY",
    "INDIA VIX": "^INDIAVIX",
    # Indian Stocks (NSE)
    "RELIANCE": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "HDFC BANK": "HDFCBANK.NS",
    "INFY": "INFY.NS",
    "INFOSYS": "INFY.NS",
    "ITC": "ITC.NS",
    "LT": "LT.NS",
    "L&T": "LT.NS",
    "MARUTI": "MARUTI.NS",
    "TATAMOTORS": "TATAMOTORS.NS",
    "TATA MOTORS": "TATAMOTORS.NS",
    "SBIN": "SBIN.NS",
    "SBI": "SBIN.NS",
    "ICICIBANK": "ICICIBANK.NS",
    "ICICI BANK": "ICICIBANK.NS",
    "WIPRO": "WIPRO.NS",
    "BAJFINANCE": "BAJFINANCE.NS",
    "SUNPHARMA": "SUNPHARMA.NS",
    "AXISBANK": "AXISBANK.NS",
    "KOTAKBANK": "KOTAKBANK.NS",
    "BHARTIARTL": "BHARTIARTL.NS",
    "HINDUNILVR": "HINDUNILVR.NS",
    "ASIANPAINT": "ASIANPAINT.NS",
    "DRREDDY": "DRREDDY.NS",
    "ONGC": "ONGC.NS",
    "POWERGRID": "POWERGRID.NS",
    "NTPC": "NTPC.NS",
    "COALINDIA": "COALINDIA.NS",
    "TITAN": "TITAN.NS",
    "ADANIENT": "ADANIENT.NS",
    "ADANIPORTS": "ADANIPORTS.NS",
    "TECHM": "TECHM.NS",
    "HCLTECH": "HCLTECH.NS",
    "ULTRACEMCO": "ULTRACEMCO.NS",
    "JSWSTEEL": "JSWSTEEL.NS",
    "TATASTEEL": "TATASTEEL.NS",
    "M&M": "M&M.NS",
    "CIPLA": "CIPLA.NS",
    "DIVISLAB": "DIVISLAB.NS",
    "EICHERMOT": "EICHERMOT.NS",
    "BPCL": "BPCL.NS",
    "HEROMOTOCO": "HEROMOTOCO.NS",
    "NESTLEIND": "NESTLEIND.NS",
    "GRASIM": "GRASIM.NS",
    "APOLLOHOSP": "APOLLOHOSP.NS",
    "SBILIFE": "SBILIFE.NS",
    "BAJAJFINSV": "BAJAJFINSV.NS",
    "TATACONSUM": "TATACONSUM.NS",
    "BRITANNIA": "BRITANNIA.NS",
    # Mid/Small Caps
    "SUZLON": "SUZLON.NS",
    "IREDA": "IREDA.NS",
    "NHPC": "NHPC.NS",
    "IRFC": "IRFC.NS",
    "ZOMATO": "ZOMATO.NS",
    "PAYTM": "PAYTM.NS",
    "JIOFIN": "JIOFIN.NS",
    "JIOFINANCE": "JIOFIN.NS",
    "TATATECH": "TATATECH.NS",
    "TATA TECH": "TATATECH.NS",
    "CDSL": "CDSL.NS",
    "BSE": "BSE.NS",
    # ETFs
    "NIFTYBEES": "NIFTYBEES.NS",
    "BANKBEES": "BANKBEES.NS",
    "GOLDBEES": "GOLDBEES.NS",
    "LIQUIDBEES": "LIQUIDBEES.NS",
    "ITBEES": "ITBEES.NS",
    "PHARMABEES": "PHARMABEES.NS",
    "MON100": "MON100.NS",
    "CPSEETF": "CPSEETF.NS",
    "MID150BEES": "MID150BEES.NS",
    "SILVERBEES": "SILVERBEES.NS",
}


def _resolve_yf_symbol(name: str) -> str:
    """Convert a display name to a Yahoo Finance symbol."""
    upper = name.strip().upper()
    if upper in SYMBOL_MAP:
        return SYMBOL_MAP[upper]
    # If already has a dot (like RELIANCE.NS), use as-is
    if "." in name or name.startswith("^"):
        return name
    # Default: assume NSE stock
    return f"{upper}.NS"


def _fetch_quote(yf_symbol: str) -> dict:
    """Fetch a single quote from Yahoo Finance."""
    import yfinance as yf
    try:
        ticker = yf.Ticker(yf_symbol)
        info = ticker.info or {}

        price = info.get("regularMarketPrice") or info.get("currentPrice") or 0
        prev = info.get("regularMarketPreviousClose") or info.get("previousClose") or price
        change = round(price - prev, 2) if price and prev else 0
        change_pct = round((change / prev) * 100, 2) if prev else 0

        return {
            "price": round(float(price), 2),
            "change": change,
            "change_pct": change_pct,
            "open": round(float(info.get("regularMarketOpen") or price), 2),
            "high": round(float(info.get("regularMarketDayHigh") or price), 2),
            "low": round(float(info.get("regularMarketDayLow") or price), 2),
            "prev_close": round(float(prev), 2),
            "volume": int(info.get("regularMarketVolume") or 0),
            "high_52w": round(float(info.get("fiftyTwoWeekHigh") or 0), 2),
            "low_52w": round(float(info.get("fiftyTwoWeekLow") or 0), 2),
            "market_cap": round(float(info.get("marketCap") or 0) / 10000000, 2),  # Cr
        }
    except Exception as e:
        print(f"[Market API] Error fetching {yf_symbol}: {e}")
        return None


# ── Simple in-memory cache ───────────────────────────────────
from datetime import datetime
_quote_cache = {}   # {yf_symbol: (timestamp, data)}
_CACHE_TTL = 120    # 2 minutes


def _get_cached_quote(yf_symbol: str) -> dict:
    """Get quote with caching."""
    now = datetime.now().timestamp()
    cached = _quote_cache.get(yf_symbol)
    if cached and (now - cached[0]) < _CACHE_TTL:
        return cached[1]
    data = _fetch_quote(yf_symbol)
    if data:
        _quote_cache[yf_symbol] = (now, data)
    return data


@market_bp.route("/live-quotes", methods=["POST"])
def live_quotes():
    """
    Fetch live quotes for a list of symbols.
    Request body: {"symbols": ["NIFTY 50", "SENSEX", "RELIANCE", ...]}
    Returns: {"quotes": {"NIFTY 50": {...}, "SENSEX": {...}, ...}}
    """
    data = request.get_json() or {}
    symbols = data.get("symbols", [])

    if not symbols or len(symbols) > 50:
        return jsonify({"error": "Provide 1-50 symbols"}), 400

    results = {}
    for name in symbols:
        yf_sym = _resolve_yf_symbol(name)
        quote = _get_cached_quote(yf_sym)
        if quote:
            results[name] = quote

    return jsonify({"quotes": results})


@market_bp.route("/ticker", methods=["GET"])
def ticker_data():
    """
    Return live ticker data for the scrolling ticker bar.
    Pre-defined list of key stocks/indices.
    """
    ticker_symbols = [
        "NIFTY 50", "SENSEX", "BANKNIFTY",
        "RELIANCE", "TCS", "HDFC BANK", "INFY", "ITC",
        "WIPRO", "SBIN", "BAJFINANCE", "TATAMOTORS"
    ]

    results = []
    for name in ticker_symbols:
        yf_sym = _resolve_yf_symbol(name)
        quote = _get_cached_quote(yf_sym)
        if quote:
            results.append({
                "name": name,
                "price": quote["price"],
                "change_pct": quote["change_pct"],
            })

    return jsonify({"ticker": results})
