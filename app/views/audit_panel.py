# app/views/audit_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from engine.utils.audit_log import AuditLog

class AuditPanel(QFrame):
    def __init__(self, audit_log: AuditLog = None):
        super().__init__()
        self.setObjectName("Card")
        self.audit_log = audit_log or AuditLog()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Audit Trail / User- & System-Events</b>"))
        
        self.refresh_btn = QPushButton("Aktualisieren")
        layout.addWidget(self.refresh_btn)
        self.refresh_btn.clicked.connect(self.reload_log)

        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.reload_log()

    def reload_log(self):
        lines = self.audit_log.read_recent(32)
        if not lines:
            self.table.setRowCount(1)
            self.table.setColumnCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("Keine Einträge gefunden!"))
            return

        header = [h.strip() for h in lines[0].split(",")]
        data = [l.strip().split(",", maxsplit=3) for l in lines[1:]]
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(val))
