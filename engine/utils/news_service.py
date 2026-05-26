# engine/utils/news_service.py

import requests
from datetime import datetime

class NewsService:
    def __init__(self):
        # Deinen (echten!) News-API.org Key hier eintragen:
        self.api_key = "76432ae953804838be6e124c415c3635"
        self.base_url = "https://newsapi.org/v2/top-headlines"
        self.country = "us"

    def get_latest_news(self, limit=10):
        try:
            params = {
                "country": self.country,
                "apiKey": self.api_key,
                "pageSize": limit,
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            items = []
            for article in data.get("articles", []):
                try:
                    ts = datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00")).strftime('%H:%M')
                except Exception:
                    ts = "??:??"
                items.append({
                    "timestamp": ts,
                    "headline": article["title"]
                })
            return items
        except Exception as e:
            # Bei Fehler einfach leere Liste (Fehler kommen ins NotificationPanel, wenn du das willst!)
            return []
