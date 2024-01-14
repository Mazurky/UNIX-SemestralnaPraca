from os import path
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from FileHandler import FileHandler
from CSVHandler import CSVHandler
from GraphHandler import GraphHandler
from DBHandler import DBHandler
from DataViewer import DataViewer
from custom_functions import resize_window


class Menu:
    def __init__(self, master):
        self.master = master
        self.main = tk.Frame(master)

        self.header = tk.Frame(self.main)
        self.header.configure(height=200, padx=40)

        self.header_title = ttk.Label(self.header)
        self.header_title.configure(cursor="arrow", text='CSV Viewer', font=("TkDefaultFont", 20, 'bold'))
        self.header_title.pack(expand=True, pady=4, side="top")

        self.header.grid(column=0, row=0, sticky="n")

        self.buttons = ttk.Frame(self.main)
        self.buttons.configure(height=200, width=200)

        self.open_file_button = ttk.Button(self.buttons, command=self.load_file)
        self.open_file_button.configure(cursor="hand2", text='Open file', width=18)
        self.open_file_button.pack(pady=2, side="top")

        self.change_file_button = ttk.Button(self.buttons, command=self.load_file)
        self.change_file_button.configure(cursor="hand2", text='Change file', width=18)

        self.selected_file_text = ttk.Label(self.buttons)
        self.selected_file_text.configure(cursor="arrow", text="")

        self.display_csv_button = ttk.Button(self.buttons, command=self.display_csv_data)
        self.display_csv_button.configure(cursor="hand2", text='Show data', width=18)
        # self.display_csv_button.pack(pady=2, side="top")

        self.show_graph_button = ttk.Button(self.buttons, command=self.display_graph)
        self.show_graph_button.configure(cursor="hand2", text='Show graph', width=18)
        # self.show_graph_button.pack(pady=2, side="top")

        self.save_to_db_button = ttk.Button(self.buttons, command=self.save_to_database)
        self.save_to_db_button.configure(cursor="hand2", text='Save to database', width=18)

        self.save_to_csv_button = ttk.Button(self.buttons, command=self.save_to_csv)
        self.save_to_csv_button.configure(cursor="hand2", text='Save to csv', width=18)

        self.quit_button = ttk.Button(self.buttons, command=self.master.quit)
        self.quit_button.configure(cursor="hand2", text='Close app', width=18)
        self.quit_button.pack(pady=2, side="top")

        self.buttons.grid(column=0, pady=10, row=1)

        self.main.pack(anchor="center", side="top")
        self.main.grid_anchor("n")
        resize_window(master)
        self.data = None

    def hide_buttons(self):
        self.open_file_button.pack_forget()
        self.display_csv_button.pack_forget()
        self.show_graph_button.pack_forget()
        self.quit_button.pack_forget()
        self.selected_file_text.pack_forget()
        self.change_file_button.pack_forget()
        self.save_to_db_button.pack_forget()
        self.save_to_csv_button.pack_forget()

    def load_file(self, open_file=False):
        try:
            if open_file:
                dialog = FileHandler(self.master).find_local_file()
            else:
                dialog = FileHandler(self.master)

            self.master.wait_window(dialog)
            result = dialog.result
            dialog.destroy()
            self.data = result
            self.data_loaded(dialog.file_path)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def data_loaded(self, file_path):
        if self.data is not None:
            self.hide_buttons()
            file_name = path.basename(file_path)
            self.selected_file_text.configure(text="File: " + file_name)
            self.selected_file_text.pack(pady=2, padx=8, side="top")

            self.change_file_button.pack(pady=2, side="top")

            self.display_csv_button.pack(pady=2, side="top")
            self.show_graph_button.pack(pady=2, side="top")

            if file_path.endswith(".csv"):
                self.save_to_db_button.pack(pady=2, side="top")
            else:
                self.save_to_csv_button.pack(pady=2, side="top")

            self.quit_button.pack(pady=2, side="top")
            resize_window(self.master)

    def display_csv_data(self):
        try:
            CSVHandler(self.master, self.data)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_graph(self):
        try:
            if self.data is not None:
                GraphHandler(self.master, self.data)
            else:
                messagebox.showerror("Error", "File not loaded")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_to_database(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".sqlite", filetypes=[("Database Files", "*.sqlite")])
            if file_path:
                DataViewer(self.data).save_to_db(DBHandler(self.master, file_path).get_conn())
            else:
                return
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_to_csv(self):
        DataViewer(self.data).save_to_csv()
