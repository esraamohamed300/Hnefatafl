import copy
import Core.rules as rules

EMPTY = 0
ATTACKER = 1
DEFENDER = 2
KING = 3
BOARD_SIZE = 9


class GameState:
    def __init__(self, board, turn):
        """
        board : 9x9 2-D list
        turn  : "ATTACKER" or "DEFENDER"
        """
        self.board = board
        self.turn  = turn

    # ── copy ──────────────────────────────────────────────────────────────────
    def clone(self):
        """Return a deep copy — the AI needs this to explore without
        modifying the real board."""
        return GameState(copy.deepcopy(self.board), self.turn)

    # ── legal moves ───────────────────────────────────────────────────────────
    def get_legal_moves(self):
        """
        Return a list of (sr, sc, tr, tc) tuples for every legal move
        the current player can make.
        """
        moves = []
        for sr in range(BOARD_SIZE):
            for sc in range(BOARD_SIZE):
                piece = self.board[sr][sc]

                # only pick pieces belonging to the current player
                if self.turn == "ATTACKER" and piece != ATTACKER:
                    continue
                if self.turn == "DEFENDER" and piece not in (DEFENDER, KING):
                    continue

                for tr in range(BOARD_SIZE):
                    for tc in range(BOARD_SIZE):
                        if rules.is_valid_move(self.board, sr, sc, tr, tc):
                            moves.append((sr, sc, tr, tc))
        return moves

    # ── apply a move ──────────────────────────────────────────────────────────
    def apply_move(self, move):
        """
        Apply (sr, sc, tr, tc) and return a NEW GameState.
        The current state is never modified — safe for the AI tree search.
        """
        sr, sc, tr, tc = move
        new_state = self.clone()

        new_state.board[tr][tc] = new_state.board[sr][sc]
        new_state.board[sr][sc] = EMPTY

        rules.apply_capture(new_state.board, tr, tc)

        # flip turn
        new_state.turn = "DEFENDER" if self.turn == "ATTACKER" else "ATTACKER"
        return new_state

    # ── terminal checks ───────────────────────────────────────────────────────
    def is_terminal(self):
        """Return True if the game is over."""
        return rules.is_king_win(self.board) or rules.is_king_captured(self.board)

    def get_winner(self):
        """
        Call only when is_terminal() is True.
        Returns "DEFENDER" or "ATTACKER".
        """
        if rules.is_king_win(self.board):
            return "DEFENDER"
        if rules.is_king_captured(self.board):
            return "ATTACKER"
        return None

    # ── utility ───────────────────────────────────────────────────────────────
    def get_piece_counts(self):
        attackers = defenders = 0
        for row in self.board:
            for cell in row:
                if cell == ATTACKER:
                    attackers += 1
                elif cell in (DEFENDER, KING):
                    defenders += 1
        return attackers, defenders

    def find_king(self):
        """Return (row, col) of the king, or None if captured."""
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == KING:
                    return (r, c)
        return None

    def __repr__(self):
        symbols = {EMPTY: ".", ATTACKER: "A", DEFENDER: "D", KING: "K"}
        rows = []
        for row in self.board:
            rows.append(" ".join(symbols[c] for c in row))
        return "\n".join(rows) + f"\nTurn: {self.turn}"