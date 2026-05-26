# engine/utils/persistence.py

import json
import os

class PersistenceManager:
    def __init__(self, base_path="app_data"):
        os.makedirs(base_path, exist_ok=True)
        self.base_path = base_path

    def save_json(self, obj, filename):
        path = os.path.join(self.base_path, filename)
        with open(path, "w", encoding="utf8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)

    def load_json(self, filename, default=None):
        path = os.path.join(self.base_path, filename)
        if not os.path.isfile(path):
            return default
        with open(path, "r", encoding="utf8") as f:
            return json.load(f)
