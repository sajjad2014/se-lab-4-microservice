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

    def delete(self, tweet_id):
        delete_query = f"DELETE FROM public.{self.table_name} " \
                       f"WHERE id = %s; "
        record = [tweet_id]
        self.cur.execute(delete_query, record)
        self.conn.commit()

    def fetch_user(self, username):
        select_query = f"select to_json(d) from (" \
                       f"SELECT * FROM public.{self.table_name} " \
                       f"WHERE username = %s " \
                       f"ORDER BY date  DESC) as d"
        record = [username]
        self.cur.execute(select_query, record)
        return self.cur.fetchall()

    def fetch_all(self):
        select_query = f"select to_json(d) from (" \
                       f"SELECT * FROM public.{self.table_name} " \
                       f"ORDER BY date  DESC) as d"
        self.cur.execute(select_query)
        return self.cur.fetchall()