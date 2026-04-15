"""
Admin Routes – User management, settings.
"""
from flask import Blueprint, request, jsonify, g
from models.user import list_users, toggle_active

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/users", methods=["GET"])
def get_users():
    from app import auth_required, admin_required
    @auth_required
    @admin_required
    def _inner():
        users = list_users()
        for u in users:
            for k, v in u.items():
                if hasattr(v, "isoformat"):
                    u[k] = v.isoformat()
        return jsonify(users)
    return _inner()


@admin_bp.route("/users/<int:user_id>/toggle", methods=["PUT"])
def toggle_user(user_id):
    from app import auth_required, admin_required
    @auth_required
    @admin_required
    def _inner():
        result = toggle_active(user_id)
        if result is None:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"user_id": user_id, "is_active": result["is_active"]})
    return _inner()
