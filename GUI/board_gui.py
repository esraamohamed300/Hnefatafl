import tkinter as tk
from tkinter import messagebox
import Core.rules as rules

CELL_SIZE = 72
BOARD_SIZE = 9
PADDING = 50  # space for labels

EMPTY = 0
ATTACKER = 1
DEFENDER = 2
KING = 3

# ── Norse colour palette ──────────────────────────────────────────────────────
BG          = "#1a1208"   # almost-black parchment
BOARD_LIGHT = "#c8a96e"   # warm sand
BOARD_DARK  = "#b8935a"   # darker sand (checkerboard feel)
CORNER_CLR  = "#3d1f0a"   # deep mahogany
THRONE_CLR  = "#8b0000"   # blood red
GRID_LINE   = "#7a5c30"   # warm brown grid
LABEL_CLR   = "#e8c98a"   # golden label text
STATUS_BG   = "#0f0b05"
HIGHLIGHT   = "#ffe066"   # yellow selection
MOVE_DOT    = "#66ffcc"   # valid move hint dot

ATK_FILL    = "#1a1a2e"   # dark navy attacker
ATK_RIM     = "#e94560"   # red rim
DEF_FILL    = "#f0ead6"   # ivory defender
DEF_RIM     = "#4a90d9"   # blue rim
KING_FILL   = "#ffd700"   # gold king
KING_RIM    = "#ff8c00"   # amber rim
SHADOW      = "#222222"

CORNER_RUNE = "ᚠ"   # decorative rune on corners
THRONE_RUNE = "᛭"   # throne marker


