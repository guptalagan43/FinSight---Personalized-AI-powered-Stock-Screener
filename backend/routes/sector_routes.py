"""
Sector Routes – List sectors, instruments by sector.
"""
from flask import Blueprint, request, jsonify
from models.instrument import get_sectors, get_instruments_by_sector

sector_bp = Blueprint("sectors", __name__)


@sector_bp.route("/", methods=["GET"])
def list_sectors():
    sectors = get_sectors()
    for s in sectors:
        for k, v in s.items():
            if hasattr(v, "as_integer_ratio"):
                s[k] = float(v)
    return jsonify(sectors)


@sector_bp.route("/<path:sector_name>/instruments", methods=["GET"])
def sector_instruments(sector_name):
    instruments = get_instruments_by_sector(sector_name)
    for inst in instruments:
        for k, v in inst.items():
            if hasattr(v, "as_integer_ratio"):
                inst[k] = float(v)
    return jsonify(instruments)
