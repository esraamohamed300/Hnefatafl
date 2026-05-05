import tkinter as tk
from tkinter import messagebox
import Core.rules as rules
from Core.game_state import GameState
from AI.ai_player import AIPlayer
from utils.helpers import EMPTY, ATTACKER, DEFENDER, KING, BOARD_SIZE, CORNERS, SPECIAL_SQUARES

CELL_SIZE  = 72
PADDING    = 50
# ── Norse colour palette ──────────────────────────────────────────────────────
BG          = "#1a1208"
BOARD_LIGHT = "#c8a96e"
BOARD_DARK  = "#b8935a"
CORNER_CLR  = "#3d1f0a"
THRONE_CLR  = "#8b0000"
GRID_LINE   = "#7a5c30"
LABEL_CLR   = "#e8c98a"
STATUS_BG   = "#0f0b05"
HIGHLIGHT   = "#ffe066"
MOVE_DOT    = "#66ffcc"
ATK_FILL  = "#1a1a2e"
ATK_RIM   = "#e94560"
DEF_FILL  = "#f0ead6"
DEF_RIM   = "#4a90d9"
KING_FILL = "#ffd700"
KING_RIM  = "#ff8c00"

CORNER_RUNE = "ᚠ"
THRONE_RUNE = "᛭"


