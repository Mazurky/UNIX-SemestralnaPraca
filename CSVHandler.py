import tkinter as tk
from tkinter import messagebox, ttk
from DataViewer import DataViewer


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

            show_all = ttk.Button(top, command=lambda: DataViewer(self.data).display_data(top))
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
                DataViewer(self.data).display_data(top, selected)

            show_selected_button = ttk.Button(top, command=show_selected)
            show_selected_button.configure(text='Show selected')
            show_selected_button.pack(pady=8, side="top")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            if top:
                top.destroy()

