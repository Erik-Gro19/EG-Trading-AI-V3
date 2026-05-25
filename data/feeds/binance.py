# data/feeds/binance.py

import asyncio
import httpx
import websockets
import json
from typing import AsyncGenerator, Dict

BINANCE_WS_URL = "wss://fstream.binance.com/ws/btcusdt@kline_1m"
BINANCE_REST_URL = "https://fapi.binance.com/fapi/v1/klines"

class BinanceFeed:
    def __init__(self, symbol: str = "BTCUSDT", interval: str = "1m"):
        self.symbol = symbol.lower()
        self.interval = interval

    async def stream_candles(self) -> AsyncGenerator[Dict, None]:
        url = f"wss://fstream.binance.com/ws/{self.symbol}@kline_{self.interval}"
        async with websockets.connect(url) as ws:
            async for msg in ws:
                data = json.loads(msg)
                candle = data.get("k", {})
                if candle:
                    yield {
                        "timestamp": int(candle["t"]),
                        "open": float(candle["o"]),
                        "high": float(candle["h"]),
                        "low": float(candle["l"]),
                        "close": float(candle["c"]),
                        "volume": float(candle["v"]),
                        "is_final": candle["x"],
                    }

    async def fetch_historical(self, limit=100) -> list:
        params = {
            "symbol": self.symbol.upper(),
            "interval": self.interval,
            "limit": limit
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(BINANCE_REST_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            ohlcvs = []
            for d in data:
                ohlcvs.append({
                    "timestamp": d[0],
                    "open": float(d[1]),
                    "high": float(d[2]),
                    "low": float(d[3]),
                    "close": float(d[4]),
                    "volume": float(d[5])
                })
            return ohlcvs
