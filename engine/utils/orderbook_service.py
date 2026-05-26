# engine/utils/orderbook_service.py

import requests

class OrderbookService:
    def __init__(self, symbol="BTCUSDT"):
        self.symbol = symbol

    def get_orderbook(self, limit=10):
        # Beispiel: Binance Public Orderbook API (REST)
        url = f"https://api.binance.com/api/v3/depth?symbol={self.symbol}&limit={limit}"
        try:
            response = requests.get(url, timeout=3)
            data = response.json()
            bids = [(float(p), float(q)) for p, q in data.get("bids", [])]
            asks = [(float(p), float(q)) for p, q in data.get("asks", [])]
            # Sortierung nicht nötig, Binance liefert korrekt
            return {"bids": bids, "asks": asks}
        except Exception:
            return None
