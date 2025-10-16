# TeamDashboardView.py - Final Layout Adjustments
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from TkUtils import TkUtils as ut
from PIL import Image, ImageTk
from model.exception.InvalidSigningException import InvalidSigningException
from model.exception.FillException import FillException
from ErrorView import ErrorView

class TeamDashboardView:
    def __init__(self, root, model, team):
        self.root = root
        self.model = model
        self.team = team
        self.selected_player_from_table = None
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.player_name_var = StringVar()
        self.jersey_buttons = []
        self.jersey_tooltips = []
        self.root.protocol("WM_DELETE_WINDOW", self.close)


        self.COLOR_BG = "#FFFFFF"
        self.COLOR_TEXT = "#202020"
        self.COLOR_BORDER = "#DCDCDC"
        self.COLOR_HEADER_BG = "#F5F5F5"
        self.COLOR_ACCENT = "#0078D7"
        self.COLOR_ACCENT_FG = "#FFFFFF"
        self.COLOR_PINK = "#E87A7A"
    

        self.root.protocol("WM_DELETE_WINDOW", self.close)

        # Color palette from previous refinement
        self.COLOR_BG = "#FFFFFF"
        self.COLOR_TEXT = "#202020"
        self.COLOR_BORDER = "#DCDCDC"
        self.COLOR_HEADER_BG = "#F5F5F5"
        self.COLOR_ACCENT = "#0078D7"
        self.COLOR_ACCENT_FG = "#FFFFFF"
        self.COLOR_PINK = "#E87A7A"
        

    def setup(self):
        self.root.title("Team Dashboard")
        

        team_jersey_path = f"image/{self.team.get_jersey_filename()}"
        
        self.team_jersey_img = ut.image(self.root, team_jersey_path, height=50, width=50).photo
        self.no_team_jersey_img = ut.image(self.root, "image/none.png", height=50, width=50).photo

        ut.image(self.root, "image/banner.png", width=800).pack()
        ut.separator(self.root).pack(fill=X)
        ut.label(self.root, str(self.team)).pack(pady=5)

        sign_frame = Frame(self.root)
        sign_frame.pack(pady=5)
        ut.label(sign_frame, "Sign a new player:").pack(side=LEFT, padx=5)
        sign_entry = Entry(sign_frame, textvariable=self.player_name_var, width=30)
        sign_entry.pack(side=LEFT)
        sign_entry.bind("<Return>", self.sign_player)
        ut.button(sign_frame, "Sign", self.sign_player).pack(side=LEFT, padx=5)

        content_frame = Frame(self.root)
        content_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        table_frame = Frame(content_frame)
        table_frame.pack(side=LEFT, fill=BOTH, expand=True)


        self.player_tree = ut.treeview(table_frame, ["Name", "Position"])
        self.player_tree.bind("<<TreeviewSelect>>", self.on_player_select)
        self.player_tree.pack(fill=BOTH, expand=True)

        active_team_frame = ttk.LabelFrame(content_frame, text="Active Team")
        active_team_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))

        positions_frame = Frame(active_team_frame)
        positions_frame.pack(expand=True)

        for i in range(5):
            jersey_button = ut.button(positions_frame, "", lambda idx=i: self.on_jersey_click(idx))
            jersey_button.config(image=self.no_team_jersey_img)
            jersey_button.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.jersey_buttons.append(jersey_button)
        
        button_frame = Frame(self.root)
        button_frame.pack(side=BOTTOM, fill=X, pady=5)
        
        self.unsign_button = ut.button(button_frame, "Unsign", self.unsign_player)
        self.unsign_button.pack(side=LEFT, expand=True, fill=X)
        self.unsign_button.config(state=DISABLED)

        ut.button(button_frame, "Close", self.close).pack(side=LEFT, expand=True, fill=X)


        self.update_view()

    def sign_player(self, event=None):
        name = self.player_name_var.get().strip()
        if not name: return
        try:
            self.model.sign_player_to_team(name, self.team)
            self.player_name_var.set("")
            self._toggle_sign_button()
            self.update_view()
        except InvalidSigningException as e: ErrorView("InvalidSigningException", str(e))


    def unsign_player(self):
        if not self.selected_player_from_table: return
        try:
            self.team.remove_player(self.selected_player_from_table)
            self.update_view()
        except InvalidSigningException as e:
            ErrorView("InvalidSigningException", str(e))

    def on_player_select(self, event):
        selected_item = self.player_tree.selection()
        if not selected_item:
            self.selected_player_from_table = None
            self.unsign_button.config(state=DISABLED)
            return
        
        player_name = self.player_tree.item(selected_item[0])['values'][0]
        self.selected_player_from_table = self.team.get_all_players().player(player_name)
        self.unsign_button.config(state=NORMAL)
    
    def on_jersey_click(self, position_index):
        player_at_pos = self.team.get_current_team()[position_index]
        if self.selected_player_from_table:
            try:
                self.team.assign_player_to_position(self.selected_player_from_table, position_index)
            except FillException as e:
                ErrorView("FillException", str(e))
        elif player_at_pos:
            self.team.unassign_player_from_position(position_index)
        self.update_view()


    def close(self):
        self.root.master.deiconify()
        self.root.destroy()

    def update_view(self):
        for item in self.player_tree.get_children():
            self.player_tree.delete(item)
        for player in sorted(self.team.get_all_players().get_players(), key=lambda p: p.get_full_name()):
            self.player_tree.insert("", "end", values=(player.get_full_name(), str(player.get_position())))

        active_team = self.team.get_current_team()
        for i, player in enumerate(active_team):
            img = self.team_jersey_img if player else self.no_team_jersey_img
            self.jersey_buttons[i].config(image=img)

            self.tooltip_text_funcs[i] = (lambda p: lambda: p.get_full_name() if p else "Empty")(player)
        
        self.selected_player_from_table = None
        self.unsign_button.config(state=DISABLED)
        if self.player_tree.selection():
            self.player_tree.selection_remove(self.player_tree.selection())


    