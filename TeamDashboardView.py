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
        self.MIN_ROWS = 17

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
        self.COLOR_PINK = "#E87A7A"

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
        
        team_name_label = Label(header, text=str(self.team), bg=self.COLOR_BG, fg=self.COLOR_PINK, font=("Helvetica", 16, "bold"))
        team_name_label.pack(pady=10)

        # ============================ CONTENT BODY ============================
        content = Frame(self.root, bg=self.COLOR_BG)
        content.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        content.grid_columnconfigure(0, weight=40)
        content.grid_columnconfigure(1, weight=60)
        content.grid_rowconfigure(1, weight=1)

        # --- Sign Player Row ---
        # REFINED: 1. Center the "Sign a new player" section.
        # The outer frame spans the grid, and the inner frame uses pack() to center its contents by default.
        sign_row_container = Frame(content, bg=self.COLOR_BG)
        sign_row_container.grid(row=0, column=0, columnspan=2, pady=(5, 15))
        sign_row = Frame(sign_row_container, bg=self.COLOR_BG)
        sign_row.pack() # This pack() call centers the sign_row frame

        Label(sign_row, text="Sign a new player:", bg=self.COLOR_BG,
            fg=self.COLOR_PINK, font=("Helvetica", 16, "bold")).pack(side=LEFT, padx=(0, 10)) 
        entry = Entry(sign_row, textvariable=self.player_name_var, width=35, font=("Helvetica", 11), relief="solid", bd=1)
        entry.bind("<KeyRelease>", self._toggle_sign_button)
        entry.bind("<Return>", self.sign_player)
        entry.pack(side=LEFT)
        self.sign_btn = ut.button(sign_row, "Sign", self.sign_player)
        self.sign_btn.pack(side=LEFT, padx=10)
        self.sign_btn.config(state=DISABLED)

        # # --- Left Panel: Player List ---
        # # REFINED: 3. This panel will now be taller due to the smaller banner.
        # left_panel = Frame(content, bg=self.COLOR_BG, highlightbackground=self.COLOR_BORDER, highlightthickness=1)
        # left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 10))


        # # left_panel.grid_columnconfigure(0, weight=1)
        # # left_panel.grid_rowconfigure(0, weight=1)

        # style = ttk.Style()
        # style.theme_use("clam")
        # style.configure("Treeview", background=self.COLOR_BG, fieldbackground=self.COLOR_BG, foreground=self.COLOR_TEXT, rowheight=28, relief="none", borderwidth=0)
        # style.map('Treeview', background=[('selected', self.COLOR_ACCENT)], foreground=[('selected', self.COLOR_ACCENT_FG)])
        # style.configure("Treeview.Heading", background=self.COLOR_HEADER_BG, foreground=self.COLOR_PINK,font=("Helvetica", 16, "bold"), relief="flat")
        # self.player_tree = ttk.Treeview(left_panel, show="headings", columns=("Name", "Position"), selectmode="browse",height=15)
      
      
        # # self.player_tree.column("Name", anchor="w", width=250, stretch=True)
        # # self.player_tree.column("Position", anchor="center", width=150, stretch=True)

        # self.player_tree.column("Name", anchor="w", width=180, stretch=False)
        # self.player_tree.column("Position", anchor="center", width=180, stretch=False)
        
        
        # self.player_tree.heading("Name", text="Name", anchor="w")
        # self.player_tree.heading("Position", text="Position", anchor="center")
        # self.player_tree.bind("<<TreeviewSelect>>", self.on_player_select)
        # self.player_tree.pack(fill="x", expand=False, padx=1, pady=1)


        # --- Left Panel: Player List ---
        # --- Left Panel: Player List ---
        # --- Left Panel: Player List ---
  # --- Left Panel: Player List ---
                # --- Left Panel: Player List ---
        left_panel = Frame(content, bg=self.COLOR_BG,
                        highlightbackground=self.COLOR_BORDER, highlightthickness=1)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("clam")

# 行高/字体（内容）
        style.configure("Players.Treeview",
            background=self.COLOR_BG,
            fieldbackground=self.COLOR_BG,
            foreground=self.COLOR_TEXT,
            font=("Helvetica", 12),
            rowheight=22,
            borderwidth=0
        )
        # 选中样式
        style.map("Players.Treeview",
            background=[('selected', self.COLOR_ACCENT)],
            foreground=[('selected', self.COLOR_ACCENT_FG)]
        )

        # 表头样式 —— 与 “Sign a new player” 保持一致（粉色、16、bold）
        style.configure("Players.Treeview.Heading",
            background="#f1f1f1",
            foreground=self.COLOR_PINK,
            font=("Helvetica", 16, "bold"),
            padding=(6, 4, 6, 4),
            relief="flat"
        )

