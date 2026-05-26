# app/views/accounts_manage_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QListWidget, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt

class AccountsManagePanel(QFrame):
    def __init__(self, accounts_service):
        super().__init__()
        self.setObjectName("Card")
        self.accounts_service = accounts_service

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Konto-Verwaltung (Hinzufügen/Bearbeiten)</b>"))

        # Auswahl existierender Accounts
        self.account_list = QListWidget()
        self.account_list.addItems([a['name'] for a in self.accounts_service.get_accounts()])
        layout.addWidget(self.account_list)

        # Felder für neuen/zu bearbeitenden Account
        self.name_edit = QLineEdit()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["binance", "fxcm"])  # erweiterbar!
        self.api_key_edit = QLineEdit()
        self.api_secret_edit = QLineEdit()

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("Broker/Typ:"))
        layout.addWidget(self.type_combo)
        layout.addWidget(QLabel("API Key / Login:"))
        layout.addWidget(self.api_key_edit)
        layout.addWidget(QLabel("API Secret / Server:"))
        layout.addWidget(self.api_secret_edit)

        row = QHBoxLayout()
        self.add_btn = QPushButton("Hinzufügen")
        self.edit_btn = QPushButton("Speichern")
        self.delete_btn = QPushButton("Löschen")
        row.addWidget(self.add_btn)
        row.addWidget(self.edit_btn)
        row.addWidget(self.delete_btn)
        layout.addLayout(row)

        self.add_btn.clicked.connect(self.add_account)
        self.edit_btn.clicked.connect(self.save_account)
        self.delete_btn.clicked.connect(self.delete_account)
        self.account_list.currentRowChanged.connect(self.populate_fields)

        self.populate_fields(0)

    def populate_fields(self, idx):
        if idx < 0 or idx >= len(self.accounts_service.get_accounts()):
            self.name_edit.clear()
            self.api_key_edit.clear()
            self.api_secret_edit.clear()
            return
        acc = self.accounts_service.get_accounts()[idx]
        self.name_edit.setText(acc.get("name", ""))
        self.type_combo.setCurrentText(acc.get("type", "binance"))
        self.api_key_edit.setText(acc.get("api_key", acc.get("login", "")))
        self.api_secret_edit.setText(acc.get("api_secret", acc.get("server", "")))

    def add_account(self):
        acc = {
            "name": self.name_edit.text(),
            "type": self.type_combo.currentText(),
            "api_key": self.api_key_edit.text(),
            "api_secret": self.api_secret_edit.text()
        }
        self.accounts_service.add_account(acc)
        self.account_list.addItem(acc["name"])
        QMessageBox.information(self, "Hinzugefügt", "Konto wurde hinzugefügt.")

    def save_account(self):
        idx = self.account_list.currentRow()
        if idx < 0:
            return
        acc = {
            "name": self.name_edit.text(),
            "type": self.type_combo.currentText(),
            "api_key": self.api_key_edit.text(),
            "api_secret": self.api_secret_edit.text()
        }
        self.accounts_service.edit_account(idx, acc)
        self.account_list.item(idx).setText(acc["name"])
        QMessageBox.information(self, "Gespeichert", "Konto wurde geändert.")

    def delete_account(self):
        idx = self.account_list.currentRow()
        if idx < 0:
            return
        self.accounts_service.delete_account(idx)
        self.account_list.takeItem(idx)
        QMessageBox.information(self, "Gelöscht", "Konto wurde gelöscht.")
