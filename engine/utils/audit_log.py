# engine/utils/audit_log.py

import csv
import threading
from datetime import datetime

class AuditLog:
    def __init__(self, logfile="audit_log.csv"):
        self.logfile = logfile
        self.lock = threading.Lock()
        # Header schreiben, falls Datei neu
        try:
            with open(self.logfile, "x", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "user", "action", "details"])
        except FileExistsError:
            pass

    def log(self, user, action, details=""):
        now = datetime.now().isoformat(sep=' ', timespec='seconds')
        with self.lock:
            with open(self.logfile, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([now, user, action, details])

    def read_recent(self, n=20):
        with self.lock:
            try:
                with open(self.logfile, "r") as f:
                    lines = f.readlines()
                header, *rows = lines
                return [header] + rows[-n:]
            except Exception:
                return []
