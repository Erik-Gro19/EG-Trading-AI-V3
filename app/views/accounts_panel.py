# app/views/accounts_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QComboBox, QHBoxLayout

class AccountsPanel(QFrame):
    def __init__(self, accounts_service):
        super().__init__()
        self.setObjectName("Card")
        self.accounts_service = accounts_service

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<b>Kontenverwaltung</b>"))

        row = QHBoxLayout()
        self.account_selector = QComboBox()
        self.update_accounts()
        self.account_selector.currentIndexChanged.connect(self.account_changed)
        row.addWidget(QLabel("Konto:"))
        row.addWidget(self.account_selector)
        layout.addLayout(row)

        self.details_label = QLabel("")
        layout.addWidget(self.details_label)

        self.setLayout(layout)

        self.display_account_details()

    def update_accounts(self):
        self.account_selector.clear()
        names = [acc['name'] for acc in self.accounts_service.get_accounts()]
        self.account_selector.addItems(names)

    def account_changed(self):
        self.display_account_details()

    def display_account_details(self):
        idx = self.account_selector.currentIndex()
        if idx < 0:
            self.details_label.setText("Kein Konto ausgewählt.")
            return
        account = self.accounts_service.get_accounts()[idx]
        balance = account.get("balance", "—")
        currency = account.get("currency", "")
        stats = account.get("stats", {})
        details = f"Konto: {account['name']}<br>Balance: {balance} {currency}<br>"
        if stats:
            details += "<br>".join([f"{k}: {v}" for k, v in stats.items()])
        self.details_label.setText(details)
