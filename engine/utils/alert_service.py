# engine/utils/alert_service.py

import smtplib
import ssl
import requests

class AlertService:
    def __init__(self, email_config=None, telegram_token=None, telegram_chat_id=None):
        self.email_config = email_config  # Dict: server, port, login, password, from_addr, to_addr
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id

    def send_email(self, subject, message):
        if not self.email_config:
            return False
        msg = f"Subject: {subject}\n\n{message}"
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.email_config["server"], self.email_config["port"], context=context) as server:
                server.login(self.email_config["login"], self.email_config["password"])
                server.sendmail(self.email_config["from_addr"], self.email_config["to_addr"], msg)
            return True
        except Exception:
            return False

    def send_telegram(self, message):
        if not self.telegram_token or not self.telegram_chat_id:
            return False
        api_url = (
            f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        )
        data = {
            "chat_id": self.telegram_chat_id,
            "text": message,
        }
        try:
            response = requests.post(api_url, data=data, timeout=5)
            return response.ok
        except Exception:
            return False

    def send_alert(self, subject, message, channels=("email", "telegram")):
        ok = True
        if "email" in channels:
            ok = ok and self.send_email(subject, message)
        if "telegram" in channels:
            ok = ok and self.send_telegram(f"{subject}\n{message}")
        return ok
