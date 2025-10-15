# TeamDashboardView.py - Final Layout Adjustments
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from TkUtils import TkUtils as ut
from model.exception.InvalidSigningException import InvalidSigningException
from model.exception.FillException import FillException
from ErrorView import ErrorView

class TeamDashboardView:
    def __init__(self, root, model, team):
        self.root = root
        self.model = model
        self.team = team

        self.player_name_var = StringVar()
        self.selected_player_from_table = None
        self.jersey_buttons = []
        self.tooltip_text_funcs = [None] * 5

        self.root.protocol("WM_DELETE_WINDOW", self.close)

        # Color palette from previous refinement
        self.COLOR_BG = "#FFFFFF"
        self.COLOR_TEXT = "#202020"
        self.COLOR_BORDER = "#DCDCDC"
        self.COLOR_HEADER_BG = "#F5F5F5"
        self.COLOR_ACCENT = "#0078D7"
        self.COLOR_ACCENT_FG = "#FFFFFF"

    def setup(self):
        self.root.title("Team Dashboard")
        self.root.geometry("1024x768")
        self.root.minsize(980, 720)
        self.root.configure(bg=self.COLOR_BG)

        # Main layout grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1) # The content row will expand

        # ============================ HEADER ============================
        header = Frame(self.root, bg=self.COLOR_BG)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        # REFINED: 2. Reduce banner height to give more space to the content below.
        # Changed height from the default to a smaller value (e.g., 200).
        banner = ut.image(self.root, "image/banner.png", width=960, height=200, background=self.COLOR_BG)
        banner.pack(in_=header, pady=(10, 5))

        ut.separator(self.root).grid(row=0, column=0, sticky="s", pady=(5,0))
        
        team_name_label = Label(header, text=str(self.team), bg=self.COLOR_BG, fg=self.COLOR_TEXT, font=("Helvetica", 18, "bold"))
        team_name_label.pack(pady=10)

        # ============================ CONTENT BODY ============================
        content = Frame(self.root, bg=self.COLOR_BG)
        content.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        content.grid_columnconfigure(0, weight=55)
        content.grid_columnconfigure(1, weight=45)
        content.grid_rowconfigure(1, weight=1)

        # --- Sign Player Row ---
        # REFINED: 1. Center the "Sign a new player" section.
        # The outer frame spans the grid, and the inner frame uses pack() to center its contents by default.
        sign_row_container = Frame(content, bg=self.COLOR_BG)
        sign_row_container.grid(row=0, column=0, columnspan=2, pady=(5, 15))
        sign_row = Frame(sign_row_container, bg=self.COLOR_BG)
        sign_row.pack() # This pack() call centers the sign_row frame

        Label(sign_row, text="Sign a new player:", bg=self.COLOR_BG, fg=self.COLOR_TEXT,
              font=("Helvetica", 11)).pack(side=LEFT, padx=(0, 10))
        entry = Entry(sign_row, textvariable=self.player_name_var, width=35, font=("Helvetica", 11), relief="solid", bd=1)
        entry.bind("<KeyRelease>", self._toggle_sign_button)
        entry.bind("<Return>", self.sign_player)
        entry.pack(side=LEFT)
        self.sign_btn = ut.button(sign_row, "Sign", self.sign_player)
        self.sign_btn.pack(side=LEFT, padx=10)
        self.sign_btn.config(state=DISABLED)

        # --- Left Panel: Player List ---
        # REFINED: 3. This panel will now be taller due to the smaller banner.
        left_panel = Frame(content, bg=self.COLOR_BG, highlightbackground=self.COLOR_BORDER, highlightthickness=1)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=self.COLOR_BG, fieldbackground=self.COLOR_BG, foreground=self.COLOR_TEXT, rowheight=28, relief="none", borderwidth=0)
        style.map('Treeview', background=[('selected', self.COLOR_ACCENT)], foreground=[('selected', self.COLOR_ACCENT_FG)])
        style.configure("Treeview.Heading", background=self.COLOR_HEADER_BG, foreground=self.COLOR_TEXT, font=("Helvetica", 11, "bold"), relief="flat")
        
        self.player_tree = ttk.Treeview(left_panel, show="headings", columns=("Name", "Position"), selectmode="browse")
        self.player_tree.column("Name", anchor="w", width=250, stretch=True)
        self.player_tree.column("Position", anchor="center", width=150, stretch=True)
        self.player_tree.heading("Name", text="Name", anchor="w")
        self.player_tree.heading("Position", text="Position", anchor="center")
        self.player_tree.bind("<<TreeviewSelect>>", self.on_player_select)
        self.player_tree.grid(row=0, column=0, sticky="nsew")

        # --- Right Panel: Active Team ---
        # REFINED: 3. This panel will also be taller.
        right_panel = Frame(content, bg=self.COLOR_BG, highlightbackground=self.COLOR_BORDER, highlightthickness=1)
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)

        title = Frame(right_panel, bg=self.COLOR_HEADER_BG, height=35)
        title.pack(fill="x")
        Label(title, text="Active Team", bg=self.COLOR_HEADER_BG, fg=self.COLOR_TEXT,
              font=("Helvetica", 12, "bold")).pack(side=LEFT, padx=15, pady=5)
        
        body = Frame(right_panel, bg=self.COLOR_BG)
        body.pack(fill="both", expand=True, padx=20, pady=20)

        team_jersey_path = f"image/{self.team.get_jersey_filename()}"
        self.team_jersey_img = ut.image(self.root, team_jersey_path, height=64, width=64).photo
        self.no_team_jersey_img = ut.image(self.root, "image/none.png", height=64, width=64).photo

        gridf = Frame(body, bg=self.COLOR_BG)
        gridf.pack(expand=True)
        for c in (0, 4): gridf.grid_columnconfigure(c, weight=1)
        for r in (0, 2): gridf.grid_rowconfigure(r, weight=1)
        jersey_pos = [(0, 2), (1, 1), (1, 2), (1, 3), (2, 2)]
        for i in range(5):
            btn = ut.button(gridf, "", lambda idx=i: self.on_jersey_click(idx))
            btn.config(image=self.no_team_jersey_img, background=self.COLOR_BG, borderwidth=0, highlightthickness=0)
            btn.unbind("<Enter>")
            btn.unbind("<Leave>")
            r, c = jersey_pos[i]
            btn.grid(row=r, column=c, padx=10, pady=10)
            self.jersey_buttons.append(btn)

        # ============================ FOOTER ============================
        footer = Frame(self.root, bg=self.COLOR_BG)
        footer.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        footer.grid_columnconfigure(0, weight=1)
        footer.grid_columnconfigure(1, weight=1)

        self.unsign_button = ut.button(footer, "Unsign", self.unsign_player)
        self.unsign_button.grid(row=0, column=0, sticky="ew", padx=(0, 10), ipady=5)
        self.unsign_button.config(state=DISABLED)

        close_btn = ut.button(footer, "Close", self.close)
        close_btn.grid(row=0, column=1, sticky="ew", padx=(10, 0), ipady=5)

        self.update_view()

    def _toggle_sign_button(self, _evt=None):
        self.sign_btn.config(state=NORMAL if self.player_name_var.get().strip() else DISABLED)

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
        except InvalidSigningException as e: ErrorView("InvalidSigningException", str(e))

    def on_player_select(self, _evt):
        sel = self.player_tree.selection()
        if not sel:
            self.selected_player_from_table = None
            self.unsign_button.config(state=DISABLED)
            return
        name = self.player_tree.item(sel[0])["values"][0]
        self.selected_player_from_table = self.team.get_all_players().player(name)
        self.unsign_button.config(state=NORMAL)

    def on_jersey_click(self, idx):
        player_at_pos = self.team.get_current_team()[idx]
        if self.selected_player_from_table:
            try: self.team.assign_player_to_position(self.selected_player_from_table, idx)
            except FillException as e: ErrorView("FillException", str(e))
        elif player_at_pos: self.team.unassign_player_from_position(idx)
        self.update_view()

    def close(self):
        self.root.master.deiconify()
        self.root.destroy()

    def update_view(self):
        for i in self.player_tree.get_children(): self.player_tree.delete(i)
        players = sorted(self.team.get_all_players().get_players(), key=lambda p: p.get_full_name())
        for p in players:
            self.player_tree.insert("", "end", values=(p.get_full_name(), str(p.get_position())))

        active = self.team.get_current_team()
        for i, player in enumerate(active):
            img = self.team_jersey_img if player else self.no_team_jersey_img
            self.jersey_buttons[i].config(image=img)

        self.selected_player_from_table = None
        self.unsign_button.config(state=DISABLED)
        if self.player_tree.selection():
            self.player_tree.selection_remove(self.player_tree.selection())