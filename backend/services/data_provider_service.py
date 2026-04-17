"""
Data Provider Service – Fetches market quotes and historical prices.
Mock implementation provides static/random data for local development.
YFinance implementation provides real market data from Yahoo Finance.
"""
import random
import math
from datetime import datetime, timedelta
from config import Config


class MockDataProvider:
    """Returns simulated market data for development and demos."""

    def get_quote(self, symbol: str) -> dict:
        """Return a simulated real-time quote."""
        base_price = random.uniform(100, 5000)
        change = round(random.uniform(-50, 50), 2)
        return {
            "symbol": symbol,
            "price": round(base_price, 2),
            "change": change,
            "change_pct": round((change / base_price) * 100, 2),
            "open": round(base_price - random.uniform(-20, 20), 2),
            "high": round(base_price + abs(random.uniform(0, 30)), 2),
            "low": round(base_price - abs(random.uniform(0, 30)), 2),
            "prev_close": round(base_price - change, 2),
            "volume": random.randint(100000, 50000000),
            "timestamp": datetime.now().isoformat(),
        }

    def get_historical_prices(
        self, symbol: str, range_type: str = "1M"
    ) -> list[dict]:
        """Generate mock OHLCV historical data for chart display."""
        range_days = {
            "1D": 1, "1W": 7, "1M": 30, "3M": 90,
            "6M": 180, "1Y": 365, "5Y": 1825, "MAX": 3650,
        }
        days = range_days.get(range_type, 30)
        base = random.uniform(200, 3000)
        data = []
        current = base

        # Generate intraday points for 1D range
        if range_type == "1D":
            for i in range(78):  # ~6.5 hours of trading, 5-min intervals
                noise = random.gauss(0, base * 0.002)
                current += noise
                current = max(current, base * 0.95)
                data.append({
                    "timestamp": (
                        datetime.now().replace(hour=9, minute=15) + timedelta(minutes=i * 5)
                    ).isoformat(),
                    "open": round(current, 2),
                    "high": round(current + abs(random.gauss(0, 2)), 2),
                    "low": round(current - abs(random.gauss(0, 2)), 2),
                    "close": round(current + random.gauss(0, 1), 2),
                    "volume": random.randint(10000, 500000),
                })
        else:
            for i in range(days):
                noise = random.gauss(0, base * 0.015)
                trend = math.sin(i / 60) * base * 0.05  # gentle wave
                current = current + noise + trend * 0.01
                current = max(current, base * 0.5)
                o = round(current, 2)
                h = round(current + abs(random.gauss(0, base * 0.01)), 2)
                l = round(current - abs(random.gauss(0, base * 0.01)), 2)
                c = round(current + random.gauss(0, base * 0.005), 2)
                data.append({
                    "timestamp": (datetime.now() - timedelta(days=days - i)).strftime("%Y-%m-%d"),
                    "open": o, "high": h, "low": l, "close": c,
                    "volume": random.randint(100000, 10000000),
                })
        return data

    def get_fundamentals(self, symbol: str) -> dict:
        """Return mock fundamental data snapshot."""
        return {
            "symbol": symbol,
            "market_cap": round(random.uniform(10000, 2000000), 2),
            "pe": round(random.uniform(5, 80), 2),
            "pb": round(random.uniform(0.5, 30), 2),
            "roe": round(random.uniform(2, 50), 2),
            "roce": round(random.uniform(2, 55), 2),
            "debt_to_equity": round(random.uniform(0, 3), 2),
            "eps": round(random.uniform(1, 200), 2),
            "dividend_yield": round(random.uniform(0, 8), 2),
        }


# ── Yahoo Finance Real Data Provider ─────────────────────────

