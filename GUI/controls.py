import tkinter as tk


# ── Norse colour palette ──────────────────────────────────────────────────────
BG          = "#0d0a05"
BG2         = "#150f08"
GOLD        = "#c8973a"
GOLD_LIGHT  = "#ffd700"
GOLD_DIM    = "#7a5c20"
TEXT        = "#e8d5a3"
TEXT_DIM    = "#7a6a4a"
RED         = "#8b1a1a"
RED_LIGHT   = "#c0392b"
BLUE        = "#1a3a5c"
BLUE_LIGHT  = "#2980b9"
BTN_BG      = "#1c1208"
BTN_HOVER   = "#2a1c0a"
BORDER      = "#3d2a10"
BORDER_GOLD = "#c8973a"
SELECT_BG   = "#2a1c0a"
RUNE_CLR    = "#3d2a10"


def _make_btn(parent, text, command, width=220, height=44, style="gold"):
    
    fg     = GOLD_LIGHT if style == "gold" else TEXT
    bg_n   = BTN_BG
    bg_h   = BTN_HOVER
    bdr    = BORDER_GOLD if style == "gold" else BORDER

    c = tk.Canvas(parent, width=width, height=height,
                  bg=parent["bg"], highlightthickness=0, cursor="hand2")

    def _draw(hover=False):
        c.delete("all")
        bg = bg_h if hover else bg_n
        
        c.create_rectangle(0, 0, width-1, height-1,
                           fill=bg, outline=bdr, width=2)
       
        c.create_rectangle(3, 3, width-4, height-4,
                           fill="", outline=RUNE_CLR, width=1)
        
        for ox, oy in [(6,6),(width-6,6),(6,height-6),(width-6,height-6)]:
            c.create_oval(ox-2, oy-2, ox+2, oy+2, fill=GOLD_DIM, outline="")
        
        c.create_text(width//2, height//2, text=text,
                      fill=fg, font=("Georgia", 11, "bold"))

    _draw()
    c.bind("<Enter>",    lambda e: _draw(True))
    c.bind("<Leave>",    lambda e: _draw(False))
    c.bind("<Button-1>", lambda e: command())
    return c


def _divider(parent, width=420):
   
    c = tk.Canvas(parent, width=width, height=20,
                  bg=parent["bg"], highlightthickness=0)
    mid = width // 2
    c.create_line(0, 10, mid-30, 10, fill=BORDER_GOLD, width=1)
    c.create_text(mid, 10, text="᛫ ᚷ ᛫", fill=GOLD_DIM, font=("Georgia", 9))
    c.create_line(mid+30, 10, width, 10, fill=BORDER_GOLD, width=1)
    return c

class _ToggleGroup:
    def __init__(self, parent, options, variable, btn_width=170):
        self.variable  = variable
        self.buttons   = {}
        self.texts     = {}  
        self.frame     = tk.Frame(parent, bg=parent["bg"])

        for text, val in options:
            self.texts[val] = text 
            c = tk.Canvas(self.frame, width=btn_width, height=46,
                          bg=parent["bg"], highlightthickness=0, cursor="hand2")
            self.buttons[val] = c
            c.pack(side="left", padx=8)

            def _draw(canvas=c, value=val):
                canvas.delete("all")
                selected = self.variable.get() == value
                bg  = SELECT_BG  if selected else BTN_BG
                bdr = GOLD       if selected else BORDER
                fg  = GOLD_LIGHT if selected else TEXT_DIM
                canvas.create_rectangle(0, 0, btn_width-1, 45,
                                        fill=bg, outline=bdr, width=2)
                if selected:
                    canvas.create_line(4, 1, btn_width-4, 1,
                                       fill=GOLD_LIGHT, width=1)
                
                canvas.create_text(btn_width//2, 23, text=self.texts[value],
                                   fill=fg, font=("Georgia", 10, "bold"))

            def _click(value=val):
                self.variable.set(value)
                self._refresh()

            c.bind("<Button-1>", lambda e, cl=_click: cl())
            c.bind("<Enter>",    lambda e, d=_draw: d())
            c.bind("<Leave>",    lambda e, d=_draw: d())
            _draw()

        variable.trace("w", lambda *a: self._refresh())

    def _refresh(self):
        for val, canvas in self.buttons.items():
            canvas.delete("all")
            w, h     = int(canvas["width"]), int(canvas["height"])
            selected = self.variable.get() == val
            bg  = SELECT_BG  if selected else BTN_BG
            bdr = GOLD       if selected else BORDER
            fg  = GOLD_LIGHT if selected else TEXT_DIM
            canvas.create_rectangle(0, 0, w-1, h-1,
                                    fill=bg, outline=bdr, width=2)
            if selected:
                canvas.create_line(4, 1, w-4, 1, fill=GOLD_LIGHT, width=1)
            #  use stored text
            canvas.create_text(w//2, h//2, text=self.texts[val],
                                fill=fg, font=("Georgia", 10, "bold"))

    def pack(self, **kw):
        self.frame.pack(**kw)


#  HOME PAGE

