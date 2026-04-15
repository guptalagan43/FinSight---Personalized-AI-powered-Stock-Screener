"""
News Routes – Financial news feed with RSS/web scraping fallback.
Provides cached news items for the landing page.
"""
import time
import urllib.request
import json
import re
from flask import Blueprint, jsonify

news_bp = Blueprint("news", __name__)

# ── In-memory cache ──────────────────────────────────────────
_news_cache = {"data": [], "timestamp": 0}
CACHE_TTL = 300  # 5 minutes


def _fetch_google_news_rss():
    """Fetch financial news from Google News RSS feed."""
    try:
        url = "https://news.google.com/rss/search?q=indian+stock+market+NSE+BSE&hl=en-IN&gl=IN&ceid=IN:en"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) FinSight/1.0"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml_data = resp.read().decode("utf-8")

        # Simple XML parsing without external deps
        items = []
        for match in re.finditer(r"<item>(.*?)</item>", xml_data, re.DOTALL):
            item_xml = match.group(1)
            title_m = re.search(r"<title>(.*?)</title>", item_xml)
            link_m = re.search(r"<link>(.*?)</link>", item_xml)
            pubdate_m = re.search(r"<pubDate>(.*?)</pubDate>", item_xml)
            source_m = re.search(r"<source[^>]*>(.*?)</source>", item_xml)

            if title_m:
                title = title_m.group(1).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#39;", "'").replace("&quot;", '"')
                items.append({
                    "title": title,
                    "link": link_m.group(1) if link_m else "#",
                    "published": pubdate_m.group(1) if pubdate_m else "",
                    "source": source_m.group(1) if source_m else "Google News",
                })
            if len(items) >= 12:
                break
        return items
    except Exception as e:
        print(f"[News RSS Error] {e}")
        return []


def _get_fallback_news():
    """Static fallback news when RSS fails."""
    return [
        {"title": "RBI keeps repo rate unchanged at 6.5%, maintains stance", "source": "Economic Times", "link": "#", "published": "", "category": "Economy"},
        {"title": "Nifty crosses 22,500 mark for the first time, IT stocks lead rally", "source": "Moneycontrol", "link": "#", "published": "", "category": "Markets"},
        {"title": "TCS Q4 Results Preview: IT major expected to report steady growth", "source": "Business Standard", "link": "#", "published": "", "category": "Corporate"},
        {"title": "Federal Reserve signals potential rate cut amid inflation concerns", "source": "Reuters", "link": "#", "published": "", "category": "Global"},
        {"title": "Gold prices hit record high as geopolitical tensions rise", "source": "LiveMint", "link": "#", "published": "", "category": "Commodities"},
        {"title": "Foreign investors pour ₹15,000 crore into Indian equities this month", "source": "NDTV Profit", "link": "#", "published": "", "category": "Markets"},
    ]


def _categorize_news(title):
    """Auto-categorize news based on keywords."""
    title_lower = title.lower()
    if any(w in title_lower for w in ["rbi", "rate", "gdp", "inflation", "fiscal", "budget"]):
        return "Economy"
    if any(w in title_lower for w in ["nifty", "sensex", "market", "rally", "crash", "bull", "bear"]):
        return "Markets"
    if any(w in title_lower for w in ["result", "quarter", "earning", "revenue", "profit", "loss"]):
        return "Corporate"
    if any(w in title_lower for w in ["fed", "global", "us ", "china", "world", "crude"]):
        return "Global"
    if any(w in title_lower for w in ["gold", "silver", "oil", "commodity", "metal"]):
        return "Commodities"
    if any(w in title_lower for w in ["ipo", "listing", "subscribe"]):
        return "IPO"
    return "Markets"


@news_bp.route("/", methods=["GET"])
def get_news():
    """Return cached financial news items."""
    now = time.time()
    if now - _news_cache["timestamp"] < CACHE_TTL and _news_cache["data"]:
        return jsonify({"news": _news_cache["data"]})

    # Try fetching live news
    items = _fetch_google_news_rss()
    if not items:
        items = _get_fallback_news()

    # Add categories
    for item in items:
        if "category" not in item:
            item["category"] = _categorize_news(item.get("title", ""))

    _news_cache["data"] = items
    _news_cache["timestamp"] = now

    return jsonify({"news": items})
