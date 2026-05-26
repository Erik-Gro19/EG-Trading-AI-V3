# engine/performance/reporter.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import pandas as pd
import tempfile
import os
from datetime import datetime

class TradeReporter:
    def __init__(self, base_path="app_data"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
    
    def create_equity_curve(self, trades, path):
        if not trades:
            return None
        df = pd.DataFrame(trades)
        eq = df['pnl'].cumsum()
        plt.figure(figsize=(6,4))
        plt.plot(eq, label="Equity Curve")
        plt.title("Equity-Kurve")
        plt.xlabel("Trade")
        plt.ylabel("Balance")
        plt.grid()
        plt.legend()
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        return path

    def export_pdf(self, trades, stats, filename="trades_report.pdf"):
        # PDF erstellen
        pdf_path = os.path.join(self.base_path, filename)
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Titel
        title = Paragraph("<b>Handelsbericht / Trading Report</b>", styles["Title"])
        elements.append(title)
        elements.append(Spacer(1, 0.4*cm))
        date_info = Paragraph(f"Generiert am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"])
        elements.append(date_info)
        elements.append(Spacer(1, 0.3*cm))

        # Kennzahlen
        stat_lines = [
            f"Anzahl Trades: {len(trades)}",
            f"Gesamt PnL: {stats.get('total_pnl',0):.2f}",
            f"Winrate: {stats.get('winrate',0):.2f}%",
            f"Max Drawdown: {stats.get('drawdown',0):.2f}",
            f"Erwartungswert: {stats.get('expectancy', 0):.2f}"
        ]
        stat_para = Paragraph("<br/>".join(stat_lines), styles["Normal"])
        elements.append(stat_para)
        elements.append(Spacer(1, 0.4*cm))

        # Equity-Kurve (als Bild)
        img_tmp = tempfile.mktemp(suffix=".png")
        self.create_equity_curve(trades, img_tmp)
        try:
            elements.append(Image(img_tmp, width=12*cm, height=7*cm))
        except Exception:
            pass
        elements.append(Spacer(1, 0.4*cm))

        # Tabelle
        if trades:
            trade_df = pd.DataFrame(trades)
            # Nur die wichtigsten Spalten
            columns = [col for col in ["timestamp_open", "symbol", "side", "qty", "entry", "exit", "pnl"] if col in trade_df.columns]
            data = [columns] + trade_df[columns].astype(str).values.tolist()
            tbl = Table(data, repeatRows=1)
            tbl_style = TableStyle([
                ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#EEE")),
                ("TEXTCOLOR", (0,0), (-1,0), colors.black),
                ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#AAA")),
                ("ALIGN", (0,0), (-1,-1), "CENTER"),
                ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
                ("FONTSIZE", (0,0), (-1,-1), 8),
            ])
            tbl.setStyle(tbl_style)
            elements.append(tbl)

        # PDF wirklich bauen
        doc.build(elements)
        if os.path.exists(img_tmp):
            os.remove(img_tmp)
        return pdf_path

    def make_stats(self, trades):
        df = pd.DataFrame(trades)
        stats = {}
        if df.empty:
            stats["total_pnl"] = 0
            stats["winrate"] = 0
            stats["drawdown"] = 0
            stats["expectancy"] = 0
            return stats
        stats["total_pnl"] = df['pnl'].sum()
        stats["winrate"] = 100*len(df[df['pnl']>0])/len(df)
        stats["drawdown"] = abs((df['pnl'].cumsum()-df['pnl'].cumsum().cummax()).min())
        stats["expectancy"] = df['pnl'].mean() if len(df) > 0 else 0
        return stats
