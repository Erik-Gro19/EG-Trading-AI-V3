# app/views/account_monitor.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from data.feeds.mt5 import MT5Connector
import config.mt5_settings as mt5_cfg

class AccountMonitorPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("Card")
        self.mt5 = MT5Connector(
            login=mt5_cfg.MT5_LOGIN,
            password=mt5_cfg.MT5_PASSWORD,
            server=mt5_cfg.MT5_SERVER,
            path=mt5_cfg.MT5_PATH
        )
        try:
            self.mt5.connect()
        except Exception as e:
            pass  # On a test/dev host this may fail

        layout = QVBoxLayout(self)

        self.acc_info_label = QLabel("Account Info: ...")
        layout.addWidget(self.acc_info_label)

        self.open_trades_table = QTableWidget()
        layout.addWidget(QLabel("Open Trades:"))
        layout.addWidget(self.open_trades_table)

        self.history_table = QTableWidget()
        layout.addWidget(QLabel("Recent Closed Trades:"))
        layout.addWidget(self.history_table)

        self.setLayout(layout)
        self.refresh_panel()

        # Refresh every 8 seconds
        from PyQt6.QtCore import QTimer
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_panel)
        self.timer.start(8000)

    def refresh_panel(self):
        # Account Info
        acc = self.mt5.get_account_info()
        if "error" not in acc:
            html = (f"<b>Balance:</b> {acc['balance']:.2f} &nbsp; "
                    f"<b>Equity:</b> {acc['equity']:.2f} &nbsp; "
                    f"<b>Margin:</b> {acc['margin']:.2f} &nbsp; "
                    f"<b>Free Margin:</b> {acc['margin_free']:.2f} &nbsp; "
                    f"<b>Profit:</b> {acc['profit']:.2f}")
        else:
            html = "<font color=red>Not connected to MT5.</font>"
        self.acc_info_label.setText(html)

        # Open trades
        wins = self.mt5.get_open_trades()
        self.open_trades_table.setColumnCount(6)
        headers = ["Ticket", "Symbol", "Type", "Volume", "Open Price", "Profit"]
        self.open_trades_table.setHorizontalHeaderLabels(headers)
        self.open_trades_table.setRowCount(len(wins))
        for i, tr in enumerate(wins):
            self.open_trades_table.setItem(i, 0, QTableWidgetItem(str(tr.get("ticket", ""))))
            self.open_trades_table.setItem(i, 1, QTableWidgetItem(str(tr.get("symbol", ""))))
            typ = "BUY" if tr.get("type", 1) == 0 else "SELL"
            self.open_trades_table.setItem(i, 2, QTableWidgetItem(typ))
            self.open_trades_table.setItem(i, 3, QTableWidgetItem(str(tr.get("volume", ""))))
            self.open_trades_table.setItem(i, 4, QTableWidgetItem(str(tr.get("price_open", ""))))
            self.open_trades_table.setItem(i, 5, QTableWidgetItem(str(tr.get("profit", ""))))
        self.open_trades_table.resizeColumnsToContents()

        # Trade history
        hist = self.mt5.get_trade_history()
        self.history_table.setColumnCount(7)
        headers2 = ["Ticket", "Symbol", "Type", "Volume", "Open Price", "Close Price", "Profit"]
        self.history_table.setHorizontalHeaderLabels(headers2)
        self.history_table.setRowCount(len(hist))
        for i, tr in enumerate(hist):
            self.history_table.setItem(i, 0, QTableWidgetItem(str(tr.get("ticket", ""))))
            self.history_table.setItem(i, 1, QTableWidgetItem(str(tr.get("symbol", ""))))
            self.history_table.setItem(i, 2, QTableWidgetItem(str(tr.get("type", ""))))
            self.history_table.setItem(i, 3, QTableWidgetItem(str(tr.get("volume", ""))))
            self.history_table.setItem(i, 4, QTableWidgetItem(str(tr.get("price_open", ""))))
            self.history_table.setItem(i, 5, QTableWidgetItem(str(tr.get("price", ""))))
            self.history_table.setItem(i, 6, QTableWidgetItem(str(tr.get("profit", ""))))
        self.history_table.resizeColumnsToContents()
