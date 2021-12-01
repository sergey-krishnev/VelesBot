import psycopg2
import psycopg2.extras

from data.config import IP, DB, NAME, PASS


class QuickConnection:
    def __init__(self):
        self.ps_connection = psycopg2.connect(host=IP, database=DB, user=NAME, password=PASS)
        self.ps_cursor = self.ps_connection.cursor()

    def __enter__(self):
        return self.ps_cursor

    def __exit__(self, err_type, err_value, traceback):
        self.ps_connection.commit()
        if err_type and err_value:
            self.ps_connection.rollback()
        self.ps_cursor.close()
        self.ps_connection.close()
        return False
