import urllib.request
import tkinter as tk
import pandas as pd
from tkinter import ttk, filedialog, simpledialog, messagebox
from DBHandler import DBHandler


class FileHandler(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.result = None
        self.file_path = None
        self.title("Choose File or URL")
        self.resizable(False, False)

        label = ttk.Label(self, text="Choose how to input the file:")
        label.pack(pady=10, padx=14)

        local_file_button = ttk.Button(self, text="Find Local File", command=self.find_local_file)
        local_file_button.configure(cursor="hand2", width=18)
        local_file_button.pack(pady=5)

        url_button = ttk.Button(self, text="Enter URL", command=self.enter_url)
        url_button.configure(cursor="hand2", width=18)
        url_button.pack(pady=5)

    def find_local_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("File", "*.csv *.sqlite")])
        if file_path is None:
            return
        if file_path.endswith(".csv"):
            file_type = "csv"
        elif file_path.endswith(".sqlite"):
            file_type = "database"
        else:
            return
        self.get_data(["file", file_type, file_path])
        self.destroy()

    def enter_url(self):
        url = simpledialog.askstring("Enter URL", "Enter the URL of the file: \t")
        if url is None:
            return
        if url.endswith(".csv"):
            file_type = "csv"
        elif url.endswith(".sqlite"):
            file_type = "database"
        else:
            messagebox.showerror("Error", "Invalid URL")
            return
        self.get_data(["url", file_type, url])
        self.destroy()

    def get_data(self, file_metadata):
        try:
            if file_metadata is None:
                return
            file_source = file_metadata[0]
            file_type = file_metadata[1]
            file_path = file_metadata[2]
            self.file_path = file_path
            if file_source == "url" and file_type == "database":
                download_result = self.download_file(file_path)
                if download_result[0]:
                    db_handler = DBHandler(download_result[1])
                    self.result = db_handler.open_database()
                else:
                    messagebox.showerror("Error", "File download failed")
            elif (file_source == "file" or file_source == "url") and file_type == "csv":
                self.result = pd.read_csv(file_path)
            elif file_source == "file" and file_type == "database":
                db_handler = DBHandler(file_path)
                self.result = db_handler.open_database()
            else:
                messagebox.showerror("Error", "File not loaded")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def download_file(url):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".sqlite", filetypes=[("Database Files", "*.sqlite")])
            if file_path is None:
                return [False, ""]
            urllib.request.urlretrieve(url, file_path)
            return [True, file_path]
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return [False, ""]

    @staticmethod
    def save_to_csv(data):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                data.to_csv(file_path, index=False, encoding="utf-16")
                messagebox.showinfo("Success", "Data saved to csv")
            else:
                return
        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def save_to_db(data):
        try:
            while True:
                file_path = filedialog.asksaveasfilename(defaultextension=".sqlite", filetypes=[("Database Files", "*.sqlite")])
                db_handler = DBHandler(file_path)
                table_name = simpledialog.askstring("Enter table name", "Enter table name")
                if table_name is None:
                    return  # cancel pressed

                cursor = db_handler.get_conn().cursor()
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                existing_table = cursor.fetchone()

                if existing_table:
                    messagebox.showerror("Error", f"Table '{table_name}' already exists. Please choose another name.")
                else:
                    data.to_sql(table_name, db_handler.get_conn(), if_exists="fail", index=False)
                    messagebox.showinfo("Success", "Data saved to database")
                    db_handler.close_conn()
                    break
        except Exception as e:
            messagebox.showerror("Error", str(e))
