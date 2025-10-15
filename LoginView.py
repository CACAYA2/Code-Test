from tkinter import *
from TkUtils import TkUtils as ut
from model.application.League import league
from model.exception.UnauthorisedAccessException import UnauthorisedAccessException
from ManagerDashboardView import ManagerDashboardView
from ErrorView import ErrorView

class LoginView:

    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.manager_id_var = StringVar()
        self.manager_id_var.trace_add("write", self.on_text_change)

    def setup(self):
        self.control()

    def login(self, event=None):
        if self.login_button['state'] == DISABLED:
            return
        try:
            manager_id = self.manager_id_var.get()
            manager = self.model.validate_manager(manager_id)
            self.model.set_logged_in_manager(manager)
            
            self.root.withdraw()
            new_root = Toplevel(self.root)
            ManagerDashboardView(new_root, self.model).setup()
            
        except UnauthorisedAccessException as e:
            ErrorView("UnauthorisedAccessException", str(e))

    def on_text_change(self, *args):
        if self.manager_id_var.get():
            self.login_button.config(state=NORMAL)
        else:
            self.login_button.config(state=DISABLED)


    def control(self):
        main_content_frame = Frame(self.root)
        main_content_frame.pack(side=TOP, fill=BOTH, expand=True)

        ut.image(self.root, "image/banner.png").pack()
        ut.separator(self.root).pack(fill=X)
        ut.label(self.root, "Login").pack(pady=5)
        ut.separator(self.root).pack(fill=X)

        content_frame = Frame(self.root)
        ut.label(content_frame, "Manager ID: ").pack(side=LEFT, padx=(10, 5))
        id_entry = Entry(content_frame, textvariable=self.manager_id_var)
        id_entry.pack(side=LEFT)
        id_entry.bind("<Return>", self.login)
        id_entry.focus_set()
        content_frame.pack(pady=10)

        btn_frame = Frame(self.root)
        btn_frame.pack(side=BOTTOM, fill=X, expand=False)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        self.login_button = ut.button(btn_frame, "Login", self.login)
        self.login_button.grid(row=0, column=0, sticky="nsew") 
        self.login_button.config(state=DISABLED)
        
        
        ut.button(btn_frame, "Exit", self.root.destroy).grid(row=0, column=1, sticky="nsew")
        


if __name__ == "__main__":
    root = ut.root()
    login_view = LoginView(root, league)
    login_view.setup()
    root.mainloop()