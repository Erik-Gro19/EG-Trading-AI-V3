# app/views/news_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QListWidget, QPushButton
from PyQt6.QtCore import Qt

class NewsPanel(QFrame):
    def __init__(self, news_service):
        super().__init__()
        self.setObjectName("Card")
        self.news_service = news_service

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>News & Events</b>"))

        self.refresh_btn = QPushButton("Aktualisieren")
        layout.addWidget(self.refresh_btn)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(self.list_widget.NoSelection)
        layout.addWidget(self.list_widget)

        self.refresh_btn.clicked.connect(self.update_news)
        self.update_news()

    def update_news(self):
        self.list_widget.clear()
        news_items = self.news_service.get_latest_news()
        if not news_items:
            self.list_widget.addItem("Keine News empfangen.")
        else:
            for item in news_items:
                text = f"{item['timestamp']} — {item['headline']}"
                self.list_widget.addItem(text)
