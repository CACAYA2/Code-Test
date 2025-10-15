from tkinter import *
from TkUtils import TkUtils as ut

class ErrorView:
    def __init__(self, error_type, error_message):
        self.root = Toplevel()
        self.root.title("Error")
        self.root.resizable(False, False)
        self.root.grab_set() # This makes the window modal

        ut.image(self.root, "image/error.png").pack()
        ut.separator(self.root).pack(fill=X)
        
        ut.error_label(self.root, error_type).pack(pady=(10,0))
        Label(self.root, text=error_message, font="Helvetica 11").pack(pady=(5,10))

        ut.separator(self.root).pack(fill=X)
        bottom_frame = Frame(self.root)
        bottom_frame.pack(side=BOTTOM, fill=X, expand=False)
        bottom_frame.grid_columnconfigure(0, weight=1)
        
        ut.button(bottom_frame, "Close", self.root.destroy).grid(row=0, column=0, sticky="nsew")