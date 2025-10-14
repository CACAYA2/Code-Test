from tkinter import *
from TkUtils import TkUtils as ut
from SwapView import SwapView
from TeamDashboardView import TeamDashboardView

class ManagerDashboardView:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.manager = self.model.get_logged_in_manager()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def withdraw(self):
        if self.manager.get_team():
            self.model.withdraw_manager_from_team(self.manager)
            self.update_view()

    def manage_team(self):
        if self.manager.get_team():
            self.root.withdraw()
            new_root = Toplevel(self.root)
            new_root.geometry("800x600") 
            TeamDashboardView(new_root, self.model, self.manager.get_team()).setup()
    
    def swap_team(self):
        SwapView(self.model, self) 

    def update_view(self):
        team = self.manager.get_team()
        if team:
            self.team_name_label.config(text=str(team))
            image_path = f"image/{team.get_jersey_filename()}"
            team_jersey_photo = ut.image(self.root, image_path, height=150, width=150).photo
            self.jersey_label.config(image=team_jersey_photo)
            self.jersey_label.photo = team_jersey_photo
            self.withdraw_button.config(state=NORMAL)
            self.manage_button.config(state=NORMAL)
        else:
            self.team_name_label.config(text="No team")
            self.jersey_label.config(image=self.no_team_jersey_img)
            self.withdraw_button.config(state=DISABLED)
            self.manage_button.config(state=DISABLED)
            
    def close(self):
        self.root.master.destroy() 

    def setup(self):
        self.root.title("Manager Dashboard")
        self.root.geometry("540x450")
        
        self.no_team_jersey_img = ut.image(self.root, "image/none.png", height=150, width=150).photo

        ut.image(self.root, "image/banner.png").pack()
        ut.separator(self.root).pack(fill=X, pady=(0, 10))

        team_frame = Frame(self.root)
        self.team_name_label = ut.label(team_frame, "")
        self.team_name_label.pack()
        self.jersey_label = Label(team_frame) 
        self.jersey_label.pack(pady=10)
        
        btn_inline_frame = Frame(team_frame)
        self.withdraw_button = ut.button(btn_inline_frame, "Withdraw", self.withdraw)
        self.withdraw_button.pack(side=LEFT, padx=5)
        self.manage_button = ut.button(btn_inline_frame, "Manage", self.manage_team)
        self.manage_button.pack(side=LEFT, padx=5)
        btn_inline_frame.pack()
        team_frame.pack(pady=10)

        bottom_btn_frame = Frame(self.root)
        ut.button(bottom_btn_frame, "Swap Team", self.swap_team).pack(side=LEFT, expand=True, fill=X)
        ut.button(bottom_btn_frame, "Close", self.close).pack(side=LEFT, expand=True, fill=X)
        bottom_btn_frame.pack(expand=True, fill=BOTH, side=BOTTOM, pady=(10, 0), padx=10)

        self.update_view() 

