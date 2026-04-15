"""
User & OTP data-access functions.
Uses PostgreSQL when available, falls back to in-memory store.
"""
from datetime import datetime, timedelta, timezone
from flask import g
from models import get_cursor as _cursor, use_db
from models import memory_store as mem


# ── User CRUD ────────────────────────────────────────────────
def create_user(email: str, password_hash: str, name: str) -> dict:
    if not use_db():
        return mem.user_create(email, password_hash, name)
    cur = _cursor()
    cur.execute(
        """INSERT INTO users (email, password_hash, name)
           VALUES (%s, %s, %s) RETURNING id, email, name, role""",
        (email, password_hash, name),
    )
    return dict(cur.fetchone())


def find_by_email(email: str):
    if not use_db():
        return mem.user_find_by_email(email)
    cur = _cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    row = cur.fetchone()
    return dict(row) if row else None


def find_by_id(user_id: int):
    if not use_db():
        return mem.user_find_by_id(user_id)
    cur = _cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    return dict(row) if row else None


def update_profile(user_id: int, data: dict):
    if not use_db():
        return mem.user_update_profile(user_id, data)
    allowed = [
        "name", "age", "country", "risk_profile", "experience_level",
        "monthly_investment_capacity", "yearly_investment_capacity", "goals",
        "dob", "mobile_number", "marital_status", "gender", "income_range", "occupation", "fathers_name"
    ]
    fields = {k: v for k, v in data.items() if k in allowed}
    if not fields:
        return
    set_clause = ", ".join(f"{k} = %s" for k in fields)
    values = list(fields.values()) + [user_id]
    cur = _cursor()
    cur.execute(
        f"UPDATE users SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
        values,
    )


def verify_email(user_id: int):
    if not use_db():
        return mem.user_verify_email(user_id)
    cur = _cursor()
    cur.execute("UPDATE users SET is_email_verified = TRUE WHERE id = %s", (user_id,))


def list_users():
    if not use_db():
        return mem.user_list_all()
    cur = _cursor()
    cur.execute(
        "SELECT id, email, name, role, is_active, is_email_verified, created_at FROM users ORDER BY id"
    )
    return [dict(r) for r in cur.fetchall()]


def toggle_active(user_id: int):
    if not use_db():
        return mem.user_toggle_active(user_id)
    cur = _cursor()
    cur.execute(
        "UPDATE users SET is_active = NOT is_active WHERE id = %s RETURNING is_active",
        (user_id,),
    )
    row = cur.fetchone()
    return dict(row) if row else None


def find_by_phone(phone: str):
    if not use_db():
        return mem.user_find_by_phone(phone)
    cur = _cursor()
    phone_clean = phone.strip().replace("+91", "").replace(" ", "").replace("-", "")
    cur.execute("SELECT * FROM users WHERE REPLACE(REPLACE(mobile_number, ' ', ''), '-', '') = %s", (phone_clean,))
    row = cur.fetchone()
    return dict(row) if row else None


def update_password(user_id: int, password_hash: str):
    if not use_db():
        return mem.user_update_password(user_id, password_hash)
    cur = _cursor()
    cur.execute(
        "UPDATE users SET password_hash = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
        (password_hash, user_id),
    )
    return True


# ── OTP helpers ──────────────────────────────────────────────
def create_otp(user_id: int, otp_code: str, expiry_minutes: int = 10):
    if not use_db():
        return mem.otp_create(user_id, otp_code, expiry_minutes)
    cur = _cursor()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
    cur.execute(
        """INSERT INTO otps (user_id, otp_code, expires_at)
           VALUES (%s, %s, %s)""",
        (user_id, otp_code, expires_at),
    )


def verify_otp(user_id: int, otp_code: str) -> bool:
    if not use_db():
        return mem.otp_verify(user_id, otp_code)
    cur = _cursor()
    cur.execute(
        """SELECT id FROM otps
           WHERE user_id = %s AND otp_code = %s
                 AND is_used = FALSE AND expires_at > NOW()
           ORDER BY created_at DESC LIMIT 1""",
        (user_id, otp_code),
    )
    row = cur.fetchone()
    if row:
        cur.execute("UPDATE otps SET is_used = TRUE WHERE id = %s", (row["id"],))
        return True
    return False
