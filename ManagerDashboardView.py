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

        white_line = Frame(self.root, height=1, bg='white')
        white_line.pack(fill=X, pady=(0, 10)) 
        
        self.jersey_label = Label(self.root)
        self.jersey_label.pack(pady=10)


        
        # button_frame = Frame(self.root)
        # button_frame.pack(side=BOTTOM, fill=X)
        
        # self.withdraw_button = ut.button(button_frame, "Withdraw", self.withdraw)
        # self.withdraw_button.pack(side=LEFT, expand=True, fill=X)
        
        # self.manage_button = ut.button(button_frame, "Manage", self.manage_team)
        # self.manage_button.pack(side=LEFT, expand=True, fill=X)
        
        # ut.button(button_frame, "Swap Team", self.swap_team).pack(side=LEFT, expand=True, fill=X)
        # ut.button(button_frame, "Close", self.close).pack(side=LEFT, expand=True, fill=X)
        
        # 1. Frame for Withdraw and Manage buttons (under jersey icon)
        jersey_button_frame = Frame(self.root)
        jersey_button_frame.pack(pady=(0, 10))
        
        self.withdraw_button = ut.button(jersey_button_frame, "Withdraw", self.withdraw)
        self.withdraw_button.pack(side=LEFT, padx=(5, 0),ipadx=20) # Use padx for spacing between buttons
        
       
        

        self.manage_button = ut.button(jersey_button_frame, "Manage", self.manage_team)
        self.manage_button.pack(side=LEFT, padx=(0, 5),ipadx=20)
        
        # 2. Frame for Swap Team and Close buttons (at the bottom, filling X, equal size)
        bottom_frame = Frame(self.root)
        bottom_frame.pack(side=BOTTOM, fill=X, expand=False)
        
        # Configure grid to ensure two columns of equal weight
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)
        

       
       
        ut.button(bottom_frame, "Swap Team", self.swap_team).grid(row=0, column=0, sticky="nsew")

        
        ut.button(bottom_frame, "Close", self.close).grid(row=0, column=1, sticky="nsew")
        
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