class BoardGUI(tk.Frame):
    def __init__(self, parent, mode, human_side, difficulty, on_end_game):
        super().__init__(parent, bg=BG)

        self.mode        = mode          # "Human" or "AI"
        self.human_side  = human_side    # "ATTACKER" or "DEFENDER"
        self.difficulty  = difficulty    # "Easy", "Medium", "Hard"
        self.on_end_game = on_end_game   # callback → returns to home page

        # ── AI setup ──────────────────────────────────────────────────────────
        if self.mode == "AI":
            ai_side   = "DEFENDER" if human_side == "ATTACKER" else "ATTACKER"
            self.ai   = AIPlayer(ai_side, difficulty)
        else:
            self.ai   = None

        # ── canvas ────────────────────────────────────────────────────────────
        self.canvas = tk.Canvas(
            self,
            width  = CELL_SIZE * BOARD_SIZE + PADDING * 2,
            height = CELL_SIZE * BOARD_SIZE + PADDING * 2,
            bg     = BG,
            highlightthickness = 0
        )
        self.canvas.pack(pady=(10, 0))

        # ── status bar ────────────────────────────────────────────────────────
        self.status_frame = tk.Frame(self, bg=STATUS_BG, height=52)
        self.status_frame.pack(fill="x")
        self.status_frame.pack_propagate(False)

        self.turn_indicator = tk.Canvas(
            self.status_frame, width=18, height=18,
            bg=STATUS_BG, highlightthickness=0
        )
        self.turn_indicator.pack(side="left", padx=(20, 8), pady=10)

        self.status_label = tk.Label(
            self.status_frame,
            text="ATTACKER'S TURN",
            font=("Georgia", 16, "bold"),
            fg=ATK_RIM, bg=STATUS_BG
        )
        self.status_label.pack(side="left", pady=10)

        self.move_label = tk.Label(
            self.status_frame,
            text="",
            font=("Georgia", 10),
            fg="#888877", bg=STATUS_BG
        )
        self.move_label.pack(side="right", padx=20, pady=10)

        # ── end game button ───────────────────────────────────────────────────
        self.end_btn = tk.Label(
            self.status_frame,
            text="⏹  End Game",
            font=("Georgia", 10, "bold"),
            fg="#ffd700", bg="#3d1f0a",
            padx=12, pady=6,
            cursor="hand2"
        )
        self.end_btn.pack(side="right", padx=10, pady=10)
        self.end_btn.bind("<Button-1>", lambda e: self._end_game())
        self.end_btn.bind("<Enter>",    lambda e: self.end_btn.config(bg="#5a3010"))
        self.end_btn.bind("<Leave>",    lambda e: self.end_btn.config(bg="#3d1f0a"))

        # ── game state ────────────────────────────────────────────────────────
        self.board       = self._create_initial_board()
        self.selected    = None
        self.valid_moves = []
        self.turn        = "ATTACKER"
        self.move_count  = 0
        self.hovered     = None
        self.game_over   = False

        self.draw_board()
        self._update_status()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>",   self.on_hover)

        # if AI goes first (AI is attacker), trigger immediately
        if self.mode == "AI" and self.ai.side == "ATTACKER":
            self.after(500, self._ai_move)

    # ── initial board ─────────────────────────────────────────────────────────
    def _create_initial_board(self):
        board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        board[4][4] = KING
        for r, c in [(4,3),(4,5),(3,4),(5,4),(4,2),(4,6),
                     (2,4),(6,4),(3,3),(3,5),(5,3),(5,5)]:
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
        return col * CELL_SIZE + PADDING, row * CELL_SIZE + PADDING

    def _rc(self, x, y):
        return (y - PADDING) // CELL_SIZE, (x - PADDING) // CELL_SIZE

    # ── drawing ───────────────────────────────────────────────────────────────
    def draw_board(self):
        self.canvas.delete("all")
        self._draw_background()
        self._draw_cells()
        self._draw_grid()
        self._draw_labels()
        self._draw_pieces()

    def _draw_background(self):
        for i in range(6, 0, -1):
            shade = 40 + i * 8
            self.canvas.create_rectangle(
                PADDING - 6 - i, PADDING - 6 - i,
                PADDING + CELL_SIZE * BOARD_SIZE + 6 + i,
                PADDING + CELL_SIZE * BOARD_SIZE + 6 + i,
                outline=f"#{shade:02x}3a10", width=1
            )
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

                if (row, col) in corners:
                    color = CORNER_CLR
                elif (row, col) == throne:
                    color = THRONE_CLR
                else:
                    color = BOARD_LIGHT if (row + col) % 2 == 0 else BOARD_DARK

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

                if self.selected == (row, col):
                    self.canvas.create_rectangle(
                        x1+2, y1+2, x2-2, y2-2,
                        outline=HIGHLIGHT, width=3, fill=""
                    )

                if (row, col) in self.valid_moves:
                    cx, cy = x1 + CELL_SIZE//2, y1 + CELL_SIZE//2
                    r = 8
                    self.canvas.create_oval(
                        cx-r, cy-r, cx+r, cy+r,
                        fill=MOVE_DOT, outline=""
                    )

                if self.hovered == (row, col) and (row, col) not in self.valid_moves:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        outline="#888866", width=1, fill="#d4c090"
                    )

                if (row, col) in corners:
                    cx, cy = x1 + CELL_SIZE//2, y1 + CELL_SIZE//2
                    self.canvas.create_text(
                        cx, cy, text=CORNER_RUNE,
                        fill="#c8813a", font=("Georgia", 20, "bold")
                    )

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
        self.canvas.create_rectangle(
            PADDING, PADDING,
            PADDING + total, PADDING + total,
            outline="#5a3a10", width=3, fill=""
        )

    def _draw_labels(self):
        for i in range(BOARD_SIZE):
            self.canvas.create_text(
                PADDING - 18, PADDING + i * CELL_SIZE + CELL_SIZE//2,
                text=str(BOARD_SIZE - i),
                fill=LABEL_CLR, font=("Georgia", 11, "bold")
            )
            self.canvas.create_text(
                PADDING + i * CELL_SIZE + CELL_SIZE//2, PADDING + BOARD_SIZE * CELL_SIZE + 18,
                text=chr(ord('A') + i),
                fill=LABEL_CLR, font=("Georgia", 11, "bold")
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
        R  = 26

        if piece == ATTACKER:
            fill, rim = ATK_FILL, ATK_RIM
        elif piece == DEFENDER:
            fill, rim = DEF_FILL, DEF_RIM
        else:
            fill, rim = KING_FILL, KING_RIM

        is_sel = self.selected == (row, col)
        if is_sel:
            self.canvas.create_oval(
                cx-R-5, cy-R-5, cx+R+5, cy+R+5,
                fill="", outline=HIGHLIGHT, width=3
            )

        self.canvas.create_oval(
            cx-R+3, cy-R+4, cx+R+3, cy+R+4,
            fill="#222222", outline=""
        )
        self.canvas.create_oval(
            cx-R, cy-R, cx+R, cy+R,
            fill=rim, outline=""
        )
        self.canvas.create_oval(
            cx-R+3, cy-R+3, cx+R-3, cy+R-3,
            fill=fill, outline=""
        )
        self.canvas.create_oval(
            cx-R//3, cy-R//2, cx, cy-R//5,
            fill="#cccccc", outline=""
        )
        if piece == KING:
            self.canvas.create_text(
                cx, cy, text="♛",
                fill="#3d1f0a", font=("Georgia", 18, "bold")
            )

    # ── status bar ────────────────────────────────────────────────────────────
    def _update_status(self):
        if self.turn == "ATTACKER":
            txt, color, dot, dot_rim = "ATTACKER'S TURN", ATK_RIM, ATK_FILL, ATK_RIM
        else:
            txt, color, dot, dot_rim = "DEFENDER'S TURN", "#4a90d9", DEF_FILL, DEF_RIM

        # add AI label if it's AI's turn
        if self.mode == "AI" and self.turn == self.ai.side:
            txt += "  🤖"

        self.status_label.config(text=txt, fg=color)
        self.move_label.config(text=f"Move {self.move_count}")
        self.turn_indicator.delete("all")
        self.turn_indicator.create_oval(1, 1, 17, 17, fill=dot, outline=dot_rim, width=2)

    # ── end game ──────────────────────────────────────────────────────────────
    def _end_game(self):
        if messagebox.askyesno("End Game", "Are you sure you want to end the game?"):
            self.on_end_game()

    # ── AI move ───────────────────────────────────────────────────────────────
    def _ai_move(self):
        if self.game_over:
            return

        move = self.ai.get_move(self.board, self.turn)

        if move is None:
            return

        sr, sc, tr, tc = move
        self.board[tr][tc] = self.board[sr][sc]
        self.board[sr][sc] = EMPTY
        self.move_count += 1

        rules.apply_capture(self.board, tr, tc)
        self.draw_board()

        if self._check_game_over():
            return

        self.turn = "DEFENDER" if self.turn == "ATTACKER" else "ATTACKER"
        self._update_status()

    # ── game over check ───────────────────────────────────────────────────────
    def _check_game_over(self):
        if rules.is_king_win(self.board):
            self.game_over = True
            self.draw_board()
            messagebox.showinfo("⚔  Game Over", "The King has escaped!\nDefenders Win!")
            self.on_end_game()
            return True

        if rules.is_king_captured(self.board):
            self.game_over = True
            self.draw_board()
            messagebox.showinfo("⚔  Game Over", "The King has been captured!\nAttackers Win!")
            self.on_end_game()
            return True

        return False

    # ── valid moves ───────────────────────────────────────────────────────────
    def _get_valid_moves(self, row, col):
        return [
            (tr, tc)
            for tr in range(BOARD_SIZE)
            for tc in range(BOARD_SIZE)
            if rules.is_valid_move(self.board, row, col, tr, tc)
        ]

    # ── hover ─────────────────────────────────────────────────────────────────
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

    # ── click ─────────────────────────────────────────────────────────────────
    def on_click(self, event):
        # block clicks when game is over or it's AI's turn
        if self.game_over:
            return
        if self.mode == "AI" and self.turn == self.ai.side:
            return

        row, col = self._rc(event.x, event.y)
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return

        if self.selected is None:
            piece = self.board[row][col]
            if (self.turn == "ATTACKER" and piece == ATTACKER) or \
               (self.turn == "DEFENDER" and piece in (DEFENDER, KING)):
                self.selected    = (row, col)
                self.valid_moves = self._get_valid_moves(row, col)
            self.draw_board()
            return

        sr, sc = self.selected

        if rules.is_valid_move(self.board, sr, sc, row, col):
            # apply human move
            self.board[row][col] = self.board[sr][sc]
            self.board[sr][sc]   = EMPTY
            self.move_count     += 1

            rules.apply_capture(self.board, row, col)

            self.selected    = None
            self.valid_moves = []
            self.draw_board()

            if self._check_game_over():
                return

            # flip turn
            self.turn = "DEFENDER" if self.turn == "ATTACKER" else "ATTACKER"
            self._update_status()

            # trigger AI move after short delay
            if self.mode == "AI":
                self.after(400, self._ai_move)

        else:
            # re-select a different friendly piece
            piece = self.board[row][col]
            if (self.turn == "ATTACKER" and piece == ATTACKER) or \
               (self.turn == "DEFENDER" and piece in (DEFENDER, KING)):
                self.selected    = (row, col)
                self.valid_moves = self._get_valid_moves(row, col)
            else:
                self.selected    = None
                self.valid_moves = []

        self.draw_board()