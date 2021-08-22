import psycopg2


class TweetDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="tweet",
            user="postgres",
            password="123")
        self.cur = self.conn.cursor()
        self.table_name = "tweet"

    def insert(self, username, tweet):
        insert_query = f"INSERT INTO public.{self.table_name} (username, tweet, date) " \
                       f"VALUES(%s, %s, NOW())"
        record = (username, tweet)
        self.cur.execute(insert_query, record)
        self.conn.commit()

