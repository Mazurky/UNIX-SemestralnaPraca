import tkinter as tk
from os import path
from tkinter import messagebox, ttk, simpledialog, filedialog
from custom_functions import *


class DataViewer:
    def __init__(self, data):
        self.data = data

    def display_data(self, parent, columns_to_show=None):
        top = None
        try:
            top = tk.Toplevel(parent)
            if columns_to_show is None:
                top.title("Data - all")
            else:
                top.title("Data - " + ", ".join(columns_to_show))

            tree = ttk.Treeview(top, show="headings")
            if columns_to_show is None:
                columns_to_show = list(self.data.columns)
            else:
                if len(columns_to_show) == 0:
                    raise Exception("No columns selected")
            tree["columns"] = columns_to_show

            for col in columns_to_show:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            for index, row in self.data.iterrows():
                tree.insert("", "end", values=list(row[columns_to_show]))

            vscroll = ttk.Scrollbar(top, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=vscroll.set)

            tree.pack(padx=20, pady=20, fill="both", expand=True, side="left")
            vscroll.pack(side="right", fill="y")

            resize_window(top)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            if top:
                top.destroy()

    def save_to_db(self, db_conn):
        try:
            while True:
                table_name = simpledialog.askstring("Enter table name", "Enter table name")
                if table_name is None:
                    return  # cancel pressed

                cursor = db_conn.cursor()
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                existing_table = cursor.fetchone()

                if existing_table:
                    messagebox.showerror("Error", f"Table '{table_name}' already exists. Please choose another name.")
                else:
                    self.data.to_sql(table_name, db_conn, if_exists="fail", index=False)
                    messagebox.showinfo("Success", "Data saved to database")
                    break
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_to_csv(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                self.data.to_csv(file_path, index=False, encoding="utf-16")
                messagebox.showinfo("Success", "Data saved to csv")
            else:
                return
        except Exception as e:
            messagebox.showerror("Error", str(e))