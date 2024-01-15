import tkinter as tk
from Menu import Menu


class App:
    def __init__(self, master):
        self.master = master
        master.title("Data Viewer")
        self.menu = Menu(master)


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = App(root)
        root.mainloop()
    except KeyboardInterrupt as KeI:
        print("Keyboard interrupt")
    except Exception as e:
        print(e)