class BoardGUI:
    def __init__(self, root):
        self.root = root
        root.configure(bg=BG)
        root.resizable(True, True)

        total_w = CELL_SIZE * BOARD_SIZE + PADDING * 2
        total_h = CELL_SIZE * BOARD_SIZE + PADDING * 2 + 60  # +60 for status bar

        # ── canvas ────────────────────────────────────────────────────────────
        self.canvas = tk.Canvas(
            root,
            width=total_w,
            height=total_h - 60,
            bg=BG,
            highlightthickness=0
        )
        self.canvas.pack(pady=(16, 0))

        # ── status bar ────────────────────────────────────────────────────────
        self.status_frame = tk.Frame(root, bg=STATUS_BG, height=52)
        self.status_frame.pack(fill="x", padx=0, pady=0)
        self.status_frame.pack_propagate(False)

        self.turn_indicator = tk.Canvas(
            self.status_frame, width=18, height=18,
            bg=STATUS_BG, highlightthickness=0
        )
        self.turn_indicator.pack(side="left", padx=(20, 8), pady=16)

        self.status_label = tk.Label(
            self.status_frame,
            text="ATTACKER'S TURN",
            font=("Georgia", 13, "bold"),
            fg=ATK_RIM,
            bg=STATUS_BG
        )
        self.status_label.pack(side="left", pady=10)

        self.move_label = tk.Label(
            self.status_frame,
            text="",
            font=("Georgia", 10),
            fg="#888877",
            bg=STATUS_BG
        )
        self.move_label.pack(side="right", padx=20, pady=16)

        # ── state ─────────────────────────────────────────────────────────────
        self.board = self._create_initial_board()
        self.selected = None
        self.valid_moves = []
        self.turn = "ATTACKER"
        self.move_count = 0
        self.hovered = None  # must be before draw_board()

        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_hover)

    # ── board setup ───────────────────────────────────────────────────────────
    def _create_initial_board(self):
        board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        board[4][4] = KING
        for r, c in [(4,3),(4,5),(3,4),(5,4),(4,2),(4,6),(2,4),(6,4),(3,3),(3,5),(5,3),(5,5)]:
            board[r][c] = DEFENDER
        for r, c in [
            (0,3),(0,4),(0,5),(0,2),(0,6),(1,4),
            (8,3),(8,4),(8,5),(8,2),(8,6),(7,4),
            (3,0),(4,0),(5,0),(2,0),(6,0),(4,1),
            (3,8),(4,8),(5,8),(2,8),(6,8),(4,7),
        ]:
            board[r][c] = ATTACKER
        return board

    # ── coordinate helpers ────────────────────────────────────────────────────
    def _xy(self, row, col):
        x = col * CELL_SIZE + PADDING
        y = row * CELL_SIZE + PADDING
        return x, y

    def _rc(self, x, y):
        col = (x - PADDING) // CELL_SIZE
        row = (y - PADDING) // CELL_SIZE
        return row, col

    # ── drawing ───────────────────────────────────────────────────────────────
    def draw_board(self):
        self.canvas.delete("all")
        self._draw_background()
        self._draw_cells()
        self._draw_grid()
        self._draw_labels()
        self._draw_pieces()

    def _draw_background(self):
        w = CELL_SIZE * BOARD_SIZE + PADDING * 2
        h = CELL_SIZE * BOARD_SIZE + PADDING * 2
        # outer glow / border
        for i in range(6, 0, -1):
            self.canvas.create_rectangle(
                PADDING - 6 - i, PADDING - 6 - i,
                PADDING + CELL_SIZE * BOARD_SIZE + 6 + i,
                PADDING + CELL_SIZE * BOARD_SIZE + 6 + i,
                outline=f"#{'%02x' % (40 + i*8)}3a10",
                width=1
            )
        # board shadow
        self.canvas.create_rectangle(
            PADDING + 4, PADDING + 4,
            PADDING + CELL_SIZE * BOARD_SIZE + 4,
            PADDING + CELL_SIZE * BOARD_SIZE + 4,
            fill="#111111", outline=""
        )

    def _draw_cells(self):
        corners = {(0,0),(0,8),(8,0),(8,8)}
        throne  = (4, 4)

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1, y1 = self._xy(row, col)
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

                # base colour
                if (row, col) in corners:
                    color = CORNER_CLR
                elif (row, col) == throne:
                    color = THRONE_CLR
                else:
                    # subtle checkerboard
                    color = BOARD_LIGHT if (row + col) % 2 == 0 else BOARD_DARK

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

                # selected highlight
                if self.selected == (row, col):
                    self.canvas.create_rectangle(
                        x1+2, y1+2, x2-2, y2-2,
                        outline=HIGHLIGHT, width=3, fill=""
                    )

                # valid move dots
                if (row, col) in self.valid_moves:
                    cx, cy = x1 + CELL_SIZE//2, y1 + CELL_SIZE//2
                    r = 8
                    self.canvas.create_oval(
                        cx-r, cy-r, cx+r, cy+r,
                        fill=MOVE_DOT, outline="", stipple=""
                    )

                # hover highlight
                if self.hovered == (row, col) and (row, col) not in self.valid_moves:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        outline="#888866", width=1, fill="#d4c090"
                    )

                # corner rune
                if (row, col) in corners:
                    cx, cy = x1 + CELL_SIZE//2, y1 + CELL_SIZE//2
                    self.canvas.create_text(
                        cx, cy, text=CORNER_RUNE,
                        fill="#c8813a", font=("Georgia", 20, "bold")
                    )

                # throne rune
                if (row, col) == throne and self.board[row][col] == EMPTY:
                    cx, cy = x1 + CELL_SIZE//2, y1 + CELL_SIZE//2
                    self.canvas.create_text(
                        cx, cy, text=THRONE_RUNE,
                        fill="#ff6666", font=("Georgia", 22, "bold")
                    )

    def _draw_grid(self):
        total = CELL_SIZE * BOARD_SIZE
        for i in range(BOARD_SIZE + 1):
            x = PADDING + i * CELL_SIZE
            y = PADDING + i * CELL_SIZE
            self.canvas.create_line(PADDING, y, PADDING+total, y, fill=GRID_LINE, width=1)
            self.canvas.create_line(x, PADDING, x, PADDING+total, fill=GRID_LINE, width=1)

        # thick border
        self.canvas.create_rectangle(
            PADDING, PADDING,
            PADDING + total, PADDING + total,
            outline="#5a3a10", width=3, fill=""
        )

    def _draw_labels(self):
        for i in range(BOARD_SIZE):
            # row numbers (left)
            self.canvas.create_text(
                PADDING - 18,
                PADDING + i * CELL_SIZE + CELL_SIZE // 2,
                text=str(BOARD_SIZE - i),
                fill=LABEL_CLR,
                font=("Georgia", 11, "bold")
            )
            # col letters (bottom)
            self.canvas.create_text(
                PADDING + i * CELL_SIZE + CELL_SIZE // 2,
                PADDING + BOARD_SIZE * CELL_SIZE + 18,
                text=chr(ord('A') + i),
                fill=LABEL_CLR,
                font=("Georgia", 11, "bold")
            )

    def _draw_pieces(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece != EMPTY:
                    self._draw_piece(row, col, piece)

    def _draw_piece(self, row, col, piece):
        x1, y1 = self._xy(row, col)
        cx = x1 + CELL_SIZE // 2
        cy = y1 + CELL_SIZE // 2
        R = 26

        is_sel = self.selected == (row, col)

        if piece == ATTACKER:
            fill, rim = ATK_FILL, ATK_RIM
        elif piece == DEFENDER:
            fill, rim = DEF_FILL, DEF_RIM
        else:
            fill, rim = KING_FILL, KING_RIM

        # drop shadow
        self.canvas.create_oval(
            cx-R+3, cy-R+4, cx+R+3, cy+R+4,
            fill="#222222", outline=""
        )

        # glow ring when selected
        if is_sel:
            self.canvas.create_oval(
                cx-R-5, cy-R-5, cx+R+5, cy+R+5,
                fill="", outline=HIGHLIGHT, width=3
            )

        # outer rim
        self.canvas.create_oval(
            cx-R, cy-R, cx+R, cy+R,
            fill=rim, outline=""
        )

        # inner body
        self.canvas.create_oval(
            cx-R+3, cy-R+3, cx+R-3, cy+R-3,
            fill=fill, outline=""
        )

        # shine spot
        self.canvas.create_oval(
            cx-R//3, cy-R//2, cx, cy-R//5,
            fill="#cccccc", outline=""
        )

        # king crown emoji
        if piece == KING:
            self.canvas.create_text(
                cx, cy,
                text="♛",
                fill="#3d1f0a",
                font=("Georgia", 18, "bold")
            )

    # ── status bar update ─────────────────────────────────────────────────────
    def _update_status(self):
        if self.turn == "ATTACKER":
            txt   = "ATTACKER'S TURN"
            color = ATK_RIM
            dot   = ATK_FILL
            dot_outline = ATK_RIM
        else:
            txt   = "DEFENDER'S TURN"
            color = "#4a90d9"
            dot   = DEF_FILL
            dot_outline = DEF_RIM

        self.status_label.config(text=txt, fg=color)
        self.move_label.config(text=f"Move {self.move_count}")

        self.turn_indicator.delete("all")
        self.turn_indicator.create_oval(1, 1, 17, 17, fill=dot, outline=dot_outline, width=5)

    # ── interaction ───────────────────────────────────────────────────────────
    def on_hover(self, event):
        row, col = self._rc(event.x, event.y)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            if self.hovered != (row, col):
                self.hovered = (row, col)
                self.draw_board()
        else:
            if self.hovered is not None:
                self.hovered = None
                self.draw_board()

    def _get_valid_moves(self, row, col):
        moves = []
        for tr in range(BOARD_SIZE):
            for tc in range(BOARD_SIZE):
                if rules.is_valid_move(self.board, row, col, tr, tc):
                    moves.append((tr, tc))
        return moves

    def on_click(self, event):
        row, col = self._rc(event.x, event.y)

        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return

        if self.selected is None:
            piece = self.board[row][col]
            if (self.turn == "ATTACKER" and piece == ATTACKER) or \
               (self.turn == "DEFENDER" and piece in (DEFENDER, KING)):
                self.selected = (row, col)
                self.valid_moves = self._get_valid_moves(row, col)
            self.draw_board()
            return

        sr, sc = self.selected

        if rules.is_valid_move(self.board, sr, sc, row, col):
            self.board[row][col] = self.board[sr][sc]
            self.board[sr][sc] = EMPTY
            self.move_count += 1

            rules.apply_capture(self.board, row, col)

            self.selected = None
            self.valid_moves = []
            self.draw_board()

            if rules.is_king_win(self.board):
                self._update_status()
                messagebox.showinfo("⚔  Game Over", "The King has escaped!\nDefenders Win!")
                return

            if rules.is_king_captured(self.board):
                self._update_status()
                messagebox.showinfo("⚔  Game Over", "The King has been captured!\nAttackers Win!")
                return

            self.turn = "DEFENDER" if self.turn == "ATTACKER" else "ATTACKER"
            self._update_status()

        else:
            # clicked a different friendly piece → re-select
            piece = self.board[row][col]
            if (self.turn == "ATTACKER" and piece == ATTACKER) or \
               (self.turn == "DEFENDER" and piece in (DEFENDER, KING)):
                self.selected = (row, col)
                self.valid_moves = self._get_valid_moves(row, col)
            else:
                self.selected = None
                self.valid_moves = []

        self.draw_board()