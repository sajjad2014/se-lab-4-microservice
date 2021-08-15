import jwt
import random


class APILogic:
    def __init__(self):
        self._secret = "sercert_password_asdfhn12234@#"

    def is_valid(self, token):
        try:
            jwt.decode(token, self._secret, "HS256")
            return True
        except:
            return False
