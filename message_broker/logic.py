from database import MsgBrokerDatabase


class MsgBrokerLogic:
    def __init__(self):
        self.db = MsgBrokerDatabase()

    def add_new_event(self, event):
        self.db.insert(event)

    def fetch_all_events(self):
        return self.db.fetch()
