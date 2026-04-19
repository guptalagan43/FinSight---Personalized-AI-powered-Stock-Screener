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


class YFinanceDataProvider:
    """Fetches real market data from Yahoo Finance — memory-optimized for 512MB."""

    _MAX_CACHE = 30  # LRU cache cap

    def __init__(self):
        import yfinance as yf
        self._yf = yf
        self._cache = {}       # {symbol: (timestamp, slim_dict)}
        self._cache_ttl = 300  # 5 minutes

    # ── Yahoo Finance symbol mapping ────────────────────────────
    _SYMBOL_MAP = {
        "NIFTY_50": "^NSEI", "NIFTY50": "^NSEI", "NIFTY 50": "^NSEI",
        "SENSEX": "^BSESN",
        "NIFTY_BANK": "^NSEBANK", "BANKNIFTY": "^NSEBANK",
        "INDIA_VIX": "^INDIAVIX", "NIFTY_IT": "^CNXIT",
        "NIFTY_MIDCAP_100": "NIFTY_MIDCAP_100.NS",
        "NIFTY_SMALLCAP_100": "^CNXSC",
        "NIFTY_MIDCAP_150": "NIFTY_MIDCAP_150.NS",
        "NIFTY_PHARMA": "^CNXPHARMA", "NIFTY_100": "^CNX100",
        "NIFTY_AUTO": "^CNXAUTO", "NIFTY_METAL": "^CNXMETAL",
        "NIFTY_REALTY": "^CNXREALTY", "NIFTY_PSU_BANK": "^CNXPSUBANK",
        "NIFTY_FMCG": "^CNXFMCG",
        "NIFTY_FIN_SERVICE": "NIFTY_FIN_SERVICE.NS",
        "NIFTY_PVT_BANK": "NIFTY_PVT_BANK.NS",
        "NIFTY_NEXT_50": "^NSMIDCP", "GIFT_NIFTY": "^NSEI",
        "KOSPI_INDEX": "^KS11", "HANG_SENG_INDEX": "^HSI",
        "US_TECH_100": "^NDX", "DOW_JONES_FUTURES": "YM=F",
        "DOW_JONES_INDEX": "^DJI", "BSE_100": "BSE-100.BO",
        "BSE_BANKEX": "BSE-BANKEX.BO", "S&P_500": "^GSPC",
        "FTSE_100_INDEX": "^FTSE", "NIKKEI_INDEX": "^N225",
        "DAX_INDEX": "^GDAXI", "CAC_INDEX": "^FCHI",
        "HDFCBANK": "HDFCBANK.NS", "ICICIBANK": "ICICIBANK.NS",
        "SBIN": "SBIN.NS", "TATAMOTORS": "TATAMOTORS.NS",
        "BAJFINANCE": "BAJFINANCE.NS", "SUNPHARMA": "SUNPHARMA.NS",
        "HINDUNILVR": "HINDUNILVR.NS", "BHARTIARTL": "BHARTIARTL.NS",
        "AXISBANK": "AXISBANK.NS", "KOTAKBANK": "KOTAKBANK.NS",
        "ASIANPAINT": "ASIANPAINT.NS", "ADANIENT": "ADANIENT.NS",
        "ADANIPORTS": "ADANIPORTS.NS", "TATASTEEL": "TATASTEEL.NS",
        "JSWSTEEL": "JSWSTEEL.NS", "HCLTECH": "HCLTECH.NS",
        "TECHM": "TECHM.NS", "EICHERMOT": "EICHERMOT.NS",
        "HEROMOTOCO": "HEROMOTOCO.NS", "DRREDDY": "DRREDDY.NS",
        "DIVISLAB": "DIVISLAB.NS", "ULTRACEMCO": "ULTRACEMCO.NS",
        "NESTLEIND": "NESTLEIND.NS", "APOLLOHOSP": "APOLLOHOSP.NS",
        "POWERGRID": "POWERGRID.NS", "COALINDIA": "COALINDIA.NS",
        "GRASIM": "GRASIM.NS", "BAJAJFINSV": "BAJAJFINSV.NS",
        "SBILIFE": "SBILIFE.NS", "TATACONSUM": "TATACONSUM.NS",
        "BRITANNIA": "BRITANNIA.NS",
        "NIFTYBEES": "NIFTYBEES.NS", "GOLDBEES": "GOLDBEES.NS",
        "BANKBEES": "BANKBEES.NS", "LIQUIDBEES": "LIQUIDBEES.NS",
        "ITBEES": "ITBEES.NS", "SILVERBEES": "SILVERBEES.NS",
        "CPSEETF": "CPSEETF.NS", "MID150BEES": "MID150BEES.NS",
        "MON100": "MON100.NS", "PHARMABEES": "PHARMABEES.NS",
        "SUZLON": "SUZLON.NS", "IREDA": "IREDA.NS",
        "ZOMATO": "ZOMATO.NS", "PAYTM": "PAYTM.NS",
        "JIOFIN": "JIOFIN.NS", "TATATECH": "TATATECH.NS",
        "CDSL": "CDSL.NS",
    }

    def _resolve_symbol(self, symbol: str) -> str:
        if not symbol:
            return symbol
        upper = symbol.strip().upper()
        if upper in self._SYMBOL_MAP:
            return self._SYMBOL_MAP[upper]
        if "." in symbol or symbol.startswith("^"):
            return symbol
        return f"{upper}.NS"

    def _evict_cache(self):
        """Remove oldest entries if cache exceeds max size."""
        if len(self._cache) <= self._MAX_CACHE:
            return
        sorted_keys = sorted(self._cache.keys(), key=lambda k: self._cache[k][0])
        while len(self._cache) > self._MAX_CACHE:
            del self._cache[sorted_keys.pop(0)]
        import gc; gc.collect()

    def _get_slim_quote(self, symbol: str) -> dict:
        """Get lightweight quote via fast_info (much less memory than .info)."""
        now = datetime.now().timestamp()
        cached = self._cache.get(symbol)
        if cached and (now - cached[0]) < self._cache_ttl:
            return cached[1]

        try:
            resolved = self._resolve_symbol(symbol)
            ticker = self._yf.Ticker(resolved)
            fi = ticker.fast_info

            slim = {
                "price": round(float(getattr(fi, "last_price", 0) or 0), 2),
                "prev_close": round(float(getattr(fi, "previous_close", 0) or 0), 2),
                "open": round(float(getattr(fi, "open", 0) or 0), 2),
                "high": round(float(getattr(fi, "day_high", 0) or 0), 2),
                "low": round(float(getattr(fi, "day_low", 0) or 0), 2),
                "volume": int(getattr(fi, "last_volume", 0) or 0),
                "market_cap": round(float(getattr(fi, "market_cap", 0) or 0) / 10000000, 2),
                "high_52w": round(float(getattr(fi, "year_high", 0) or 0), 2),
                "low_52w": round(float(getattr(fi, "year_low", 0) or 0), 2),
            }

            if slim["price"] and slim["prev_close"]:
                slim["change"] = round(slim["price"] - slim["prev_close"], 2)
                slim["change_pct"] = round((slim["change"] / slim["prev_close"]) * 100, 2)
            else:
                slim["change"] = 0
                slim["change_pct"] = 0

            self._cache[symbol] = (now, slim)
            self._evict_cache()
            del ticker
            return slim

        except Exception as e:
            print(f"[YFinance] Error fetching quote for {symbol}: {e}")
            return {}

    def get_quote(self, symbol: str) -> dict:
        """Return a lightweight real-time quote."""
        slim = self._get_slim_quote(symbol)
        if not slim:
            return {"symbol": symbol, "price": 0, "change": 0, "change_pct": 0,
                    "prev_close": 0, "volume": 0, "timestamp": datetime.now().isoformat()}
        return {
            "symbol": symbol,
            "price": slim["price"], "change": slim["change"],
            "change_pct": slim["change_pct"], "open": slim["open"],
            "high": slim["high"], "low": slim["low"],
            "prev_close": slim["prev_close"], "volume": slim["volume"],
            "timestamp": datetime.now().isoformat(),
        }

    def get_historical_prices(self, symbol: str, range_type: str = "1M") -> list[dict]:
        """Fetch OHLCV historical data using yf.download() (memory efficient)."""
        range_map = {
            "1D": {"period": "1d", "interval": "5m"},
            "1W": {"period": "5d", "interval": "15m"},
            "1M": {"period": "1mo", "interval": "1d"},
            "3M": {"period": "3mo", "interval": "1d"},
            "6M": {"period": "6mo", "interval": "1d"},
            "1Y": {"period": "1y", "interval": "1wk"},
            "5Y": {"period": "5y", "interval": "1mo"},
            "MAX": {"period": "max", "interval": "1mo"},
        }
        params = range_map.get(range_type, {"period": "1mo", "interval": "1d"})

        try:
            resolved = self._resolve_symbol(symbol)
            hist = self._yf.download(
                resolved, period=params["period"], interval=params["interval"],
                progress=False, threads=False,
            )
            if hist.empty:
                print(f"[YFinance] No historical data for {symbol}")
                return []

            data = []
            for idx, row in hist.iterrows():
                ts = idx.isoformat() if hasattr(idx, "isoformat") else str(idx)
                try:
                    o = float(row["Open"].iloc[0]) if hasattr(row["Open"], 'iloc') else float(row["Open"])
                    h = float(row["High"].iloc[0]) if hasattr(row["High"], 'iloc') else float(row["High"])
                    l = float(row["Low"].iloc[0]) if hasattr(row["Low"], 'iloc') else float(row["Low"])
                    c = float(row["Close"].iloc[0]) if hasattr(row["Close"], 'iloc') else float(row["Close"])
                    v = int(row["Volume"].iloc[0]) if hasattr(row["Volume"], 'iloc') else int(row["Volume"])
                except (IndexError, KeyError):
                    continue
                data.append({
                    "timestamp": ts, "open": round(o, 2), "high": round(h, 2),
                    "low": round(l, 2), "close": round(c, 2), "volume": v,
                })
            del hist
            return data
        except Exception as e:
            print(f"[YFinance] Error fetching history for {symbol}: {e}")
            return []

    def get_fundamentals(self, symbol: str) -> dict:
        """Fetch fundamentals (uses .info — only called on individual detail pages)."""
        try:
            resolved = self._resolve_symbol(symbol)
            ticker = self._yf.Ticker(resolved)
            info = ticker.info or {}

            def _f(key, fallback=None):
                val = info.get(key)
                if val is None:
                    return fallback
                try:
                    return round(float(val), 2)
                except (ValueError, TypeError):
                    return fallback

            mcap_raw = _f("marketCap", 0)
            result = {
                "symbol": symbol,
                "market_cap": round(mcap_raw / 10000000, 2) if mcap_raw else 0,
                "pe": _f("trailingPE") or _f("forwardPE"),
                "pb": _f("priceToBook"),
                "roe": _f("returnOnEquity", 0) * 100 if _f("returnOnEquity") else None,
                "roce": None,
                "debt_to_equity": _f("debtToEquity", 0) / 100 if _f("debtToEquity") else None,
                "eps": _f("trailingEps"),
                "dividend_yield": _f("dividendYield", 0) * 100 if _f("dividendYield") else 0,
                "net_profit_margin": _f("profitMargins", 0) * 100 if _f("profitMargins") else None,
                "sales_growth": _f("revenueGrowth", 0) * 100 if _f("revenueGrowth") else None,
                "profit_growth": _f("earningsGrowth", 0) * 100 if _f("earningsGrowth") else None,
                "promoter_holding": None,
            }
            del info, ticker
            import gc; gc.collect()
            return result
        except Exception as e:
            print(f"[YFinance] Error fetching fundamentals for {symbol}: {e}")
            return {}


# ── Factory ──────────────────────────────────────────────────
_yfinance_instance = None


def get_data_provider():
    """Factory: return the configured data provider."""
    global _yfinance_instance
    if Config.DATA_PROVIDER == "mock":
        return MockDataProvider()
    if _yfinance_instance is None:
        _yfinance_instance = YFinanceDataProvider()
    return _yfinance_instance
