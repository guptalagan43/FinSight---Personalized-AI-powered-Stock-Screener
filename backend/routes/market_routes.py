"""
Market Routes – Live market data endpoints.
Uses the shared YFinanceDataProvider for memory efficiency.
"""
from flask import Blueprint, request, jsonify
from services.data_provider_service import get_data_provider

market_bp = Blueprint("market", __name__)

# ── Symbol mapping for Yahoo Finance ─────────────────────────
SYMBOL_MAP = {
    "NIFTY 50": "NIFTY_50", "SENSEX": "SENSEX", "BANKNIFTY": "NIFTY_BANK",
    "NIFTY IT": "NIFTY_IT", "NIFTY MIDCAP 100": "NIFTY_MIDCAP_100",
    "NIFTY SMALLCAP": "NIFTY_SMALLCAP_100", "FINNIFTY": "NIFTY_FIN_SERVICE",
    "NIFTY AUTO": "NIFTY_AUTO", "NIFTY METAL": "NIFTY_METAL",
    "NIFTY PHARMA": "NIFTY_PHARMA", "NIFTY FMCG": "NIFTY_FMCG",
    "NIFTY REALTY": "NIFTY_REALTY", "INDIA VIX": "INDIA_VIX",
    "RELIANCE": "RELIANCE", "TCS": "TCS",
    "HDFC BANK": "HDFCBANK", "INFY": "INFY", "INFOSYS": "INFY",
    "ITC": "ITC", "L&T": "LT", "MARUTI": "MARUTI",
    "TATA MOTORS": "TATAMOTORS", "SBI": "SBIN",
    "ICICI BANK": "ICICIBANK", "WIPRO": "WIPRO",
    "BAJFINANCE": "BAJFINANCE", "SUNPHARMA": "SUNPHARMA",
    "AXISBANK": "AXISBANK", "KOTAKBANK": "KOTAKBANK",
    "BHARTIARTL": "BHARTIARTL", "HINDUNILVR": "HINDUNILVR",
    "ASIANPAINT": "ASIANPAINT", "DRREDDY": "DRREDDY",
    "ONGC": "ONGC", "POWERGRID": "POWERGRID", "NTPC": "NTPC",
    "COALINDIA": "COALINDIA", "TITAN": "TITAN",
    "ADANIENT": "ADANIENT", "ADANIPORTS": "ADANIPORTS",
    "TECHM": "TECHM", "HCLTECH": "HCLTECH",
    "ULTRACEMCO": "ULTRACEMCO", "JSWSTEEL": "JSWSTEEL",
    "TATASTEEL": "TATASTEEL", "M&M": "M&M",
    "CIPLA": "CIPLA", "DIVISLAB": "DIVISLAB",
    "EICHERMOT": "EICHERMOT", "BPCL": "BPCL",
    "HEROMOTOCO": "HEROMOTOCO", "NESTLEIND": "NESTLEIND",
    "GRASIM": "GRASIM", "APOLLOHOSP": "APOLLOHOSP",
    "SBILIFE": "SBILIFE", "BAJAJFINSV": "BAJAJFINSV",
    "TATACONSUM": "TATACONSUM", "BRITANNIA": "BRITANNIA",
    "SUZLON": "SUZLON", "IREDA": "IREDA", "NHPC": "NHPC",
    "IRFC": "IRFC", "ZOMATO": "ZOMATO", "PAYTM": "PAYTM",
    "JIOFIN": "JIOFIN", "JIOFINANCE": "JIOFIN",
    "TATA TECH": "TATATECH", "CDSL": "CDSL", "BSE": "BSE",
    "NIFTYBEES": "NIFTYBEES", "BANKBEES": "BANKBEES",
    "GOLDBEES": "GOLDBEES", "LIQUIDBEES": "LIQUIDBEES",
    "ITBEES": "ITBEES", "PHARMABEES": "PHARMABEES",
    "MON100": "MON100", "CPSEETF": "CPSEETF",
    "MID150BEES": "MID150BEES", "SILVERBEES": "SILVERBEES",
}


def _resolve_name(name: str) -> str:
    """Convert display name to internal symbol for the provider."""
    upper = name.strip().upper()
    return SYMBOL_MAP.get(upper, upper)


@market_bp.route("/live-quotes", methods=["POST"])
def live_quotes():
    """
    Fetch live quotes for a list of symbols.
    Request body: {"symbols": ["NIFTY 50", "SENSEX", "RELIANCE", ...]}
    """
    data = request.get_json() or {}
    symbols = data.get("symbols", [])

    if not symbols or len(symbols) > 50:
        return jsonify({"error": "Provide 1-50 symbols"}), 400

    provider = get_data_provider()
    results = {}
    for name in symbols:
        internal = _resolve_name(name)
        try:
            # Use _get_slim_quote for YFinance, get_quote for mock
            if hasattr(provider, '_get_slim_quote'):
                quote = provider._get_slim_quote(internal)
            else:
                q = provider.get_quote(internal)
                quote = {
                    "price": q["price"], "change": q["change"],
                    "change_pct": q["change_pct"],
                    "high_52w": 0, "low_52w": 0, "market_cap": 0,
                }
            if quote and quote.get("price"):
                results[name] = quote
        except Exception as e:
            print(f"[Market API] Error for {name}: {e}")

    return jsonify({"quotes": results})


@market_bp.route("/ticker", methods=["GET"])
def ticker_data():
    """Return live ticker data for the scrolling ticker bar."""
    ticker_symbols = [
        "NIFTY 50", "SENSEX", "BANKNIFTY",
        "RELIANCE", "TCS", "HDFC BANK", "INFY", "ITC",
        "WIPRO", "SBIN", "BAJFINANCE", "TATAMOTORS"
    ]

    provider = get_data_provider()
    results = []
    for name in ticker_symbols:
        internal = _resolve_name(name)
        try:
            if hasattr(provider, '_get_slim_quote'):
                quote = provider._get_slim_quote(internal)
            else:
                q = provider.get_quote(internal)
                quote = {"price": q["price"], "change_pct": q["change_pct"]}
            if quote and quote.get("price"):
                results.append({
                    "name": name,
                    "price": quote["price"],
                    "change_pct": quote.get("change_pct", 0),
                })
        except Exception:
            pass

    return jsonify({"ticker": results})
