"""
Instrument Routes – Search, detail, chart, fundamentals.
"""
from flask import Blueprint, request, jsonify
from models.instrument import search_instruments, get_instrument, get_fundamentals, get_all_instruments, get_instruments_by_type
from services.data_provider_service import get_data_provider

instrument_bp = Blueprint("instruments", __name__)


@instrument_bp.route("/search", methods=["GET"])
def search():
    q = request.args.get("q", "").strip()
    if len(q) < 1:
        return jsonify([])
    results = search_instruments(q)
    # Serialize decimals
    for r in results:
        for k, v in r.items():
            if hasattr(v, "as_integer_ratio"):  # Decimal
                r[k] = float(v)
    # Overlay live prices
    try:
        provider = get_data_provider()
        if hasattr(provider, '_yf'):
            for r in results:
                try:
                    quote = provider.get_quote(r["symbol"])
                    if quote and quote.get("price"):
                        r["current_price"] = quote["price"]
                        r["day_change_pct"] = quote["change_pct"]
                except Exception:
                    pass
    except Exception:
        pass
    return jsonify(results)


@instrument_bp.route("/all", methods=["GET"])
def all_instruments():
    results = get_all_instruments()
    for r in results:
        for k, v in r.items():
            if hasattr(v, "as_integer_ratio"):
                r[k] = float(v)
    return jsonify(results)

@instrument_bp.route("/by-type", methods=["GET"])
def by_type():
    inst_type = request.args.get("type", "stock")
    sector = request.args.get("sector")
    sort_by = request.args.get("sort_by")
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 50))
    except ValueError:
        page = 1
        limit = 50
        
    result = get_instruments_by_type(inst_type, sector, sort_by, page, limit)
    
    # Serialize decimals
    for r in result["items"]:
        for k, v in r.items():
            if hasattr(v, "as_integer_ratio"):
                r[k] = float(v)
                
    return jsonify(result)


@instrument_bp.route("/<int:instrument_id>", methods=["GET"])
def detail(instrument_id):
    inst = get_instrument(instrument_id)
    if not inst:
        return jsonify({"error": "Instrument not found"}), 404
    # Convert Decimals and dates
    for k, v in inst.items():
        if hasattr(v, "as_integer_ratio"):
            inst[k] = float(v)
        elif hasattr(v, "isoformat"):
            inst[k] = v.isoformat()

    # Overlay live quote data from yfinance (if available)
    try:
        provider = get_data_provider()
        if hasattr(provider, '_yf'):  # YFinanceDataProvider
            quote = provider.get_quote(inst["symbol"])
            if quote and quote.get("price"):
                inst["current_price"] = quote["price"]
                inst["day_change"] = quote["change"]
                inst["day_change_pct"] = quote["change_pct"]
                inst["prev_close"] = quote["prev_close"]
                inst["volume"] = quote.get("volume", inst.get("volume"))
            # Also fetch 52w high/low and market cap from info
            info = provider._get_info(inst["symbol"])
            if info:
                if info.get("fiftyTwoWeekHigh"):
                    inst["high_52w"] = round(float(info["fiftyTwoWeekHigh"]), 2)
                if info.get("fiftyTwoWeekLow"):
                    inst["low_52w"] = round(float(info["fiftyTwoWeekLow"]), 2)
                if info.get("marketCap"):
                    inst["market_cap"] = round(float(info["marketCap"]) / 10000000, 2)  # Convert to Cr
    except Exception as e:
        print(f"[Instrument Detail] Live quote overlay failed for {inst.get('symbol')}: {e}")

    return jsonify(inst)


@instrument_bp.route("/<int:instrument_id>/chart", methods=["GET"])
def chart_data(instrument_id):
    inst = get_instrument(instrument_id)
    if not inst:
        return jsonify({"error": "Instrument not found"}), 404
    range_type = request.args.get("range", "1M")
    provider = get_data_provider()
    data = provider.get_historical_prices(inst["symbol"], range_type)
    return jsonify({"symbol": inst["symbol"], "range": range_type, "data": data})


@instrument_bp.route("/<int:instrument_id>/fundamentals", methods=["GET"])
def fundamentals(instrument_id):
    rows = get_fundamentals(instrument_id)
    # Convert Decimals
    for row in rows:
        for k, v in row.items():
            if hasattr(v, "as_integer_ratio"):
                row[k] = float(v)
    return jsonify(rows)
