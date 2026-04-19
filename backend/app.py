"""
FinSight – Flask Application Entry Point
Registers all blueprints, sets up CORS, DB helpers, and serves frontend.
"""
import os
import functools
from datetime import datetime, timedelta, timezone

import jwt
from flask import Flask, request, jsonify, send_from_directory, g
from flask_cors import CORS

from config import Config

# ── Optional PostgreSQL import ───────────────────────────────
try:
    import psycopg2
    import psycopg2.extras
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("[WARN] psycopg2 not installed - database features disabled.")
    print("       Install with: pip install psycopg2-binary  (Python <=3.12)")
    print("       or:           pip install psycopg[binary]  (Python 3.13+)")

# ── App factory ──────────────────────────────────────────────
app = Flask(__name__, static_folder=None)
app.config.from_object(Config)
CORS(app, resources={r"/api/*": {"origins": "*"}})


# ── Database helpers ─────────────────────────────────────────
def get_db():
    """Return a per-request database connection (stored on Flask `g`)."""
    if not DB_AVAILABLE:
        raise RuntimeError("Database not available – psycopg2 is not installed")
    if "db" not in g:
        g.db = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
        )
        g.db.autocommit = False
    return g.db


def get_cursor():
    """Return a dict cursor for the current request."""
    return get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        if exc:
            db.rollback()
        else:
            db.commit()
        db.close()


# ── JWT helpers ──────────────────────────────────────────────
def create_token(user_id: int, role: str) -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=Config.JWT_EXPIRY_HOURS),
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")


def decode_token(token: str) -> dict:
    return jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])


def auth_required(f):
    """Decorator: extracts and validates JWT, sets g.user_id and g.user_role."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        try:
            payload = decode_token(auth_header[7:])
            g.user_id = payload["user_id"]
            g.user_role = payload["role"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    """Decorator: must be called after @auth_required."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if getattr(g, "user_role", None) != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return wrapper


# ── Register blueprints ─────────────────────────────────────
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.instrument_routes import instrument_bp
from routes.screener_routes import screener_bp
from routes.sector_routes import sector_bp
from routes.chat_routes import chat_bp
from routes.admin_routes import admin_bp
from routes.watchlist_routes import watchlist_bp, portfolio_bp
from routes.news_routes import news_bp
from routes.market_routes import market_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(user_bp, url_prefix="/api/user")
app.register_blueprint(instrument_bp, url_prefix="/api/instruments")
app.register_blueprint(screener_bp, url_prefix="/api/screeners")
app.register_blueprint(sector_bp, url_prefix="/api/sectors")
app.register_blueprint(chat_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(watchlist_bp, url_prefix="/api/watchlists")
app.register_blueprint(portfolio_bp, url_prefix="/api/portfolio")
app.register_blueprint(news_bp, url_prefix="/api/news")
app.register_blueprint(market_bp, url_prefix="/api/market")


# ── Serve frontend static files ──────────────────────────────
FRONTEND_DIR = os.path.abspath(Config.FRONTEND_DIR)


@app.route("/")
def serve_index():
    return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), "index.html")


@app.route("/pages/<path:filename>")
def serve_page(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), filename)


@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "static"), filename)


# ── Health check ─────────────────────────────────────────────
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "app": "FinSight"})


# ── Run ──────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
