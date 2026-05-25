# data/feeds/mt5.py

# ... rest of your MT5Connector class above ...

    def get_account_info(self):
        # Returns dict with balance, equity, margin, etc.
        acc = mt5.account_info()
        if acc is None:
            return {"error": "No account info"}
        return acc._asdict()

    def get_open_trades(self):
        # Returns a list of open positions as dicts
        deals = mt5.positions_get()
        if deals is None:
            return []
        return [d._asdict() for d in deals]

    def get_trade_history(self, count=20):
        # Returns latest closed deals
        import time
        now = int(time.time())
        earlier = now - 3600*48  # last 48 hours
        deals = mt5.history_deals_get(earlier, now)
        if deals is None:
            return []
        return [d._asdict() for d in deals][-count:]
