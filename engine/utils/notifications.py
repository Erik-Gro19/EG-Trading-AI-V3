# engine/utils/notifications.py

from engine.utils.alert_service import AlertService
import threading

class NotificationBus:
    def __init__(self):
        # Hier deine realen Zugangsdaten eintragen!
        self.alert_service = AlertService(
            email_config={
                "server": "smtp.example.com",
                "port": 465,
                "login": "user@example.com",
                "password": "passwort123",
                "from_addr": "user@example.com",
                "to_addr": "empfaenger@example.com"
            },
            telegram_token="8878302157:AAEhM6qr48AHz77RAz17fHnY_Ae2WrG1Ih8",
            telegram_chat_id="-1003976343968"
        )
        self.subscribers = []

    def subscribe(self, callback):
        """Registriert einen Callback, der bei jeder Notification aufgerufen wird."""
        self.subscribers.append(callback)

    def notify(self, message, level="info"):
        """Verteilt die Notification an alle UI-Panels – und bei error/critical auch als Alert."""
        # UI/Logger Notification (an Abonnenten, z.B. Notification-Panel)
        for cb in self.subscribers:
            try:
                cb(message, level)
            except Exception:
                pass

        # Bei Fehler/wichtigen Warnungen: E-Mail & Telegram
        if level.lower() in ("error", "critical"):
            subj = "Trading Terminal ALERT"
            # Damit UI und Workflow nicht blockiert werden, Alert asynchron senden!
            threading.Thread(
                target=self.alert_service.send_alert,
                args=(subj, message, ("email", "telegram")),
                daemon=True
            ).start()
