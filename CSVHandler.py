import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from custom_functions import resize_window


class CSVHandler:
    def __init__(self, master, data):
        self.data = data
        self.settings_menu(master)

    def settings_menu(self, parent):
        top = None
        try:
            top = tk.Toplevel(parent)
            top.title("CSV settings")
            csv_columns = list(self.data.columns)

            text = ttk.Label(top)
            text.configure(text='Pick columns to show')
            text.pack(padx=14, pady=10, side="top")

            show_all = ttk.Button(top, command=lambda: self.display_csv_data(top))
            show_all.configure(text='Show all')
            show_all.pack(pady=3, side="top")

            checkboxes_frame = ttk.Frame(top)
            checkboxes = []
            for column in csv_columns:
                checkbox_var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(checkboxes_frame, text=column, variable=checkbox_var)
                checkbox.pack(pady=3, side="top", anchor="w")
                checkboxes.append((column, checkbox_var))

            checkboxes_frame.pack(side="top")

            def show_selected():
                selected = [col for col, var in checkboxes if var.get()]
                self.display_csv_data(top, selected)

            show_selected_button = ttk.Button(top, command=show_selected)
            show_selected_button.configure(text='Show selected')
            show_selected_button.pack(pady=8, side="top")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            if top:
                top.destroy()

    def display_csv_data(self, parent, columns_to_show=None):
        top = None
        try:
            top = tk.Toplevel(parent)
            top.title("CSV Data")

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
