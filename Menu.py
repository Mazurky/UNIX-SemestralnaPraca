import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from FileHandler import FileHandler
from CSVHandler import CSVHandler
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

        self.open_file_button = ttk.Button(self.buttons, command=lambda: self.load_file(ask_path=False))
        self.open_file_button.configure(cursor="hand2", text='Open file', width=18)
        self.open_file_button.pack(pady=2, side="top")

        self.change_file_button = ttk.Button(self.buttons, command=self.load_file)
        self.change_file_button.configure(cursor="hand2", text='Change file', width=18)

        self.selected_file_text = ttk.Label(self.buttons)
        self.selected_file_text.configure(cursor="arrow", text="")

        self.display_csv_button = ttk.Button(self.buttons, command=self.display_csv_data)
        self.display_csv_button.configure(cursor="hand2", text='Show CSV', width=18)
        # self.display_csv_button.pack(pady=2, side="top")

        self.show_graph_button = ttk.Button(self.buttons, command=self.show_graph)
        self.show_graph_button.configure(cursor="hand2", text='Show graph', width=18)
        # self.show_graph_button.pack(pady=2, side="top")

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

    def load_file(self, ask_path=True):
        if ask_path:
            file_path = self.ask_file_or_url()
        else:
            file_path = "D:\\instadelete\\commodity-price-index-cereal-crops-and-petroleum.csv"

        if file_path:
            self.data = pd.read_csv(file_path)
            if self.data is not None:
                self.hide_buttons()
                self.selected_file_text.configure(text="File: " + file_path)
                self.selected_file_text.pack(pady=2, padx=8, side="top")

                self.change_file_button.pack(pady=2, side="top")

                self.display_csv_button.pack(pady=2, side="top")
                self.show_graph_button.pack(pady=2, side="top")

                self.quit_button.pack(pady=2, side="top")
                resize_window(self.master)

    def ask_file_or_url(self):
        dialog = FileHandler(self.master)
        self.master.wait_window(dialog)
        result = dialog.result
        dialog.destroy()
        return result

    def display_csv_data(self):
        try:
            if self.data is not None:
                CSVHandler(self.master, self.data)
            else:
                messagebox.showerror("Error", "File not loaded")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_graph(self):
        # TODO: show graph
        pass
