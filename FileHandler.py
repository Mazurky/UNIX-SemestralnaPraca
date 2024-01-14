from tkinter import ttk, filedialog, simpledialog, messagebox
import tkinter as tk
from os import path
import urllib.request

import pandas as pd

from DBHandler import DBHandler


class FileHandler(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.result = None
        self.file_type = None
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
            self.file_type = "csv"
        elif file_path.endswith(".sqlite"):
            self.file_type = "database"
        else:
            return
        self.get_data(["file", self.file_type, file_path])
        self.destroy()

    def enter_url(self):
        url = simpledialog.askstring("Enter URL", "Enter the URL of the file: \t")
        if url is None:
            return
        if url.endswith(".csv"):
            self.file_type = "csv"
        elif url.endswith(".sqlite"):
            self.file_type = "database"
        else:
            messagebox.showerror("Error", "Invalid URL")
            return
        self.get_data(["url", self.file_type, url])
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
                if self.download_file(file_path):
                    messagebox.showinfo("Success", "File downloaded successfully. Open downloaded file.")
                else:
                    messagebox.showerror("Error", "File download failed")
            elif (file_source == "file" or file_source == "url") and file_type == "csv":
                self.result = pd.read_csv(file_path)
            elif file_source == "file" and file_type == "database":
                self.result = DBHandler(self.master, file_path).open_database()
            else:
                messagebox.showerror("Error", "File not loaded")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def download_file(url):
        file_name = url.split("/")[-1]
        file_path = path.abspath("files/" + file_name)
        urllib.request.urlretrieve(url, file_path)
        return True
