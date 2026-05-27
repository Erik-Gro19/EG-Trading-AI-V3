# app/views/login_panel.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginPanel(QDialog):
    def __init__(self, user_service):
        super().__init__()
        self.user_service = user_service
        self.setWindowTitle("Login")
        self.setModal(True)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Username:"))
        self.username_edit = QLineEdit()
        layout.addWidget(self.username_edit)
        layout.addWidget(QLabel("Passwort:"))
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_edit)
        self.login_btn = QPushButton("Login")
        layout.addWidget(self.login_btn)
        self.login_btn.clicked.connect(self.try_login)

        self.result_user = None

    def try_login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        if self.user_service.authenticate(username, password):
            self.result_user = self.user_service.find_user(username)
            self.accept()  # Schließt Dialog mit Erfolgscode
        else:
            QMessageBox.warning(self, "Fehler", "Login fehlgeschlagen!")

    def get_user(self):
        return self.result_user
