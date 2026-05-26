# app/views/orderbook_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt

class OrderbookPanel(QFrame):
    def __init__(self, orderbook_service):
        super().__init__()
        self.setObjectName("Card")
        self.orderbook_service = orderbook_service

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Orderbuch (Level 2)</b>"))
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Preis", "Bids", "Asks"])
        self.table.setEditTriggers(self.table.NoEditTriggers)
        layout.addWidget(self.table)

        self.refresh_orderbook()

    def refresh_orderbook(self):
        orderbook = self.orderbook_service.get_orderbook()
        if not orderbook:
            self.table.setRowCount(1)
            for col in range(3):
                self.table.setItem(0, col, QTableWidgetItem("—"))
            return

        max_rows = max(len(orderbook['bids']), len(orderbook['asks']))
        self.table.setRowCount(max_rows)
        for i in range(max_rows):
            price = orderbook['bids'][i][0] if i < len(orderbook['bids']) else orderbook['asks'][i][0]
            bid_vol = orderbook['bids'][i][1] if i < len(orderbook['bids']) else ""
            ask_vol = orderbook['asks'][i][1] if i < len(orderbook['asks']) else ""
            self.table.setItem(i, 0, QTableWidgetItem(str(price)))
            self.table.setItem(i, 1, QTableWidgetItem(str(bid_vol)))
            self.table.setItem(i, 2, QTableWidgetItem(str(ask_vol)))
