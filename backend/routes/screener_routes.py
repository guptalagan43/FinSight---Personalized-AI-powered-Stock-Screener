"""
FinSight Routes – Predefined, custom, run.
"""
from flask import Blueprint, request, jsonify, g
from models.screener import get_predefined, get_user_screeners, create_screener, run_screener

screener_bp = Blueprint("screeners", __name__)


@screener_bp.route("/predefined", methods=["GET"])
def predefined():
    screens = get_predefined()
    return jsonify(screens)


@screener_bp.route("/custom", methods=["GET"])
def custom_list():
    from app import auth_required
    @auth_required
    def _inner():
        screens = get_user_screeners(g.user_id)
        return jsonify(screens)
    return _inner()


@screener_bp.route("/custom", methods=["POST"])
def custom_create():
    from app import auth_required
    @auth_required
    def _inner():
        data = request.get_json()
        name = data.get("name", "Untitled Screen")
        description = data.get("description", "")
        definition_json = data.get("definition_json", "{}")
        if isinstance(definition_json, dict):
            import json
            definition_json = json.dumps(definition_json)
        result = create_screener(g.user_id, name, description, definition_json)
        return jsonify(result), 201
    return _inner()


@screener_bp.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    definition_json = data.get("definition_json", "{}")
    if isinstance(definition_json, dict):
        import json
        definition_json = json.dumps(definition_json)
    results = run_screener(definition_json)
    # Convert Decimals
    for row in results:
        for k, v in row.items():
            if hasattr(v, "as_integer_ratio"):
                row[k] = float(v)
    return jsonify(results)
