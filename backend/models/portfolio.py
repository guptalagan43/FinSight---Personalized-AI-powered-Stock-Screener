"""
Watchlist & Portfolio data-access functions.
Uses PostgreSQL when available, falls back to in-memory store.
"""
from flask import g
from models import get_cursor as _cursor, use_db
from models import memory_store as mem


# ── Watchlists ───────────────────────────────────────────────
def get_watchlists(user_id: int):
    if not use_db():
        return mem.watchlist_get_all(user_id)
    cur = _cursor()
    cur.execute(
        "SELECT id, name, created_at FROM watchlists WHERE user_id = %s ORDER BY id",
        (user_id,),
    )
    watchlists = [dict(r) for r in cur.fetchall()]
    for wl in watchlists:
        cur.execute(
            """SELECT wi.id as item_id, i.id as instrument_id, i.symbol, i.name,
                      i.current_price, i.day_change, i.day_change_pct
               FROM watchlist_items wi
               JOIN instruments i ON i.id = wi.instrument_id
               WHERE wi.watchlist_id = %s ORDER BY wi.added_at""",
            (wl["id"],),
        )
        wl["items"] = [dict(r) for r in cur.fetchall()]
    return watchlists


def create_watchlist(user_id: int, name: str):
    if not use_db():
        return mem.watchlist_create(user_id, name)
    cur = _cursor()
    cur.execute(
        "INSERT INTO watchlists (user_id, name) VALUES (%s, %s) RETURNING id, name",
        (user_id, name),
    )
    return dict(cur.fetchone())


def add_watchlist_item(watchlist_id: int, instrument_id: int):
    if not use_db():
        return mem.watchlist_add_item(watchlist_id, instrument_id)
    cur = _cursor()
    cur.execute(
        """INSERT INTO watchlist_items (watchlist_id, instrument_id)
           VALUES (%s, %s) ON CONFLICT DO NOTHING RETURNING id""",
        (watchlist_id, instrument_id),
    )
    row = cur.fetchone()
    return dict(row) if row else {"message": "Already in watchlist"}


def remove_watchlist_item(watchlist_id: int, item_id: int):
    if not use_db():
        return mem.watchlist_remove_item(watchlist_id, item_id)
    cur = _cursor()
    cur.execute(
        "DELETE FROM watchlist_items WHERE watchlist_id = %s AND id = %s",
        (watchlist_id, item_id),
    )


# ── Portfolio positions ──────────────────────────────────────
def get_positions(user_id: int):
    if not use_db():
        return mem.portfolio_get_positions(user_id)
    cur = _cursor()
    cur.execute(
        """SELECT pp.id, pp.quantity, pp.buy_price, pp.buy_date,
                  i.id as instrument_id, i.symbol, i.name,
                  i.current_price,
                  ROUND((i.current_price - pp.buy_price) * pp.quantity, 2) as unrealized_pl,
                  CASE WHEN pp.buy_price > 0
                       THEN ROUND(((i.current_price - pp.buy_price) / pp.buy_price) * 100, 2)
                       ELSE 0 END as return_pct
           FROM portfolio_positions pp
           JOIN instruments i ON i.id = pp.instrument_id
           WHERE pp.user_id = %s ORDER BY pp.buy_date DESC""",
        (user_id,),
    )
    return [dict(r) for r in cur.fetchall()]


def add_position(user_id: int, instrument_id: int, quantity, buy_price, buy_date):
    if not use_db():
        return mem.portfolio_add_position(user_id, instrument_id, quantity, buy_price, buy_date)
    cur = _cursor()
    cur.execute(
        """INSERT INTO portfolio_positions (user_id, instrument_id, quantity, buy_price, buy_date)
           VALUES (%s, %s, %s, %s, %s) RETURNING id""",
        (user_id, instrument_id, quantity, buy_price, buy_date),
    )
    return dict(cur.fetchone())
