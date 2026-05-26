# engine/utils/accounts_service.py

import json, os

class AccountsService:
    def __init__(self, json_path="accounts.json"):
        self.json_path = json_path
        self.accounts = []
        self.load()

    def load(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, "r") as f:
                self.accounts = json.load(f)
        else:
            self.accounts = []

    def save(self):
        with open(self.json_path, "w") as f:
            json.dump(self.accounts, f, indent=2)

    def get_accounts(self):
        return self.accounts

    def add_account(self, acc):
        self.accounts.append(acc)
        self.save()

    def edit_account(self, idx, acc):
        self.accounts[idx] = acc
        self.save()

    def delete_account(self, idx):
        self.accounts.pop(idx)
        self.save()
