# app/main.py

import sys
import asyncio
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop
from app.views.dashboard import DashboardWindow

async def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    dashboard = DashboardWindow()
    dashboard.show()

    with loop:
        loop.run_forever()

if __name__ == "__main__":
    asyncio.run(main())
