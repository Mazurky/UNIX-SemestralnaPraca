from tkinter import ttk, filedialog, simpledialog, messagebox
import tkinter as tk


class FileHandler(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.result = None
        self.title("Choose File or URL")
        self.resizable(False, False)
        self.file_type = None

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
        self.result = ["file", self.file_type, file_path]
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
        self.result = ["url", self.file_type, url]
        self.destroy()
