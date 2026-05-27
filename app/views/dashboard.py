# app/views/dashboard.py

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QPushButton, QMessageBox
)
from engine.performance.logger import TradeLogger
from engine.utils.audit_log import AuditLog
from app.views.live_chart import LiveChartPanel
from app.views.news_panel import NewsPanel
from app.views.accounts_panel import AccountsPanel
from app.views.stats_panel import StatsPanel
from app.views.import_panel import ImportPanel
from app.views.indicator_overlay import IndicatorOverlayPanel
from app.views.report_panel import ReportPanel
from app.views.orderbook_panel import OrderbookPanel
from app.views.accounts_manage_panel import AccountsManagePanel
from app.views.user_manage_panel import UserManagePanel
from app.views.audit_panel import AuditPanel

class DashboardWindow(QMainWindow):
    def __init__(self, user, accounts_service, notification_bus, user_service):
        super().__init__()
        self.setWindowTitle("Trading-Plattform – Dashboard")
        self.user = user
        self.accounts_service = accounts_service
        self.notification_bus = notification_bus
        self.user_service = user_service
        self.audit_log = AuditLog("audit_log.csv")
        self.trade_logger = TradeLogger()
        self.setMinimumSize(1440, 900)

        # Audit-Log: User-Login vermerken
        self.audit_log.log(self.user["username"], "Login", f"Role: {self.user['role']}")

        # Hauptlayout
        main = QWidget()
        self.setCentralWidget(main)
        hbox = QHBoxLayout(main)

        # Linke Spalte: Chart, Orderbuch, Overlay, Import
        left_col = QVBoxLayout()
        hbox.addLayout(left_col, 63)

        user_header = QLabel(f"Willkommen {self.user['username']} (Role: {self.user['role']})")
        user_header.setStyleSheet("font-size:21px;margin-bottom:8px;")
        left_col.addWidget(user_header)

        # Kerzenchart (inkl Trades)
        self.chart_panel = LiveChartPanel(self.trade_logger)
        left_col.addWidget(self.chart_panel)

        # Orderbuch (standardmäßig 1. Konto)
        self.orderbook_panel = OrderbookPanel(orderbook_service=self.accounts_service)
        left_col.addWidget(self.orderbook_panel)

        # Indikatoren (Overlay für Chart)
        self.ind_overlay_panel = IndicatorOverlayPanel(self.chart_panel)
        left_col.addWidget(self.ind_overlay_panel)

        # Trade-Import (CSV/XLSX/MT5 etc.)
        self.import_panel = ImportPanel(self.trade_logger)
        left_col.addWidget(self.import_panel)

        # Rechte Spalte als Scrollarea für viele Panels
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_col_content = QWidget()
        right_scroll.setWidget(right_col_content)
        right_col = QVBoxLayout(right_col_content)
        hbox.addWidget(right_scroll, 37)

        # Kontenübersicht (multi-account)
        self.accounts_panel = AccountsPanel(self.accounts_service)
        right_col.addWidget(self.accounts_panel)

        # Admins dürfen Konten konfigurieren
        self.accounts_manage_panel = AccountsManagePanel(self.accounts_service)
        if self.user["role"] == "admin":
            right_col.addWidget(self.accounts_manage_panel)

        # Statistik zu Trades
        self.stats_panel = StatsPanel(self.trade_logger)
        right_col.addWidget(self.stats_panel)

        # PDF Report erstellen
        self.report_panel = ReportPanel(self.trade_logger)
        right_col.addWidget(self.report_panel)

        # Newsfeed
        # Annahme: NotificationBus stellt news_service bereit, sonst musst du hier ggf. ein NewsService-Objekt instanziieren
        if hasattr(self.notification_bus, 'news_service'):
            self.news_panel = NewsPanel(self.notification_bus.news_service)
        else:
            # Fallback nur wenn nötig
            from engine.utils.news_service import NewsService
            self.news_panel = NewsPanel(NewsService(api_key="DEIN_NEWSAPI_KEY"))
        right_col.addWidget(self.news_panel)

        # Audit-Trail (nur admins)
        self.audit_panel = AuditPanel(self.audit_log)
        if self.user["role"] == "admin":
            right_col.addWidget(self.audit_panel)

        # User-Management (nur admins)
        self.user_manage_panel = UserManagePanel(self.user_service)
        if self.user["role"] == "admin":
            right_col.addWidget(self.user_manage_panel)

        # Logout-Button
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.try_logout)
        right_col.addWidget(logout_btn)

        # Fehler/Notification-Audit: Alle errors an Auditlog hängen
        def on_error(msg, level):
            if level.lower() in ("error", "critical"):
                self.audit_log.log(self.user["username"], "Error", msg)
        self.notification_bus.subscribe(on_error)

        # Rollenbasierte Rechtesteuerung
        if self.user["role"] == "viewer":
            self.accounts_manage_panel.hide()
            self.user_manage_panel.hide()
            self.audit_panel.hide()
            self.import_panel.setDisabled(True)
            self.report_panel.btn.setDisabled(True)

        # Panels initialisieren
        self.stats_panel.refresh_stats()
        if self.user["role"] == "admin":
            self.audit_panel.reload_log()

    def try_logout(self):
        reply = QMessageBox.question(self, "Logout", "Wirklich abmelden?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.audit_log.log(self.user["username"], "Logout", "")
            self.close()
