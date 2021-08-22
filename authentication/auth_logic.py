import jwt
import random
from database import Database


class AuthLogic:
    def __init__(self):
        self._secret = "sercert_password_asdfhn12234@#"
        self.db = Database()
        self.columns = ["username", "password", "status"]

    def create_token(self, username):
        rand_num = random.random()
        return jwt.encode({"username": username, "salt": random.random()}, self._secret, "HS256")

    def add_new_user(self, username, password, status="user"):
        self.db.insert(username, password, status)

    def update_profile(self, username, password):
        return self.decode_prof(self.db.update(username, password))

    def remove_user(self, username):
        self.db.delete(username)

    def get_profile(self, username):
        return self.db.fetch(username)

    def decode_prof(self, prof):
        dic_prof = {}
        for column, value in zip(self.columns, prof):
            dic_prof[column] = value
        return dic_prof

    def refresh(self):
        self.db = Database()

    def get_token(self, token):
        return jwt.decode(token, self._secret, "HS256")