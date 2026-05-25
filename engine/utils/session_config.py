# engine/utils/session_config.py

class SessionConfig:
    def __init__(self):
        self.live_mode = False
        self.default_symbol = "BTCUSD"
        self.default_lot = 0.01
        self.bot_cooldown = 60  # Sekunden
        self.default_risk = 0.01
        self.available_symbols = ["BTCUSD", "XAUUSD"]
        self.last_emergency = None
        self._subscribers = []

    def as_dict(self):
        return {
            "live_mode": self.live_mode,
            "default_symbol": self.default_symbol,
            "default_lot": self.default_lot,
            "bot_cooldown": self.bot_cooldown,
            "default_risk": self.default_risk,
            "last_emergency": self.last_emergency,
        }

    def subscribe(self, callback):
        """Erlaubt es Modulen, auf Config-Änderungen zu reagieren."""
        self._subscribers.append(callback)

    def notify_all(self):
        """Alle Subscriber bei Änderung benachrichtigen."""
        for cb in self._subscribers:
            cb(self)
