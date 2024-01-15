import sqlite3
import pandas as pd
from tkinter import messagebox, simpledialog


class DBHandler:
    def __init__(self, file_name):
        self.data = None
        self.file_name = file_name
        self.conn = sqlite3.connect(file_name)
        self.cursor = self.conn.cursor()

    def open_database(self):
        try:
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            self.cursor.execute(query)

            tables = self.cursor.fetchall()
            tables_list = [table[0] for table in tables]
            tables_string = "\n".join(tables_list)
            prompt = "Choose table from db: \n\n" + tables_string + "\n"

            table_name = simpledialog.askstring("Enter table name", prompt)
            if table_name is None:
                return None
            return pd.read_sql_query("SELECT * FROM " + table_name, self.conn)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None
        finally:
            self.close_conn()

    def get_conn(self):
        return self.conn

    def close_conn(self):
        self.cursor.close()
        self.conn.close()
