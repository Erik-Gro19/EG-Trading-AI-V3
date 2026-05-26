# app/views/multisymbol_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QComboBox

class MultiSymbolPanel(QFrame):
    def __init__(self, session_config):
        super().__init__()
        self.setObjectName("Card")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Symbol-Auswahl</b>"))

        self.combo = QComboBox()
        self.combo.addItems(session_config.available_symbols)
        self.combo.setCurrentText(session_config.default_symbol)
        layout.addWidget(self.combo)

        self.session_config = session_config
        self.combo.currentTextChanged.connect(self.symbol_changed)

    def symbol_changed(self, new_symbol):
        self.session_config.default_symbol = new_symbol
        self.session_config.notify_all()
