# engine/utils/user_service.py

import json
import os
import hashlib

class UserService:
    def __init__(self, json_path="users.json"):
        self.json_path = json_path
        self.users = []
        self.load()

    def load(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, "r") as f:
                self.users = json.load(f)
        else:
            self.users = []

    def save(self):
        with open(self.json_path, "w") as f:
            json.dump(self.users, f, indent=2)

    def get_users(self):
        return self.users

    def add_user(self, user):
        self.users.append(user)
        self.save()

    def delete_user(self, idx):
        self.users.pop(idx)
        self.save()

    def find_user(self, username):
        for u in self.users:
            if u["username"] == username:
                return u
        return None

    def authenticate(self, username, password):
        u = self.find_user(username)
        if not u:
            return False
        return u["password"] == self._hash(password)

    def _hash(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