# 不要滚动条：不创建 Scrollbar，也不设置 yscrollcommand
        self.player_tree = ttk.Treeview(
            left_panel,
            style="Players.Treeview",
            show="headings",
            columns=("Name", "Position"),
            selectmode="browse"
        )
        self.player_tree.grid(row=0, column=0, sticky="nsew")

# 表头与单元格都居中；两列都允许拉伸
        self.player_tree.heading("Name", text="Name", anchor="center")
        self.player_tree.heading("Position", text="Position", anchor="center")
        self.player_tree.column("Name", anchor="center", stretch=True, width=200)
        self.player_tree.column("Position", anchor="center", stretch=True, width=200)

# 斑马纹
        self.player_tree.tag_configure("even", background=self.COLOR_BG)
        self.player_tree.tag_configure("odd",  background="#fafafa")

# 随容器尺寸变化时，自动把两列调成等宽
        self.player_tree.bind("<Configure>", self._on_tree_resize)

        self.player_tree.bind("<<TreeviewSelect>>", self.on_player_select)







        
        # In TeamDashboardView.py

        # --- Right Panel: Active Team ---

        
        right_panel = Frame(content, bg=self.COLOR_BG, highlightbackground=self.COLOR_BORDER, highlightthickness=1)
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)

        # 1. 修正：创建 Active Team 标题栏
        title = Frame(right_panel, bg="black", height=40)
        title.grid(row=0, column=0, sticky="ew") # 使用 grid 布局
        title.pack_propagate(False)
        title.grid_columnconfigure(0, weight=1)
        active_team_label = Label(title, text="Active Team", bg="black", fg=self.COLOR_PINK, font=("Helvetica", 16, "bold"))
        active_team_label.grid(row=0, column=0)

        # 2. 修正：创建球衣区域的 body，并统一使用 grid 布局
        body = Frame(right_panel, bg=self.COLOR_BG)
        body.grid(row=1, column=0, sticky="nsew", padx=20, pady=20) # 使用 grid 布局

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
# 关键：padx 从 20 改成 0，pady 也可收紧
        footer.grid(row=2, column=0, sticky="ew", padx=0, pady=(10, 0))

        # 两列等宽
        footer.grid_columnconfigure(0, weight=1)
        footer.grid_columnconfigure(1, weight=1)

        # 左右按钮贴边，中间留一点间距；只横向拉伸，保持原有高度(ipady)
        self.unsign_button = ut.button(footer, "Unsign", self.unsign_player)
        self.unsign_button.grid(row=0, column=0, sticky="ew", padx=0, ipady=5)

        close_btn = ut.button(footer, "Close", self.close)
        close_btn.grid(row=0, column=1, sticky="ew", padx=0, ipady=5)


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


      

    def _on_tree_resize(self, event):
    # 让 Name 与 Position 始终各占 50%
        total = max(event.width - 2, 1)  # 去掉边线的微小误差
        col_w = total // 2
        try:
            self.player_tree.column("Name", width=col_w)
            self.player_tree.column("Position", width=col_w)
        except Exception:
            pass


    def update_view(self):
        for i in self.player_tree.get_children():
            self.player_tree.delete(i)

    # —— 插入真实玩家行 ——
        players = sorted(self.team.get_all_players().get_players(),
                        key=lambda p: p.get_full_name())
        for idx, p in enumerate(players):
            zebra = "odd" if idx % 2 else "even"
            self.player_tree.insert(
                "", "end",
                values=(p.get_full_name(), str(p.get_position())),
                tags=(zebra,)
            )

    # —— 追加占位行，直到达到 MIN_ROWS —— 
        total = len(self.player_tree.get_children())
        need = max(0, self.MIN_ROWS - total)
        for i in range(need):
            row_index = total + i
            zebra = "odd" if row_index % 2 else "even"
            # 占位行 values 用空字符串；加上 'placeholder' tag 以便禁止选择
            self.player_tree.insert(
                "", "end",
                values=("", ""),
                tags=(zebra, "placeholder")
            )

        
       
        active = self.team.get_current_team()
        for i, player in enumerate(active):
            img = self.team_jersey_img if player else self.no_team_jersey_img
            self.jersey_buttons[i].config(image=img)

        self.selected_player_from_table = None
        
        if self.player_tree.selection():
            self.player_tree.selection_remove(self.player_tree.selection())