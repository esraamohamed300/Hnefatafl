from rules import Rules

EMPTY = 0
ATTACKER = 1
DEFENDER = 2
KING = 3
BOARD_SIZE = 9

class Evaluation:
    def __init__(self):
        self.rules = Rules()

    def evaluate(self, state):
        if self.rules.is_king_win(state.board):
            return -10000

        if self.rules.is_king_captured(state.board):
            return 10000

        king_score = self._king_position(state)
        piece_score = self._piece_count(state)
        mobility_score = self._mobility(state)
        threat_score = self._king_threat(state)

        return king_score + piece_score + mobility_score + threat_score

    def _king_position(self, state):
        pos = state.find_king()
        if pos is None:
            return 1000

        r, c = pos
        corners = [(0,0),(0,8),(8,0),(8,8)]

        if (r,c) in corners:
            return -1000

        dist = min(abs(r-x)+abs(c-y) for x,y in corners)
        return dist * 20

    def _piece_count(self, state):
        attackers, defenders = state.get_piece_counts()
        return (attackers - defenders) * 50

    def _mobility(self, state):
        original = state.turn

        state.turn = "ATTACKER"
        a = len(state.get_legal_moves())

        state.turn = "DEFENDER"
        d = len(state.get_legal_moves())

        state.turn = original

        return (a - d) * 5

    def _king_threat(self, state):
        pos = state.find_king()
        if pos is None:
            return 1000

        r, c = pos
        s = 0

        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                if state.board[nr][nc] == ATTACKER:
                    s += 1
            else:
                s += 1

        return s * 150
