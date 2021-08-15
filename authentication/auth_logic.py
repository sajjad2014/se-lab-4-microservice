import jwt
import random


class AuthLogic:
    def __init__(self):
        self._secret = "sercert_password_asdfhn12234@#"

    def create_token(self, username):
        rand_num = random.random()
        return jwt.encode({"username": username, "salt": random.random()}, self._secret, "HS256")