class HomePage(tk.Frame):
    def __init__(self, parent, on_new_game):
        super().__init__(parent, bg=BG)
        self.on_new_game = on_new_game
        self._build()

    def _build(self):
        # top spacer
        tk.Frame(self, bg=BG, height=30).pack()

        # ── rune banner ───────────────────────────────────────────────────────
        banner = tk.Canvas(self, width=520, height=80,
                           bg=BG, highlightthickness=0)
        banner.pack()
        banner.create_text(260, 28, text="ᚺᚾᛖᚠᚨᛏᚨᚠᛚ",
                           fill=GOLD, font=("Georgia", 30, "bold"))
        banner.create_text(260, 60, text="— VIKING CHESS —",
                           fill=TEXT_DIM, font=("Georgia", 11, "italic"))

        # ── decorative border box ─────────────────────────────────────────────
        box = tk.Canvas(self, width=480, height=220,
                        bg=BG2, highlightthickness=0)
        box.pack(pady=18)

        # border
        box.create_rectangle(2, 2, 477, 217, outline=BORDER_GOLD, width=1)
        box.create_rectangle(6, 6, 473, 213, outline=BORDER,      width=1)

        # corner runes
        for rx, ry, txt in [(18,18,"ᚠ"),(462,18,"ᚠ"),(18,202,"ᚠ"),(462,202,"ᚠ")]:
            box.create_text(rx, ry, text=txt, fill=GOLD_DIM,
                            font=("Georgia", 13, "bold"))

        # description text
        lines = [
            "An ancient Norse strategy game of siege and escape.",
            "",
            "The Defender guides the King to one of the four corners.",
            "The Attacker surrounds and captures the King.",
            "",
            "All pieces move like the Rook in Chess.",
            "Capture by sandwiching an enemy between two of your own.",
        ]
        y = 28
        for line in lines:
            if line == "":
                y += 8
                continue
            box.create_text(240, y, text=line, fill=TEXT,
                            font=("Georgia", 10), width=440)
            y += 22

        # ── divider ───────────────────────────────────────────────────────────
        _divider(self).pack(pady=4)

        # ── new game button ───────────────────────────────────────────────────
        _make_btn(self, "⚔   NEW GAME", self.on_new_game,
                  width=240, height=50).pack(pady=16)

        # ── footer ────────────────────────────────────────────────────────────
        tk.Label(self, text="ᚺᚾᛖᚠᚨᛏᚨᚠᛚ  —  ᛏᚺᛖ ᚨᚾᚲᛁᛖᚾᛏ ᚷᚨᛗᛖ ᛟᚠ ᚲᛁᚾᚷᛊ",
                 font=("Georgia", 8), fg=TEXT_DIM, bg=BG).pack(pady=(4, 0))



#  SETTINGS PAGE

class SettingsPage(tk.Frame):
    def __init__(self, parent, on_start_game, on_back):
        super().__init__(parent, bg=BG)
        self.on_start_game = on_start_game
        self.on_back       = on_back

        self.mode       = tk.StringVar(value="Human")
        self.side       = tk.StringVar(value="ATTACKER")
        self.difficulty = tk.StringVar(value="Medium")

        self._build()

    def _build(self):
        tk.Frame(self, bg=BG, height=20).pack()

        # ── title ─────────────────────────────────────────────────────────────
        tk.Label(self, text="GAME SETTINGS",
                 font=("Georgia", 20, "bold"),
                 fg=GOLD, bg=BG).pack()

        _divider(self).pack(pady=8)

        # ── section: opponent ─────────────────────────────────────────────────
        self._section_label("Choose Opponent")
        opp = _ToggleGroup(
            self,
            [("👤   Human vs Human", "Human"),
             ("🤖   Human vs Computer", "AI")],
            self.mode, btn_width=190
        )
        opp.pack(pady=(4, 14))

        # ── section: side ─────────────────────────────────────────────────────
        self._section_label("Choose Your Side")
        side = _ToggleGroup(
            self,
            [("⚔   Attacker  (Black)", "ATTACKER"),
             ("🛡   Defender  (White)", "DEFENDER")],
            self.side, btn_width=190
        )
        side.pack(pady=(4, 14))

        # ── section: difficulty ───────────────────────────────────────────────
        self.diff_title = self._section_label("Difficulty", return_it=True)
        diff = _ToggleGroup(
            self,
            [("🌿  Easy", "Easy"), ("⚔  Medium", "Medium"), ("💀  Hard", "Hard")],
            self.difficulty, btn_width=120
        )
        self.diff_frame = diff.frame
        diff.pack(pady=(4, 14))

        self.mode.trace("w", self._toggle_diff)
        self._toggle_diff()

        _divider(self).pack(pady=8)

        # ── bottom buttons ────────────────────────────────────────────────────
        row = tk.Frame(self, bg=BG)
        row.pack(pady=10)
        _make_btn(row, "◀   Back",        self.on_back,
                  width=160, height=44, style="dim").pack(side="left", padx=10)
        _make_btn(row, "▶   Start Game",  self._start,
                  width=200, height=44, style="gold").pack(side="left", padx=10)

        tk.Frame(self, bg=BG, height=10).pack()

    def _section_label(self, text, return_it=False):
        lbl = tk.Label(self, text=text,
                       font=("Georgia", 11, "bold"),
                       fg=GOLD_DIM, bg=BG)
        lbl.pack(pady=(2, 2))
        if return_it:
            return lbl

    def _toggle_diff(self, *args):
        if self.mode.get() == "AI":
            self.diff_title.pack()
            self.diff_frame.pack(pady=(4, 14))
        else:
            self.diff_title.pack_forget()
            self.diff_frame.pack_forget()

    def _start(self):
        self.on_start_game(
            mode       = self.mode.get(),
            side       = self.side.get(),
            difficulty = self.difficulty.get()
        )