def resize_window(window_name):
    """
    Resizes window to fit all widgets
    :param window_name: tk.Tk, tk.Frame or tk.TopLevel
    :return: None
    """
    window_name.update_idletasks()
    req_width = window_name.winfo_reqwidth()
    req_height = window_name.winfo_reqheight() + 10
    window_name.geometry(f"{req_width}x{req_height}")