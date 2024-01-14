from tkinter import messagebox, simpledialog
import pandas as pd

import sqlite3


class DBHandler:
    def __init__(self, master, file_name, data=None):
        self.master = master
        self.data = data
        self.file_name = file_name
        try:
            self.conn = sqlite3.connect(file_name)
        except Exception as e:
            messagebox.showerror("Tu je error Error", str(e))
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
                return  # cancel pressed
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
