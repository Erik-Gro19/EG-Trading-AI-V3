# data/feeds/forexcom.py

import os
import httpx
from typing import List, Dict

TWELVE_URL = "https://api.twelvedata.com/time_series"

class ForexComFeed:
    def __init__(self, symbol: str = "XAU/USD", interval: str = "1min"):
        self.symbol = symbol
        self.interval = interval
        self.api_key = os.getenv("TWELVE_DATA_API_KEY")
    
    async def fetch_historical(self, limit: int = 100) -> List[Dict]:
        params = {
            "symbol": self.symbol,
            "interval": self.interval,
            "apikey": self.api_key,
            "outputsize": limit,
            "format": "JSON"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(TWELVE_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            candles = []
            for d in data.get("values", []):
                candles.append({
                    "timestamp": d["datetime"],
                    "open": float(d["open"]),
                    "high": float(d["high"]),
                    "low": float(d["low"]),
                    "close": float(d["close"]),
                    "volume": float(d.get("volume", 0)),  # Some providers may not send volume
                })
            return candles
