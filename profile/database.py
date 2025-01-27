import psycopg2


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="profile",
            user="postgres",
            password="123")
        self.cur = self.conn.cursor()
        self.table_name = "profile"

    def insert(self, username, password, email=None, mobile=None, status="user"):
        insert_query = f"INSERT INTO public.{self.table_name} (username, password, email, mobile, status) " \
                       f"VALUES(%s, %s, %s, %s, %s)"
        record = (username, password, email, mobile, status)
        self.cur.execute(insert_query, record)
        self.conn.commit()

    def update(self, username, password, email, mobile):
        update_query = f"UPDATE public.{self.table_name} " \
                       f"SET password=%s, " \
                       f"email=%s, " \
                       f"mobile=%s " \
                       f"WHERE username = %s " \
                       f"RETURNING *; "
        record = (password, email, mobile, username)
        self.cur.execute(update_query, record)
        self.conn.commit()
        return self.cur.fetchone()

    def delete(self, username):
        delete_query = f"DELETE FROM public.{self.table_name} " \
                       f"WHERE username = %s; "
        record = [username]
        self.cur.execute(delete_query, record)
        self.conn.commit()

    def fetch(self, username):
        select_query = f"SELECT * FROM public.{self.table_name} " \
                       f"WHERE username = %s; "
        record = [username]
        self.cur.execute(select_query, record)
        return self.cur.fetchone()

