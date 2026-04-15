"""
Watchlist & Portfolio Routes – CRUD for watchlists and simulated portfolio.
"""
from flask import Blueprint, request, jsonify, g
from models.portfolio import (
    get_watchlists, create_watchlist, add_watchlist_item,
    remove_watchlist_item, get_positions, add_position,
)

watchlist_bp = Blueprint("watchlists", __name__)


@watchlist_bp.route("/", methods=["GET"])
def list_watchlists():
    from app import auth_required
    @auth_required
    def _inner():
        wls = get_watchlists(g.user_id)
        for wl in wls:
            for k, v in wl.items():
                if hasattr(v, "isoformat"):
                    wl[k] = v.isoformat()
            for item in wl.get("items", []):
                for k, v in item.items():
                    if hasattr(v, "as_integer_ratio"):
                        item[k] = float(v)
        return jsonify(wls)
    return _inner()


@watchlist_bp.route("/", methods=["POST"])
def create():
    from app import auth_required
    @auth_required
    def _inner():
        data = request.get_json()
        name = data.get("name", "My Watchlist")
        wl = create_watchlist(g.user_id, name)
        return jsonify(wl), 201
    return _inner()


@watchlist_bp.route("/<int:watchlist_id>/items", methods=["POST"])
def add_item(watchlist_id):
    from app import auth_required
    @auth_required
    def _inner():
        data = request.get_json()
        instrument_id = data.get("instrument_id")
        if not instrument_id:
            return jsonify({"error": "instrument_id is required"}), 400
        result = add_watchlist_item(watchlist_id, instrument_id)
        return jsonify(result), 201
    return _inner()


@watchlist_bp.route("/<int:watchlist_id>/items/<int:item_id>", methods=["DELETE"])
def remove_item(watchlist_id, item_id):
    from app import auth_required
    @auth_required
    def _inner():
        remove_watchlist_item(watchlist_id, item_id)
        return jsonify({"message": "Item removed"})
    return _inner()


# ── Portfolio ────────────────────────────────────────────────
portfolio_bp = Blueprint("portfolio", __name__)


@portfolio_bp.route("/", methods=["GET"])
def list_positions():
    from app import auth_required
    @auth_required
    def _inner():
        positions = get_positions(g.user_id)
        for p in positions:
            for k, v in p.items():
                if hasattr(v, "as_integer_ratio"):
                    p[k] = float(v)
                elif hasattr(v, "isoformat"):
                    p[k] = v.isoformat()
        return jsonify(positions)
    return _inner()


@portfolio_bp.route("/positions", methods=["POST"])
def add():
    from app import auth_required
    @auth_required
    def _inner():
        data = request.get_json()
        result = add_position(
            g.user_id,
            data["instrument_id"],
            data["quantity"],
            data["buy_price"],
            data["buy_date"],
        )
        return jsonify(result), 201
    return _inner()
