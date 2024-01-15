import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class GraphHandler:
    def __init__(self, master, data):
        self.left_side = None
        self.left_inside = None
        self.label_graph_type = None
        self.line = None
        self.bar = None
        self.scatter = None
        self.label_picked_graph_type = None

        self.right_side = None
        self.right_inside = None
        self.label_graph_options = None
        self.label_frame_x = None
        self.label_frame_y = None
        self.separator = None
        self.data = data
        self.top = tk.Toplevel(master)
        self.top.configure(height=500, width=500)
        self.top.resizable(False, True)

        self.__init__Gui()
        self.graph_type = None
        self.graphWindows = None

    def __init__Gui(self):
        self.gui_left_side()

    def gui_left_side(self):
        self.left_side = ttk.Frame(self.top)
        self.left_inside = ttk.Frame(self.left_side)
        self.label_graph_type = ttk.Label(self.left_inside)
        self.label_graph_type.configure(text='Select graph type')
        self.label_graph_type.pack(padx=16, pady=10, side="top")
        self.line = ttk.Button(self.left_inside, command=lambda: self.set_graph_type("line"))
        self.line.configure(text='Line')
        self.line.pack(pady=4, side="top")
        self.bar = ttk.Button(self.left_inside, command=lambda: self.set_graph_type("bar"))
        self.bar.configure(text='Bar')
        self.bar.pack(pady=4, side="top")
        self.scatter = ttk.Button(self.left_inside, command=lambda: self.set_graph_type("scatter"))
        self.scatter.configure(text='Scatter')
        self.scatter.pack(pady=4, side="top")

        self.label_picked_graph_type = ttk.Label(self.left_inside)
        self.label_picked_graph_type.pack(padx=8, pady=10, side="top")

        self.left_inside.pack(side="left")
        self.left_side.pack(fill="both", side="left")

    def gui_right_side(self):
        self.right_side = ttk.Frame(self.top)
        self.right_inside = ttk.Frame(self.right_side)
        self.right_inside.configure(height=200, width=200)
        self.label_graph_options = ttk.Label(self.right_inside)
        self.label_graph_options.configure(text='Select graph options')
        self.label_graph_options.pack(padx=16, pady=10, side="top")
        self.label_frame_x = ttk.Labelframe(self.right_inside)
        self.label_frame_x.configure(height=80, text='x axis', width=200)

        csv_columns = list(self.data.columns)
        combobox = ttk.Combobox(self.label_frame_x)
        combobox.configure(values=csv_columns)
        combobox.pack(side="top")

        self.label_frame_x.pack(fill="both", padx=4, side="top")

        self.label_frame_y = ttk.Labelframe(self.right_inside)
        self.label_frame_y.configure(height=80, text='y axis', width=200)

        checkboxes_frame = ttk.Frame(self.label_frame_y)
        checkboxes = []
        for column in csv_columns:
            checkbox_var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(checkboxes_frame, text=column, variable=checkbox_var, takefocus=0)
            checkbox.pack(pady=3, side="top", anchor="w")
            checkboxes.append((column, checkbox_var))

        checkboxes_frame.pack(side="top")

        self.label_frame_y.pack(fill="both", padx=4, side="top")

        def show_selected():
            selected = [col for col, var in checkboxes if var.get()]
            self.show_graph(self.graph_type, combobox.get(), selected)

        show_selected_button = ttk.Button(self.right_inside, command=show_selected)
        show_selected_button.configure(text='Show selected')
        show_selected_button.pack(pady=8, side="top")

        self.right_inside.pack(side="right")
        self.right_side.pack(fill="both", side="right")

        self.separator = ttk.Separator(self.top)
        self.separator.configure(orient="vertical")
        self.separator.pack(expand=True, fill="y", side="top")

    def set_graph_type(self, graph_type):
        self.graph_type = graph_type
        self.label_picked_graph_type.configure(text=f'Selected: {graph_type}')
        if self.right_side is None:
            self.gui_right_side()

    def show_graph(self, graph_type, x_axis, y_axis):
        if x_axis and y_axis:
            if graph_type == "line":
                self.line_graph(x_axis, y_axis)
            elif graph_type == "bar":
                self.bar_graph(x_axis, y_axis)
            elif graph_type == "scatter":
                self.scatter_graph(x_axis, y_axis)

    def line_graph(self, x_axis, y_axes):
        plt.figure(figsize=(6, 4))
        sorted_data = self.data.sort_values(by=[x_axis])
        for y_axis in y_axes:
            plt.plot(sorted_data[x_axis], sorted_data[y_axis], label=y_axis)
        plt.xlabel(x_axis)
        plt.ylabel(', '.join(y_axes))
        plt.title('Line Graph')
        plt.legend()
        self.show_plot()

    def bar_graph(self, x_axis, y_axes):
        plt.figure(figsize=(6, 4))
        width = 0.3
        x_values = self.data[x_axis]

        for i, y_axis in enumerate(y_axes):
            x_position = x_values + i * width - (width * (len(y_axes) - 1) / 2)
            plt.bar(x_position, self.data[y_axis], width=width, label=y_axis)

        plt.xlabel(x_axis)
        plt.ylabel(', '.join(y_axes))
        plt.title('Bar Graph')
        plt.legend()
        self.show_plot()

    def scatter_graph(self, x_axis, y_axis):
        plt.figure(figsize=(6, 4))
        plt.scatter(self.data[x_axis], self.data[y_axis])
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title('Scatter Plot')
        self.show_plot()

    def show_plot(self):
        # if hasattr(self, 'graphWindows') and self.graphWindows:
        #     self.graphWindows.destroy()
        self.graphWindows = tk.Toplevel(self.top)
        self.graphWindows.title("Graphs")
        self.graphWindows.geometry("800x600")
        self.graphWindows.resizable(True, True)
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.graphWindows)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.graphWindows)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
