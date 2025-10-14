from tkinter import *
from TkUtils import TkUtils as ut

class ErrorView:
    def __init__(self, error_type, error_message):
        self.root = Toplevel()
        self.root.title("Error")
        self.root.resizable(False, False)
        self.root.grab_set() # This makes the window modal

        ut.image(self.root, "image/error.png").pack()
        ut.separator(self.root).pack(fill=X, pady=5)
        
        ut.error_label(self.root, error_type).pack(pady=(5,0))
        Label(self.root, text=error_message, font="Helvetica 11").pack(pady=(0,10))
        
        ut.button(self.root, "Close", self.root.destroy).pack(fill=X, expand=True, padx=10, pady=(0, 10))