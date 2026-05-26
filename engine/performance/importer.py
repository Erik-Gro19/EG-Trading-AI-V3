# engine/performance/importer.py

import pandas as pd

class TradeImporter:
    def __init__(self):
        pass

    def import_csv(self, filepath, delimiter=","):
        df = pd.read_csv(filepath, delimiter=delimiter)
        return self._df_to_trades(df)

    def import_xlsx(self, filepath):
        df = pd.read_excel(filepath)
        return self._df_to_trades(df)

    def import_mt5_csv(self, filepath):
        # Beispieldaten: MT5-Export ist oft ';'-separiert, eigene Spaltennamen
        df = pd.read_csv(filepath, delimiter=';')
        # Mapping auf das Standardformat deines Systems
        mapper = {
            "Open Time": "timestamp_open",
            "Symbol": "symbol",
            "Type": "side",
            "Volume": "qty",
            "Open Price": "entry",
            "Close Price": "exit",
            "Profit": "pnl"
        }
        df.rename(columns=mapper, inplace=True)
        return self._df_to_trades(df)

    def _df_to_trades(self, df):
        """Konvertiert DataFrames in die im System genutzte Trades-Liste"""
        required_cols = ["timestamp_open", "symbol", "side", "qty", "entry", "exit", "pnl"]
        trades = []
        for _, row in df.iterrows():
            trade = {}
            for c in required_cols:
                trade[c] = row.get(c, None)
            trades.append(trade)
        return trades
