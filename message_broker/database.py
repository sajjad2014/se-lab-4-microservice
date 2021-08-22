import psycopg2


class MsgBrokerDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="event",
            user="postgres",
            password="123")
        self.cur = self.conn.cursor()
        self.table_name = "event"

    def insert(self, event):
        insert_query = f"INSERT INTO public.{self.table_name} (event) " \
                       f"VALUES(%s)"
        record = [event]
        self.cur.execute(insert_query, record)
        self.conn.commit()

    def fetch(self):
        select_query = f"SELECT * FROM public.{self.table_name} "
        self.cur.execute(select_query)
        return self.cur.fetchall()
