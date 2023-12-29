from Menu import Menu
import tkinter as tk


class App:
    def __init__(self, master):
        self.master = master
        master.title("CSV Viewer")
        self.menu = Menu(master)


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = App(root)
        root.mainloop()
    except KeyboardInterrupt as KeI:
        print("Keyboard interrupt")
