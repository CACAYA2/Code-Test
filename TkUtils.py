from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, UnidentifiedImageError
import os


class ObservableButton(Label):
  
    def __init__(self, root, text, callback, main_color, hover_color):
        super().__init__(root, text=text)
        self.main_color = main_color
        self.hover_color = hover_color
        self.callback = callback

        self.configure(
            font="Helvetica 12 bold",
            foreground="white",
            background=self.main_color,
            pady=5,
<<<<<<< HEAD
=======
            
>>>>>>> 786b624 (test111)
        )
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_exit)
<<<<<<< HEAD
        self.bind("<Button-1>", self.on_click)

    def on_hover(self, _):
=======
        self.bind("<Button-1>", self.on_click) 

    def on_hover(self, event):
>>>>>>> 786b624 (test111)
        self.config(background=self.hover_color)

    def on_exit(self, _):
        self.config(background=self.main_color)

    def on_click(self, _):
        if self.callback:
            self.callback()


<<<<<<< HEAD
=======

#You will never have to manually call this, It's used as part of one of the static methods
>>>>>>> 786b624 (test111)
class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def showtip(self, text_func):
        text = text_func()
        if self.tip_window or not text:
            return
        try:
            x, y, _, _ = self.widget.bbox("insert")
        except Exception:
            x, y = 0, 0
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20
        self.tip_window = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = Label(
            tw, text=text, justify=LEFT,
            background="#ffffe0", relief=SOLID, borderwidth=1,
            font=("tahoma", "8", "normal")
        )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


def create_tooltip(widget, text_func):
    tool_tip = ToolTip(widget)
    widget.bind('<Enter>', lambda event: tool_tip.showtip(text_func))
    widget.bind('<Leave>', lambda event: tool_tip.hidetip())


class TkUtils:
    red = "#ff4747"
    image_width = 540
    image_height = 300

    @staticmethod
    def root():
        window = Tk()
        window.resizable(False, False)
        window.title("Login")
        return window

<<<<<<< HEAD
=======
    
>>>>>>> 786b624 (test111)
    @staticmethod
    def top_level(title_, height=0):
        tl = Toplevel()
        tl.title(title_)
<<<<<<< HEAD
        tl.configure(background="white")
=======
        tl.configure(background="#d9d9d9")
>>>>>>> 786b624 (test111)
        return tl

    @staticmethod
    def same_window(title, root):
        for pack in root.pack_slaves():
            pack.destroy()
        root.title(title)
        return root

    @staticmethod
    def button(root, text_, callback=None, main="#F08080", hover="#FF9999"):
        return ObservableButton(root, text_, callback, main, hover)
        

    @staticmethod
    def separator(root):
        return ttk.Separator(root, orient='horizontal')

    @staticmethod
    def label(root, text_):
        return Label(root, text=text_, font="Helvetica 12 bold", foreground=TkUtils.red)

    @staticmethod
    def error_label(root, text_):
        return Label(root, text=text_, font="Courier 14", foreground="RED")

    @staticmethod
    def image(root, path, height=None, width=None, background=None):
       
        if height is None:
            height = TkUtils.image_height
        if width is None:
            width = TkUtils.image_width

        lbl = Label(root)
        if background:
            lbl.configure(background=background)

        try:
            if not os.path.exists(path):
                raise FileNotFoundError(path)
            img = Image.open(path).resize((width, height))
            image_ = ImageTk.PhotoImage(img)
            lbl.config(image=image_)
            lbl.photo = image_
        except (FileNotFoundError, UnidentifiedImageError, OSError) as _:
            
            lbl.config(text=f"[missing image: {os.path.basename(path)}]", width=width // 8, height=height // 18)
            lbl.photo = None

        return lbl

       

   

    @staticmethod
    def _select(event, tree: ttk.Treeview):
        
        item_id = tree.identify_row(event.y)
        if not item_id:
            return
        if item_id in tree.selection():
            tree.selection_remove(item_id)
            return 'break'

    @staticmethod
    def treeview(root, columns, multi=False, width=500):
        tree = ttk.Treeview(
            root,
            show="headings",
            columns=columns,
            selectmode="extended" if multi else "browse"
        )

        
        for col in columns:
            tree.column(col, anchor=CENTER, width=int(width / len(columns)), stretch=NO)
            tree.heading(col, text=col)

        
        tree.bind("<Button-1>", lambda event: TkUtils._select(event, tree))

        return tree
