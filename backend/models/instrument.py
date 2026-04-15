"""
Instrument data-access functions.
Uses PostgreSQL when available, falls back to in-memory store.
"""
from flask import g
from models import get_cursor as _cursor, use_db
from models import memory_store as mem


def search_instruments(query: str, limit: int = 20):
    """Search instruments by name or symbol (case-insensitive)."""
    if not use_db():
        return mem.instrument_search(query, limit)
    cur = _cursor()
    pattern = f"%{query}%"
    cur.execute(
        """SELECT id, symbol, name, type, exchange, sector, current_price,
                  day_change, day_change_pct
           FROM instruments
           WHERE LOWER(name) LIKE LOWER(%s)
              OR LOWER(symbol) LIKE LOWER(%s)
           ORDER BY market_cap DESC NULLS LAST
           LIMIT %s""",
        (pattern, pattern, limit),
    )
    return [dict(r) for r in cur.fetchall()]


def get_all_instruments():
    if not use_db():
        return mem.instrument_get_all()
    cur = _cursor()
    cur.execute(
        """SELECT id, symbol, name, type, exchange, sector, industry,
                  market_cap, current_price, day_change, day_change_pct,
                  high_52w, low_52w
           FROM instruments
           WHERE is_active = TRUE
           ORDER BY market_cap DESC NULLS LAST"""
    )
    return [dict(r) for r in cur.fetchall()]

def get_instruments_by_type(inst_type: str, sector: str = None, sort_by: str = None, page: int = 1, limit: int = 50):
    if not use_db():
        return mem.instrument_get_by_type(inst_type, sector, sort_by, page, limit)
    
    cur = _cursor()
    offset = (page - 1) * limit
    
    query = """
        SELECT id, symbol, name, type, exchange, sector, industry,
               market_cap, current_price, day_change, day_change_pct,
               high_52w, low_52w
        FROM instruments
        WHERE type = %s AND is_active = TRUE
    """
    params = [inst_type]
    
    if sector:
        query += " AND (LOWER(sector) = LOWER(%s) OR LOWER(industry) = LOWER(%s))"
        params.extend([sector, sector])
        
    if sort_by == 'price_desc':
        query += " ORDER BY current_price DESC NULLS LAST"
    elif sort_by == 'price_asc':
        query += " ORDER BY current_price ASC NULLS LAST"
    elif sort_by == 'change_desc':
        query += " ORDER BY day_change_pct DESC NULLS LAST"
    elif sort_by == 'change_asc':
        query += " ORDER BY day_change_pct ASC NULLS LAST"
    elif sort_by == 'name_asc':
        query += " ORDER BY name ASC NULLS LAST"
    elif sort_by == 'name_desc':
        query += " ORDER BY name DESC NULLS LAST"
    else:
        query += " ORDER BY market_cap DESC NULLS LAST"
        
    # Count total
    count_query = query.replace("SELECT id, symbol, name, type, exchange, sector, industry,\n               market_cap, current_price, day_change, day_change_pct,\n               high_52w, low_52w", "SELECT COUNT(*)")
    count_query = count_query.split(" ORDER BY")[0]
    
    cur.execute(count_query, params)
    total = cur.fetchone()[0]
    
    # Get items
    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    
    cur.execute(query, params)
    items = [dict(r) for r in cur.fetchall()]
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit
    }


def get_instrument(instrument_id: int):
    if not use_db():
        return mem.instrument_get(instrument_id)
    cur = _cursor()
    cur.execute("SELECT * FROM instruments WHERE id = %s", (instrument_id,))
    row = cur.fetchone()
    return dict(row) if row else None


def get_fundamentals(instrument_id: int):
    if not use_db():
        return mem.instrument_get_fundamentals(instrument_id)
    cur = _cursor()
    cur.execute(
        """SELECT * FROM instrument_fundamentals
           WHERE instrument_id = %s ORDER BY fiscal_year DESC""",
        (instrument_id,),
    )
    return [dict(r) for r in cur.fetchall()]


def get_instruments_by_sector(sector: str):
    if not use_db():
        return mem.instrument_get_by_sector(sector)
    cur = _cursor()
    cur.execute(
        """SELECT i.id, i.symbol, i.name, i.type, i.exchange, i.sector,
                  i.industry, i.market_cap, i.current_price,
                  i.day_change, i.day_change_pct, i.high_52w, i.low_52w
           FROM instruments i
           WHERE LOWER(i.sector) = LOWER(%s)
           ORDER BY i.market_cap DESC NULLS LAST""",
        (sector,),
    )
    return [dict(r) for r in cur.fetchall()]


def get_sectors():
    """Return distinct sectors with instrument count and avg stats."""
    if not use_db():
        return mem.instrument_get_sectors()
    cur = _cursor()
    cur.execute(
        """SELECT sector, COUNT(*) as instrument_count,
                  ROUND(AVG(day_change_pct)::numeric, 2) as avg_day_change_pct
           FROM instruments
           WHERE sector IS NOT NULL
           GROUP BY sector
           ORDER BY sector"""
    )
    return [dict(r) for r in cur.fetchall()]
