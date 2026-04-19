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
        if hasattr(provider, '_get_slim_quote'):
            for r in results:
                try:
                    slim = provider._get_slim_quote(r["symbol"])
                    if slim and slim.get("price"):
                        r["current_price"] = slim["price"]
                        r["day_change_pct"] = slim["change_pct"]
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
        if hasattr(provider, '_get_slim_quote'):
            slim = provider._get_slim_quote(inst["symbol"])
            if slim and slim.get("price"):
                inst["current_price"] = slim["price"]
                inst["day_change"] = slim["change"]
                inst["day_change_pct"] = slim["change_pct"]
                inst["prev_close"] = slim["prev_close"]
                inst["volume"] = slim.get("volume", inst.get("volume"))
                if slim.get("high_52w"):
                    inst["high_52w"] = slim["high_52w"]
                if slim.get("low_52w"):
                    inst["low_52w"] = slim["low_52w"]
                if slim.get("market_cap"):
                    inst["market_cap"] = slim["market_cap"]
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
