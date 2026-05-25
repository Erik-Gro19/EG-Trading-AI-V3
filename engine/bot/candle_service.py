# engine/bot/candle_service.py

from collections import defaultdict

class CandleService:
    """
    Thread/async-safe, in-memory "bus" for sharing recent candles
    between streamer, bot, and other consumers.
    """
    def __init__(self, maxlen=150):
        self.candles = defaultdict(list)
        self.maxlen = maxlen

    def add_candle(self, symbol: str, candle: dict):
        arr = self.candles[symbol]
        arr.append(candle)
        if len(arr) > self.maxlen:
            arr.pop(0)

    def get_candles(self, symbol: str, n=None):
        arr = self.candles[symbol]
        return arr[-n:] if n else list(arr)
