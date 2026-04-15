"""
Chat Routes – AI chatbot endpoints with full personalization context.
Gathers user profile, portfolio, watchlists, instrument data, and sectors
to deliver highly personalized responses.
"""
from flask import Blueprint, request, jsonify, g
from models.chat import log_chat, get_chat_history
from models.instrument import get_instrument, get_fundamentals, search_instruments, get_sectors
from models.user import find_by_id
from models.portfolio import get_watchlists, get_positions
from services.chatbot_service import get_chatbot_service

chat_bp = Blueprint("chat", __name__)


def _build_full_context(user_id, instrument_id=None, user_message=""):
    """Gather ALL available context for personalized responses."""
    # ── Full user profile ──
    user = find_by_id(user_id)
    user_profile = {
        "name": user.get("name", ""),
        "email": user.get("email", ""),
        "age": user.get("age"),
        "country": user.get("country", "India"),
        "risk_profile": user.get("risk_profile", "Moderate"),
        "experience_level": user.get("experience_level", "Beginner"),
        "goals": user.get("goals", ""),
        "monthly_investment_capacity": user.get("monthly_investment_capacity"),
        "yearly_investment_capacity": user.get("yearly_investment_capacity"),
        "income_range": user.get("income_range"),
        "occupation": user.get("occupation", ""),
        "gender": user.get("gender", ""),
        "marital_status": user.get("marital_status", ""),
        "dob": user.get("dob", ""),
    }

    # ── Instrument data (if on detail page or mentioned in message) ──
    instrument_data = {}
    fundamentals = None

    if instrument_id:
        inst = get_instrument(instrument_id)
        if inst:
            instrument_data = {
                k: (float(v) if hasattr(v, "as_integer_ratio") else v)
                for k, v in inst.items()
            }
            fund_rows = get_fundamentals(instrument_id)
            if fund_rows:
                latest = fund_rows[0]
                fundamentals = {
                    k: (float(v) if hasattr(v, "as_integer_ratio") else v)
                    for k, v in latest.items()
                }
                instrument_data.update(fundamentals)

    # If no instrument from page, try to detect stock mention in message
    if not instrument_data and user_message:
        from services.chatbot_service import extract_stock_mention
        # Get a subset of popular instruments for matching
        try:
            all_instruments = search_instruments("", limit=500)
        except Exception:
            all_instruments = []
        mentioned = extract_stock_mention(user_message, all_instruments)
        if mentioned:
            inst_id = mentioned.get("id")
            instrument_data = {
                k: (float(v) if hasattr(v, "as_integer_ratio") else v)
                for k, v in mentioned.items()
            }
            fund_rows = get_fundamentals(inst_id)
            if fund_rows:
                latest = fund_rows[0]
                fundamentals = {
                    k: (float(v) if hasattr(v, "as_integer_ratio") else v)
                    for k, v in latest.items()
                }
                instrument_data.update(fundamentals)

    # ── Portfolio positions ──
    positions = []
    try:
        raw_positions = get_positions(user_id)
        for p in raw_positions:
            positions.append({
                k: (float(v) if hasattr(v, "as_integer_ratio") else
                    v.isoformat() if hasattr(v, "isoformat") else v)
                for k, v in p.items()
            })
    except Exception:
        pass

    # ── Watchlists ──
    watchlists = []
    try:
        raw_watchlists = get_watchlists(user_id)
        for wl in raw_watchlists:
            clean_wl = {}
            for k, v in wl.items():
                if k == "items":
                    clean_wl["items"] = [
                        {ik: (float(iv) if hasattr(iv, "as_integer_ratio") else iv)
                         for ik, iv in item.items()}
                        for item in v
                    ]
                elif hasattr(v, "isoformat"):
                    clean_wl[k] = v.isoformat()
                else:
                    clean_wl[k] = v
            watchlists.append(clean_wl)
    except Exception:
        pass

    # ── Sectors overview ──
    sectors = []
    try:
        raw_sectors = get_sectors()
        for s in raw_sectors:
            sectors.append({
                k: (float(v) if hasattr(v, "as_integer_ratio") else v)
                for k, v in s.items()
            })
    except Exception:
        pass

    # ── Chat history (last 5 for context) ──
    history = []
    try:
        raw_history = get_chat_history(user_id, limit=5)
        for h in raw_history:
            history.append({
                k: (v.isoformat() if hasattr(v, "isoformat") else v)
                for k, v in h.items()
            })
    except Exception:
        pass

    context = {
        "positions": positions,
        "watchlists": watchlists,
        "sectors": sectors,
        "history": history,
        "fundamentals": fundamentals,
    }

    return user_profile, instrument_data, context


@chat_bp.route("/chat", methods=["POST"])
def chat():
    from app import auth_required

    @auth_required
    def _inner():
        data = request.get_json()
        instrument_id = data.get("instrumentId")
        user_message = data.get("userMessage", "").strip()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Build full context
        user_profile, instrument_data, context = _build_full_context(
            g.user_id, instrument_id, user_message
        )

        # Get AI response
        chatbot = get_chatbot_service()
        response_text = chatbot.get_response(
            instrument_data, user_profile, user_message, context
        )

        # Log the conversation
        log_chat(
            user_id=g.user_id,
            instrument_id=instrument_id,
            user_message=user_message,
            ai_response_summary=response_text[:500],
        )

        return jsonify({"response": response_text})

    return _inner()


@chat_bp.route("/chat/suggestions", methods=["GET"])
def chat_suggestions():
    from app import auth_required

    @auth_required
    def _inner():
        instrument_id = request.args.get("instrumentId", type=int)

        user_profile, instrument_data, context = _build_full_context(
            g.user_id, instrument_id
        )

        chatbot = get_chatbot_service()
        suggestions = chatbot.get_suggestions(user_profile, instrument_data or None, context)

        return jsonify({"suggestions": suggestions})

    return _inner()


@chat_bp.route("/chat/history", methods=["GET"])
def chat_history():
    from app import auth_required

    @auth_required
    def _inner():
        instrument_id = request.args.get("instrumentId", type=int)
        limit = request.args.get("limit", 20, type=int)

        history = get_chat_history(g.user_id, instrument_id, limit)

        # Serialize dates
        result = []
        for h in history:
            entry = {}
            for k, v in h.items():
                if hasattr(v, "isoformat"):
                    entry[k] = v.isoformat()
                else:
                    entry[k] = v
            result.append(entry)

        return jsonify({"history": result})

    return _inner()
