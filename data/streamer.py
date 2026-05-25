# data/streamer.py

import asyncio
from typing import Callable, Dict, List
from data.feeds.binance import BinanceFeed
from data.feeds.forexcom import ForexComFeed
from data.normalizer import normalize_candle

class DataStreamer:
    def __init__(self):
        self.feeds = {
            "BTCUSD": BinanceFeed(symbol="BTCUSDT", interval="1m"),
            "XAUUSD": ForexComFeed(symbol="XAU/USD", interval="1min"),
        }
        self.callbacks: List[Callable[[str, dict], None]] = []

    def register_callback(self, callback: Callable[[str, dict], None]):
        """Register function to receive (symbol, normalized_candle) every update."""
        self.callbacks.append(callback)

    async def start(self):
        await asyncio.gather(
            self._stream_binance(),
            self._stream_forexcom()
        )

    async def _stream_binance(self):
        async for candle in self.feeds["BTCUSD"].stream_candles():
            norm = normalize_candle(candle, source="binance")
            for cb in self.callbacks:
                cb("BTCUSD", norm)

    async def _stream_forexcom(self):
        while True:
            candles = await self.feeds["XAUUSD"].fetch_historical(limit=1)
            if candles:
                norm = normalize_candle(candles[0], source="forexcom")
                for cb in self.callbacks:
                    cb("XAUUSD", norm)
            await asyncio.sleep(60)  # 1 new candle per minute
