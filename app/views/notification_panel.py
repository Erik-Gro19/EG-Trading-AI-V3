# app/views/notification_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from engine.utils.notifications import NotificationBus

LEVEL_COLORS = {
    "info": "#cceeff",
    "warning": "#ffd700",
    "error": "#ff4444",
    "success": "#00ff99",
}

class NotificationPanel(QFrame):
    def __init__(self, bus: NotificationBus):
        super().__init__()
        self.bus = bus
        self.setObjectName("Card")
        layout = QVBoxLayout()
        self.title = QLabel("<b>NOTIFICATIONS & EVENTS</b>")
        layout.addWidget(self.title)
        self.list = QListWidget()
        layout.addWidget(self.list)
        self.setLayout(layout)

        # Show latest on launch
        for (level, msg) in self.bus.get_events():
            self._add_item(level, msg)

        # Subscribe to new events
        self.bus.subscribe(self.on_new_notification)

    def on_new_notification(self, level, message):
        self._add_item(level, message)

    def _add_item(self, level, message):
        item = QListWidgetItem(f"[{level.upper()}] {message}")
        if level in LEVEL_COLORS:
            item.setForeground(QtGui.QColor(LEVEL_COLORS[level]))
        self.list.insertItem(0, item)
        # Keep scroll at top
        self.list.scrollToTop()
