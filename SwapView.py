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

        btn_frame = Frame(self.root)
        ut.button(btn_frame, "Swap", self.swap).pack(side=LEFT, expand=True, fill=X)
        ut.button(btn_frame, "Close", self.root.destroy).pack(side=LEFT, expand=True, fill=X)
        btn_frame.pack(expand=True, fill=BOTH, pady=(0, 10), padx=10)

    def populate_teams(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for team in self.model.get_manageable_teams().get_teams():
            self.tree.insert("", "end", values=(str(team),))

    def swap(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return 
        
        team_name = self.tree.item(selection[0])['values'][0]
        for team in self.model.get_manageable_teams().get_teams():
            if str(team) == team_name:
                self.model.set_manager_for_team(self.manager, team)
                break
                
        self.observable_view.update_view()
        self.root.destroy()