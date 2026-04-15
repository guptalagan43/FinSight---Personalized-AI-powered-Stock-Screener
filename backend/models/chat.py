"""
Chat log data-access functions.
Uses PostgreSQL when available, falls back to in-memory store.
"""
from flask import g
from models import get_cursor as _cursor, use_db
from models import memory_store as mem


def log_chat(user_id: int, instrument_id, user_message: str, ai_response_summary: str):
    if not use_db():
        return mem.chat_log(user_id, instrument_id, user_message, ai_response_summary)
    cur = _cursor()
    cur.execute(
        """INSERT INTO chat_logs (user_id, instrument_id, user_message, ai_response_summary)
           VALUES (%s, %s, %s, %s) RETURNING id, created_at""",
        (user_id, instrument_id, user_message, ai_response_summary),
    )
    return dict(cur.fetchone())


def get_chat_history(user_id: int, instrument_id=None, limit: int = 50):
    if not use_db():
        return mem.chat_get_history(user_id, instrument_id, limit)
    cur = _cursor()
    if instrument_id:
        cur.execute(
            """SELECT id, user_message, ai_response_summary, created_at
               FROM chat_logs
               WHERE user_id = %s AND instrument_id = %s
               ORDER BY created_at DESC LIMIT %s""",
            (user_id, instrument_id, limit),
        )
    else:
        cur.execute(
            """SELECT id, instrument_id, user_message, ai_response_summary, created_at
               FROM chat_logs
               WHERE user_id = %s
               ORDER BY created_at DESC LIMIT %s""",
            (user_id, limit),
        )
    return [dict(r) for r in cur.fetchall()]
