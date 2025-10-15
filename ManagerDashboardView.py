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

    def setup(self):
        self.root.title("Manager Dashboard")
        
        # Load images
        team = self.manager.get_team()
        self.no_team_jersey_img = ut.image(self.root, "image/none.png", height=150, width=150).photo

        # Setup UI
        ut.image(self.root, "image/banner.png").pack()
        ut.separator(self.root).pack(fill=X)
        
        self.team_name_label = ut.label(self.root, "No team")
        self.team_name_label.pack(pady=5)
        
        self.jersey_label = Label(self.root)
        self.jersey_label.pack(pady=10)
        
        button_frame = Frame(self.root)
        button_frame.pack(side=BOTTOM, fill=X)
        
        self.withdraw_button = ut.button(button_frame, "Withdraw", self.withdraw)
        self.withdraw_button.pack(side=LEFT, expand=True, fill=X)
        
        self.manage_button = ut.button(button_frame, "Manage", self.manage_team)
        self.manage_button.pack(side=LEFT, expand=True, fill=X)
        
        ut.button(button_frame, "Swap Team", self.swap_team).pack(side=LEFT, expand=True, fill=X)
        ut.button(button_frame, "Close", self.close).pack(side=LEFT, expand=True, fill=X)
        
        self.update_view()

    def withdraw(self):
        if self.manager.get_team():
            self.model.withdraw_manager_from_team(self.manager)
            self.update_view()

    def manage_team(self):
        if self.manager.get_team():
            self.root.withdraw()
            new_root = ut.top_level("Team Dashboard")
            new_root.geometry("800x600")
            # Pass only three arguments: root, model, and team
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