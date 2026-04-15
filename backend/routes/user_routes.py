"""
User Routes – Profile view & update.
"""
from flask import Blueprint, request, jsonify, g
from models.user import find_by_id, update_profile

user_bp = Blueprint("user", __name__)


def _sanitize_user(user):
    """Remove sensitive fields and ensure dates are serializable."""
    user.pop("password_hash", None)
    for k in ("created_at", "updated_at"):
        val = user.get(k)
        if val and hasattr(val, "isoformat"):
            user[k] = val.isoformat()
        # If already a string, leave as-is
    return user


@user_bp.route("/profile", methods=["GET"])
def get_profile():
    from app import auth_required
    @auth_required
    def _inner():
        user = find_by_id(g.user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(_sanitize_user(user))
    return _inner()


@user_bp.route("/profile", methods=["PUT"])
def update_profile_route():
    from app import auth_required
    @auth_required
    def _inner():
        data = request.get_json()
        update_profile(g.user_id, data)
        user = find_by_id(g.user_id)
        return jsonify({"message": "Profile updated", "user": _sanitize_user(user)})
    return _inner()
