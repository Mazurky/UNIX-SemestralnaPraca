import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox


class FileHandler(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.result = None
        self.title("Choose File or URL")
        self.resizable(False, False)

        label = ttk.Label(self, text="Choose how to input the file:")
        label.pack(pady=10, padx=14)

        local_file_button = ttk.Button(self, text="Find Local File", command=self.find_local_file)
        local_file_button.pack(pady=5)

        url_button = ttk.Button(self, text="Enter URL", command=self.enter_url)
        url_button.pack(pady=5)

    def find_local_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.result = file_path
            self.destroy()
        else:
            messagebox.showerror("Error", "No file selected")

    def enter_url(self):
        url = simpledialog.askstring("Enter URL", "Enter the URL of the CSV file: \t")
        if url and url.endswith(".csv"):
            self.result = url
            self.destroy()
        else:
            messagebox.showerror("Error", "Invalid URL")
