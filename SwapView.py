from tkinter import *
from TkUtils import TkUtils as ut

class SwapView:

    def __init__(self, model, observable_view):
        self.model = model
        self.observable_view = observable_view 
        self.manager = self.model.get_logged_in_manager()
        
        self.root = Toplevel()
        self.root.title("Swap")
        self.root.grab_set()

        ut.image(self.root, "image/banner.png").pack()
        ut.separator(self.root).pack(fill=X, pady=(0, 10))
        ut.label(self.root, "Swap Team").pack()

        self.tree = ut.treeview(self.root, ["Team Name"], width=500)

        self.tree.pack(pady=10, padx=10)
        self.populate_teams()


        bottom_frame = Frame(self.root)
        bottom_frame.pack(side=BOTTOM, fill=X, expand=False)

        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)

        ut.button(bottom_frame, "Swap", self.swap).grid(row=0, column=0, sticky="nsew")
        ut.button(bottom_frame, "Close", self.root.destroy).grid(row=0, column=1, sticky="nsew")

    
    def populate_teams(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for team in self.model.get_manageable_teams().get_teams():
            self.tree.insert("", "end", values=(str(team),))

    def swap(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return 
        
        team_name = self.tree.item(selected_item[0])['values'][0]
        for team in self.model.get_manageable_teams().get_teams():
            if str(team) == team_name:
                self.model.set_manager_for_team(self.manager, team)
                break
                
        self.observable_view.update_view()
        self.populate_teams()
        