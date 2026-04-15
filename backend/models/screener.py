"""
FinSight data-access functions.
Uses PostgreSQL when available, falls back to in-memory store.
"""
from flask import g
from models import get_cursor as _cursor, use_db
from models import memory_store as mem
import json


def get_predefined():
    if not use_db():
        return mem.finsight_get_predefined()
    cur = _cursor()
    cur.execute(
        "SELECT id, name, description, definition_json FROM screeners WHERE user_id IS NULL ORDER BY id"
    )
    return [dict(r) for r in cur.fetchall()]


def get_user_screeners(user_id: int):
    if not use_db():
        return mem.finsight_get_user(user_id)
    cur = _cursor()
    cur.execute(
        "SELECT id, name, description, definition_json FROM screeners WHERE user_id = %s ORDER BY id",
        (user_id,),
    )
    return [dict(r) for r in cur.fetchall()]


def create_screener(user_id: int, name: str, description: str, definition_json: str):
    if not use_db():
        return mem.finsight_create(user_id, name, description, definition_json)
    cur = _cursor()
    cur.execute(
        """INSERT INTO screeners (user_id, name, description, definition_json)
           VALUES (%s, %s, %s, %s) RETURNING id, name""",
        (user_id, name, description, definition_json),
    )
    return dict(cur.fetchone())


def run_screener(definition_json: str):
    """
    Execute a screener against instrument_fundamentals.
    definition_json: {"conditions":[{"field":"roe","op":">","value":15}], "logic":"AND"}
    """
    if not use_db():
        return mem.finsight_run(definition_json)
    defn = json.loads(definition_json) if isinstance(definition_json, str) else definition_json
    conditions = defn.get("conditions", [])
    logic = defn.get("logic", "AND").upper()

    ALLOWED_FIELDS = {
        "revenue", "net_profit", "eps", "debt", "equity", "roe", "roce",
        "pe", "pb", "debt_to_equity", "promoter_holding", "net_profit_margin",
        "sales_growth", "profit_growth", "market_cap",
    }
    ALLOWED_OPS = {"<", ">", "<=", ">=", "=", "!="}

    where_clauses = []
    values = []

    for cond in conditions:
        field = cond.get("field", "")
        op = cond.get("op", "")
        val = cond.get("value")

        if field not in ALLOWED_FIELDS or op not in ALLOWED_OPS:
            continue

        if field == "market_cap":
            where_clauses.append(f"i.market_cap {op} %s")
        else:
            where_clauses.append(f"f.{field} {op} %s")
        values.append(val)

    if not where_clauses:
        where_sql = "TRUE"
    else:
        joiner = f" {logic} "
        where_sql = joiner.join(where_clauses)

    cur = _cursor()
    cur.execute(
        f"""SELECT DISTINCT i.id, i.symbol, i.name, i.sector, i.industry,
                   i.market_cap, i.current_price, i.day_change_pct,
                   f.pe, f.pb, f.roe, f.roce, f.debt_to_equity,
                   f.net_profit_margin, f.sales_growth, f.profit_growth
            FROM instruments i
            JOIN instrument_fundamentals f ON f.instrument_id = i.id
            WHERE f.fiscal_year = (
                SELECT MAX(f2.fiscal_year) FROM instrument_fundamentals f2
                WHERE f2.instrument_id = i.id
            )
            AND ({where_sql})
            ORDER BY i.market_cap DESC NULLS LAST
            LIMIT 50""",
        values,
    )
    return [dict(r) for r in cur.fetchall()]
