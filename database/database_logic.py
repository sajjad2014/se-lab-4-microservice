from database import Database


class DatabaseLogic:
    def __init__(self):
        self.db = Database()

    def add_new_user(self, username, password, email=None, mobile=None):
        self.db.insert(username, password, email, mobile)

    def update_profile(self, username, password, email, mobile):
        self.db.update(username, password, email, mobile)

    def remove_user(self, username):
        self.db.delete(username)

    def get_profile(self, username):
        return self.db.fetch(username)

    def change_username(self, old_username, new_username):
        old_info = self.db.fetch(old_username)
        self.db.delete(old_username)
        old_info = list(old_info)
        old_info[0] = new_username
        self.db.insert(*old_info)