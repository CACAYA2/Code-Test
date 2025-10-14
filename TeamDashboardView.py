from tkinter import *
from TkUtils import TkUtils as ut
from ErrorView import ErrorView
from model.exception.InvalidSigningException import InvalidSigningException
from model.exception.FillException import FillException

class TeamDashboardView:

    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.team = team
        self.selected_player_from_table = None
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def sign_player(self, event=None):
        player_name = self.player_name_var.get().strip()
        if not player_name: return
        try:
            self.model.sign_player_to_team(player_name, self.team)
            self.player_name_var.set("")
            self.update_view()
        except InvalidSigningException as e:
            ErrorView("InvalidSigningException", str(e))

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


    def setup(self):
        self.root.title("Team Dashboard")
        self.player_name_var = StringVar()

        team_jersey_path = f"image/{self.team.get_jersey_filename()}"
        
        self.team_jersey_img = ut.image(self.root, team_jersey_path, height=50, width=50).photo
        self.no_team_jersey_img = ut.image(self.root, "image/none.png", height=50, width=50).photo

        ut.image(self.root, "image/banner.png", width=800).pack()
        ut.separator(self.root).pack(fill=X)
        ut.label(self.root, str(self.team)).pack(pady=5)

        sign_frame = Frame(self.root)
        ut.label(sign_frame, "Sign a new player:").pack(side=LEFT, padx=5)
        sign_entry = Entry(sign_frame, textvariable=self.player_name_var, width=30)
        sign_entry.pack(side=LEFT)
        sign_entry.bind("<Return>", self.sign_player)
        ut.button(sign_frame, "Sign", self.sign_player).pack(side=LEFT, padx=5)
        sign_frame.pack(pady=5)

        main_frame = Frame(self.root)
        left_frame = Frame(main_frame)
        self.player_tree = ut.treeview(left_frame, ["Name", "Position"], width=400)
        self.player_tree.bind("<ButtonRelease-1>", self.on_player_select)
        self.player_tree.pack()
        left_frame.pack(side=LEFT, padx=10, pady=5)

        right_frame = Frame(main_frame)
        ut.label(right_frame, "Active Team").pack()
        
        self.jersey_buttons = []
        self.tooltip_text_funcs = [None] * 5
        jersey_frame_top = Frame(right_frame)
        jersey_frame_bottom = Frame(right_frame)

        for i in range(5):
            frame = jersey_frame_top if i < 3 else jersey_frame_bottom
            btn = Button(frame, image=self.no_team_jersey_img, relief=FLAT, command=lambda i=i: self.on_jersey_click(i))
            btn.pack(side=LEFT, padx=5, pady=5)
            self.jersey_buttons.append(btn)
            create_tooltip(btn, lambda i=i: self.tooltip_text_funcs[i]())
        
        jersey_frame_top.pack()
        jersey_frame_bottom.pack()
        right_frame.pack(side=LEFT, padx=10, fill=Y, pady=5)
        main_frame.pack(pady=10, fill=BOTH, expand=True)

        bottom_btn_frame = Frame(self.root)
        self.unsign_button = ut.button(bottom_btn_frame, "Unsign", self.unsign_player)
        self.unsign_button.pack(side=LEFT, expand=True, fill=X)
        ut.button(bottom_btn_frame, "Close", self.close).pack(side=LEFT, expand=True, fill=X)
        bottom_btn_frame.pack(fill=BOTH, side=BOTTOM, pady=(0, 10), padx=10)

        self.update_view()