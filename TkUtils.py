from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk



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
            # This is a label 
        )

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_exit)
        self.bind("<Button-1>", self.on_click) # Manually handle the click

    def on_hover(self, event):
        #No  need to check for state on a Label
        self.config(background=self.hover_color)

    def on_exit(self, event):
        self.config(background=self.main_color)
        
    def on_click(self, event):
        if self.callback:
            self.callback()


#You will never have to manually call this, It's used as part of one of the static methods
# class ObservableButton(Button):
#     def __init__(self, root, text, callback, main_color, hover_color):
#         print("--- INITIALIZING NEW CUSTOM BUTTON ---")
#         super().__init__(root, text=text, command=callback)
#         self.main_color = main_color
#         self.hover_color = hover_color
        
#         self.configure(                 
#             font="Helvetica 12 bold",      
#             foreground="white",           
#             background=self.main_color,    
#             activebackground=self.hover_color, 
#             activeforeground="white",          
#             pady=5,
#             relief=FLAT,  
#             bd=0,
#             highlightthickness=0,                         
#         )

#         self.bind("<Enter>", self.on_hover)
#         self.bind("<Leave>", self.on_exit)

#     def on_hover(self, event):
#          if self['state'] == NORMAL:
#             self.config(background=self.hover_color)

#     def on_exit(self, event):
#         self.config(background=self.main_color)

#You will never have to manually call this, It's used as part of one of the static methods
class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def showtip(self, text_func):
        text = text_func() 
        if self.tip_window or not text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20
        self.tip_window = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = Label(tw, text=text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
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
        """
        Generates the root login window for the application.

        Returns:
            The root tk.Tk() object, prestyled and preconfigured.
        """
        window = Tk()
        window.resizable(False, False)
        window.title("Login")
        return window

    #Some operating systems struggle to automatically stretch the window
    #If needed, pass in a manual height and uncomment line 83
    @staticmethod
    def top_level(title_, height=0):
        """
        Generates a top level window for the application.

        Parameters:
            title_ (str): The title of the window.
            height (int, optional): The height of the window.

        Returns:
            The root tk.Tk() object, prestyled and preconfigured.
        """
        tl = Toplevel()
        tl.resizable(False, False)
        tl.title(title_)
        tl.configure(background="#d9d9d9")
        # tl.geometry(f"{TkUtils.width}x{height}")
        return tl

    @staticmethod
    def same_window(title, root):
        """
        A simple way to replace the content of a window without a top level window.

        Parameters:
            title (str): The title of the window.
            root (tk.Tk): The existing window.

        Returns:
            The existing window with all packed elements removed.
        """
        for pack in root.pack_slaves():
            pack.destroy()
        root.title(title)
        return root

    @staticmethod
    def button(root, text_, callback=None):
        """
        Generates a prestyled button according to the assignment specifications.

        Parameters:
            root (tk.Tk): The window or frame containing the button.
            text_ (str): The text of the button.
            callback (function): The callback function.

        Returns:
            A tk.Button() object, prestyled and preconfigured.
        """
        return ObservableButton(root, text_, callback,  "#F08080", "#FF9999")

    @staticmethod
    def separator(root):
        """
        Generates a prestyled separator according to the assignment specifications.

        Parameters:
            root (tk.Tk): The window or frame containing the separator.

        Returns:
            A ttk.Separator() object, prestyled and preconfigured.
        """
        return ttk.Separator(root, orient='horizontal')

    @staticmethod
    def label(root, text_):
        """
        Generates a prestyled label according to the assignment specifications.

        Parameters:
            root (tk.Tk): The window or frame containing the label.
            text_ (str): The text of the label.

        Returns:
            A tk.Label() object, prestyled and preconfigured.
        """
        return Label(root, text=text_, font="Helvetica 12 bold", foreground=TkUtils.red)

    @staticmethod
    def error_label(root, text_):
        """
        Generates a prestyled error label according to the assignment specifications.

        Parameters:
            root (tk.Tk): The window or frame containing the label.
            text_ (str): The text of the label.

        Returns:
            A tk.Label() object, prestyled and preconfigured.
        """
        return Label(root, text=text_, font="Courier 14", foreground="RED")

    @staticmethod
    def image(root, path, height=None, width=None, background=None):
        """
        Generates an image.

        Parameters:
            root (tk.Tk): The window or frame containing the image.
            path (str): The path to the image.
            height (int, optional): The height of the image. Defaults to the height of the banner image
            width (int, optional): The width of the image. Defaults to the width of the banner image
            background (str, optional): The background of the image. Defaults to no background

        Returns:
            A tk.Label() object with an image attribute, prestyled and preconfigured.
        """
        if height is None:
            height = TkUtils.image_height
        if width is None:
            width = TkUtils.image_width
        image_ = ImageTk.PhotoImage(Image.open(path).resize((width, height)))
        lbl = Label(root, image=image_)
        lbl.photo = image_
        if background:
            lbl.configure(background=background)
        return lbl

    #You will never have to manually call this, It's used as part of one of the static methods
    @staticmethod
    def _select(event, tree):
        item_id = tree.identify_row(event.y)
        if item_id is None:
            return
        if item_id in tree.selection():
            tree.selection_remove(item_id)
            return 'break'

    @staticmethod
    def treeview(root, columns, multi=False, width=500):
        """
        Generates a prestyled treeview according to the assignment specifications.

        Para)meters:
            root (tk.Tk): The window or frame containing the treeview.
            columns (list): A list of column names.
            multi (bool, optional): Whether the tree view is multi-column or not. Defaults to browse (single) mode
            width (int, optional): The width of the treeview. Defaults to 500

        Returns:
            A ttk.Treeview() object, prestyled and preconfigured with deselecting
        """
        tree = ttk.Treeview(root, show="headings", height=12, columns=columns, selectmode="extended" if multi else "browse")
        for column in tree["columns"]:
            tree.column(column, anchor=CENTER, width=int(width/len(columns)), stretch=NO)
        for i in range(len(columns)):
            tree.heading(i, text=columns[i])
        tree.bind("<<TreeViewSelect>>", 'break')
        tree.bind("<Button-1>", lambda event: TkUtils._select(event, tree))
        return tree

    