class YFinanceDataProvider:
    """Fetches real market data from Yahoo Finance via the yfinance library."""

    def __init__(self):
        import yfinance as yf
        self._yf = yf
        # Simple in-memory cache: {symbol: (timestamp, info_dict)}
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes

    def _resolve_symbol(self, symbol: str) -> str:
        """
        Ensure the symbol is Yahoo Finance compatible.
        Indian NSE stocks need a '.NS' suffix (e.g., RELIANCE -> RELIANCE.NS).
        Symbols that already contain a dot (e.g., AAPL, RELIANCE.NS) are left as-is.
        """
        if not symbol:
            return symbol
        if "." in symbol:
            return symbol
        # Try the plain symbol first; if it looks like an Indian stock we add .NS
        return f"{symbol}.NS"

    def _get_info(self, symbol: str) -> dict:
        """
        Get ticker info with simple TTL caching to avoid redundant API calls.
        """
        now = datetime.now().timestamp()
        cached = self._cache.get(symbol)
        if cached and (now - cached[0]) < self._cache_ttl:
            return cached[1]

        try:
            ticker = self._yf.Ticker(self._resolve_symbol(symbol))
            info = ticker.info or {}
            self._cache[symbol] = (now, info)
            return info
        except Exception as e:
            print(f"[YFinance] Error fetching info for {symbol}: {e}")
            return {}

    def get_quote(self, symbol: str) -> dict:
        """Return a real-time quote from Yahoo Finance."""
        info = self._get_info(symbol)
        if not info or info.get("trailingPegRatio") is None and info.get("regularMarketPrice") is None:
            # Fallback: try without .NS suffix (for US stocks)
            plain_info = {}
            try:
                ticker = self._yf.Ticker(symbol)
                plain_info = ticker.info or {}
            except Exception:
                pass
            if plain_info.get("regularMarketPrice"):
                info = plain_info

        price = info.get("regularMarketPrice") or info.get("currentPrice") or 0
        prev_close = info.get("regularMarketPreviousClose") or info.get("previousClose") or price
        change = round(price - prev_close, 2) if price and prev_close else 0

        return {
            "symbol": symbol,
            "price": round(float(price), 2),
            "change": change,
            "change_pct": round((change / prev_close) * 100, 2) if prev_close else 0,
            "open": round(float(info.get("regularMarketOpen") or info.get("open") or price), 2),
            "high": round(float(info.get("regularMarketDayHigh") or info.get("dayHigh") or price), 2),
            "low": round(float(info.get("regularMarketDayLow") or info.get("dayLow") or price), 2),
            "prev_close": round(float(prev_close), 2),
            "volume": int(info.get("regularMarketVolume") or info.get("volume") or 0),
            "timestamp": datetime.now().isoformat(),
        }

    def get_historical_prices(
        self, symbol: str, range_type: str = "1M"
    ) -> list[dict]:
        """Fetch real OHLCV historical data from Yahoo Finance."""
        # Map our range codes to yfinance period/interval params
        range_map = {
            "1D":  {"period": "1d",  "interval": "5m"},
            "1W":  {"period": "5d",  "interval": "15m"},
            "1M":  {"period": "1mo", "interval": "1d"},
            "3M":  {"period": "3mo", "interval": "1d"},
            "6M":  {"period": "6mo", "interval": "1d"},
            "1Y":  {"period": "1y",  "interval": "1wk"},
            "5Y":  {"period": "5y",  "interval": "1mo"},
            "MAX": {"period": "max", "interval": "1mo"},
        }
        params = range_map.get(range_type, {"period": "1mo", "interval": "1d"})

        try:
            resolved = self._resolve_symbol(symbol)
            ticker = self._yf.Ticker(resolved)
            hist = ticker.history(period=params["period"], interval=params["interval"])

            # If no data with .NS, try plain symbol
            if hist.empty and ".NS" in resolved:
                ticker = self._yf.Ticker(symbol)
                hist = ticker.history(period=params["period"], interval=params["interval"])

            if hist.empty:
                print(f"[YFinance] No historical data for {symbol}")
                return []

            data = []
            for idx, row in hist.iterrows():
                ts = idx.isoformat() if hasattr(idx, "isoformat") else str(idx)
                data.append({
                    "timestamp": ts,
                    "open": round(float(row["Open"]), 2),
                    "high": round(float(row["High"]), 2),
                    "low": round(float(row["Low"]), 2),
                    "close": round(float(row["Close"]), 2),
                    "volume": int(row["Volume"]),
                })
            return data

        except Exception as e:
            print(f"[YFinance] Error fetching history for {symbol}: {e}")
            return []

    def get_fundamentals(self, symbol: str) -> dict:
        """Fetch real fundamental data from Yahoo Finance."""
        info = self._get_info(symbol)

        # Helper to safely extract a float
        def _f(key, fallback=None):
            val = info.get(key)
            if val is None:
                return fallback
            try:
                return round(float(val), 2)
            except (ValueError, TypeError):
                return fallback

        # Market cap in Crores (for Indian context) or raw
        market_cap_raw = _f("marketCap", 0)
        market_cap = round(market_cap_raw / 10000000, 2) if market_cap_raw else 0  # Convert to Cr

        return {
            "symbol": symbol,
            "market_cap": market_cap,
            "pe": _f("trailingPE") or _f("forwardPE"),
            "pb": _f("priceToBook"),
            "roe": _f("returnOnEquity", 0) * 100 if _f("returnOnEquity") else None,
            "roce": None,  # Not directly available in yfinance
            "debt_to_equity": _f("debtToEquity", 0) / 100 if _f("debtToEquity") else None,
            "eps": _f("trailingEps"),
            "dividend_yield": _f("dividendYield", 0) * 100 if _f("dividendYield") else 0,
            "net_profit_margin": _f("profitMargins", 0) * 100 if _f("profitMargins") else None,
            "sales_growth": _f("revenueGrowth", 0) * 100 if _f("revenueGrowth") else None,
            "profit_growth": _f("earningsGrowth", 0) * 100 if _f("earningsGrowth") else None,
            "promoter_holding": None,  # Not available via yfinance
        }


# ── Factory ──────────────────────────────────────────────────

# Singleton instance to preserve the cache across requests
_yfinance_instance = None


def get_data_provider():
    """Factory: return the configured data provider."""
    global _yfinance_instance
    if Config.DATA_PROVIDER == "mock":
        return MockDataProvider()
    # Any non-mock value (e.g. "yfinance", "real", "live") uses Yahoo Finance
    if _yfinance_instance is None:
        _yfinance_instance = YFinanceDataProvider()
    return _yfinance_instance

