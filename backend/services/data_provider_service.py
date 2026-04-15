"""
Data Provider Service – Fetches market quotes and historical prices.
Mock implementation provides static/random data for local development.
Replace with a real API adapter (Alpha Vantage, Yahoo Finance, etc.) later.
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


class RealDataProvider:
    """
    Placeholder for a real market data API integration.
    Implement methods using httpx/requests to call Alpha Vantage,
    Yahoo Finance, or any other provider.
    """

    def __init__(self):
        self.api_key = Config.DATA_API_KEY
        self.base_url = Config.DATA_API_BASE_URL

    def get_quote(self, symbol: str) -> dict:
        # TODO: Implement real API call
        raise NotImplementedError("Plug in a real data provider API")

    def get_historical_prices(self, symbol: str, range_type: str = "1M") -> list:
        raise NotImplementedError("Plug in a real data provider API")

    def get_fundamentals(self, symbol: str) -> dict:
        raise NotImplementedError("Plug in a real data provider API")


def get_data_provider():
    """Factory: return the configured data provider."""
    if Config.DATA_PROVIDER == "mock":
        return MockDataProvider()
    return RealDataProvider()
