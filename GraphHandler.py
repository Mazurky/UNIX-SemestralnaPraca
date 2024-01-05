import tkinter as tk
from tkinter import ttk


class GraphHandler:
    def __init__(self, master, data):
        self.data = data
        self.top = tk.Toplevel(master)
        self.top.configure(height=500, width=500)
        self.top.resizable(False, True)

        self.left_side = ttk.Frame(self.top)
        self.left_inside = ttk.Frame(self.left_side)
        self.label_graph_type = ttk.Label(self.left_inside)
        self.label_graph_type.configure(text='Select graph type')
        self.label_graph_type.pack(padx=16, pady=10, side="top")
        self.line = ttk.Button(self.left_inside)
        self.line.configure(text='Line')
        self.line.pack(pady=4, side="top")
        self.bar = ttk.Button(self.left_inside)
        self.bar.configure(text='Bar')
        self.bar.pack(pady=4, side="top")
        self.Pie = ttk.Button(self.left_inside)
        self.Pie.configure(text='Pie')
        self.Pie.pack(pady=4, side="top")
        self.Scatter = ttk.Button(self.left_inside)
        self.Scatter.configure(text='Scatter')
        self.Scatter.pack(pady=4, side="top")
        self.left_inside.pack(side="left")
        self.left_side.pack(fill="both", side="left")
        self.right_side = ttk.Frame(self.top)
        self.right_inside = ttk.Frame(self.right_side)
        self.right_inside.configure(height=200, width=200)
        self.label_graph_options = ttk.Label(self.right_inside)
        self.label_graph_options.configure(text='Select graph options')
        self.label_graph_options.pack(padx=16, pady=10, side="top")
        self.label_frame_x = ttk.Labelframe(self.right_inside)
        self.label_frame_x.configure(height=80, text='axis X', width=200)
        csv_columns = list(self.data.columns)

        combobox = ttk.Combobox(self.label_frame_x)
        combobox.configure(values=csv_columns)
        combobox.pack(side="top")

        self.label_frame_x.pack(fill="both", padx=4, side="top")

        self.label_frame_y = ttk.Labelframe(self.right_inside)
        self.label_frame_y.configure(height=80, text='axis y', width=200)

        checkboxes_frame = ttk.Frame(self.label_frame_y)
        checkboxes = []
        for column in csv_columns:
            checkbox_var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(checkboxes_frame, text=column, variable=checkbox_var, takefocus=0)
            checkbox.pack(pady=3, side="top", anchor="w")
            checkboxes.append((column, checkbox_var))

        checkboxes_frame.pack(side="top")

        # TODO: implement graph options on button press

        self.label_frame_y.pack(fill="both", padx=4, side="top")

        self.right_inside.pack(side="right")
        self.right_side.pack(fill="both", side="right")

        separator = ttk.Separator(self.top)
        separator.configure(orient="vertical")
        separator.pack(expand=True, fill="y", side="top")

        # Main widget
        self.mainwindow = self.top
