# app/views/user_manage_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QListWidget, QHBoxLayout, QMessageBox

class UserManagePanel(QFrame):
    def __init__(self, user_service):
        super().__init__()
        self.setObjectName("Card")
        self.user_service = user_service

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>User/Rollen-Verwaltung</b>"))

        self.user_list = QListWidget()
        self.user_list.addItems([u['username'] for u in self.user_service.get_users()])
        layout.addWidget(self.user_list)

        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["admin", "trader", "viewer"])

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_edit)
        layout.addWidget(QLabel("Passwort:"))
        layout.addWidget(self.password_edit)
        layout.addWidget(QLabel("Rolle:"))
        layout.addWidget(self.role_combo)

        row = QHBoxLayout()
        self.add_btn = QPushButton("Hinzufügen")
        self.delete_btn = QPushButton("Löschen")
        row.addWidget(self.add_btn)
        row.addWidget(self.delete_btn)
        layout.addLayout(row)

        self.add_btn.clicked.connect(self.add_user)
        self.delete_btn.clicked.connect(self.delete_user)
        self.user_list.currentRowChanged.connect(self.populate_fields)

        self.populate_fields(0)

    def populate_fields(self, idx):
        users = self.user_service.get_users()
        if idx < 0 or idx >= len(users):
            self.username_edit.clear()
            self.password_edit.clear()
            self.role_combo.setCurrentText("trader")
            return
        u = users[idx]
        self.username_edit.setText(u.get("username", ""))
        self.password_edit.setText("*****")
        self.role_combo.setCurrentText(u.get("role", "trader"))

    def add_user(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        role = self.role_combo.currentText()
        if not username or not password:
            QMessageBox.warning(self, "Fehler", "Username und Passwort erforderlich!")
            return
        user = {
            "username": username,
            "password": self.user_service._hash(password),
            "role": role
        }
        self.user_service.add_user(user)
        self.user_list.addItem(username)
        QMessageBox.information(self, "Hinzugefügt", "User wurde hinzugefügt.")

    def delete_user(self):
        idx = self.user_list.currentRow()
        if idx < 0:
            return
        self.user_service.delete_user(idx)
        self.user_list.takeItem(idx)
        QMessageBox.information(self, "Gelöscht", "User wurde gelöscht.")
