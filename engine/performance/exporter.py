# engine/performance/exporter.py

import pandas as pd
import os

class TradeExporter:
    def __init__(self, base_path="app_data"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def export_csv(self, trades, filename="trades_export.csv"):
        path = os.path.join(self.base_path, filename)
        if not trades:
            raise Exception("Keine Trades zum Exportieren gefunden!")
        df = pd.DataFrame(trades)
        df.to_csv(path, sep=";", index=False, decimal=".")
        return path

    def export_xlsx(self, trades, filename="trades_export.xlsx"):
        path = os.path.join(self.base_path, filename)
        if not trades:
            raise Exception("Keine Trades zum Exportieren gefunden!")
        df = pd.DataFrame(trades)
        df.to_excel(path, index=False)
        return path
