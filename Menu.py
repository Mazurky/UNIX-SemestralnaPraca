import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd


class Menu:
    def __init__(self, master):
        self.master = master
        self.main = tk.Frame(master)

        self.header = tk.Frame(self.main)
        self.header.configure(height=200, padx=40)

        self.title = ttk.Label(self.header)
        self.title.configure(cursor="arrow", text='CSV Viewer', font=("TkDefaultFont", 20, 'bold'))
        self.title.pack(expand=True, pady=4, side="top")

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
        self.resize_window(master)
        self.data = None

    def hide_buttons(self):
        self.open_file_button.pack_forget()
        self.display_csv_button.pack_forget()
        self.show_graph_button.pack_forget()
        self.quit_button.pack_forget()
        self.selected_file_text.pack_forget()
        self.change_file_button.pack_forget()

    @staticmethod
    def resize_window(window_name):
        window_name.update_idletasks()
        req_width = window_name.winfo_reqwidth()
        req_height = window_name.winfo_reqheight() + 10
        window_name.geometry(f"{req_width}x{req_height}")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            if self.data is not None:
                self.hide_buttons()
                self.selected_file_text.configure(text="File: " + file_path)
                self.selected_file_text.pack(pady=2, side="top")

                self.change_file_button.pack(pady=2, side="top")

                self.display_csv_button.pack(pady=2, side="top")
                self.show_graph_button.pack(pady=2, side="top")

                self.quit_button.pack(pady=2, side="top")
                self.resize_window(self.master)

    def display_csv_data(self):
        top = None
        try:
            if self.data is not None:
                top = tk.Toplevel(self.master)
                top.title("CSV Data")

                tree = ttk.Treeview(top, show="headings")

                tree["columns"] = list(self.data.columns)
                for col in list(self.data.columns):
                    tree.heading(col, text=col)
                    tree.column(col, width=100)

                for row in self.data.itertuples(index=False):
                    tree.insert("", "end", values=row)

                vscroll = ttk.Scrollbar(top, orient="vertical", command=tree.yview)
                tree.configure(yscrollcommand=vscroll.set)

                tree.pack(padx=20, pady=20, fill="both", expand=True, side="left")
                vscroll.pack(side="right", fill="y")

                self.resize_window(top)
            else:
                messagebox.showerror("Error", "File not loaded")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            top.destroy()

    def show_graph(self):
        # TODO: show graph
        pass
