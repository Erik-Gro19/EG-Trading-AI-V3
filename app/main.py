# main.py

import sys
from PyQt6.QtWidgets import QApplication
from engine.utils.user_service import UserService
from engine.utils.accounts_service import AccountsService
from engine.utils.notifications import NotificationBus
from app.views.login_panel import LoginPanel
from app.views.dashboard import DashboardWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Init User-/Role-Service
    user_service = UserService("users.json")
    
    # Login-Dialog → Hole eingeloggten User (user = dict: username, password, role)
    login = LoginPanel(user_service)
    if login.exec() != 1:
        sys.exit(0)
    current_user = login.get_user()
    if not current_user:
        sys.exit(0)

    # Init Accounts-Service (Accounts werden wie beschrieben per GUI/persistent .json eingerichtet)
    accounts_service = AccountsService("accounts.json")

    # (Optional) NotificationBus für Alarme/Fehler/UI-Notifications
    notification_bus = NotificationBus()

    # Dashboard (Rollenübergabe)
    main_window = DashboardWindow(
        user=current_user,
        accounts_service=accounts_service,
        notification_bus=notification_bus,
        user_service=user_service
    )
    main_window.show()

    sys.exit(app.exec())
