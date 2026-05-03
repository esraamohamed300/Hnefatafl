import numpy as np
from game_state import GameState
from rules import Rules

class Evaluation:
    def __init__(self):
        self.rules = Rules()

    def evaluate(self, state: GameState) -> float:
        if state.check_king_escape():
            return -10000

        if state.check_king_captured():
            return 10000

        king_score = self._evaluate_king_position(state)
        piece_score = self._evaluate_piece_count(state)
        mobility_score = self._evaluate_mobility(state)
        threat_score = self._evaluate_king_threat(state)
        center_score = self._evaluate_center_control(state)
        escape_score = self._evaluate_escape_routes(state)

        total = (
            king_score * 3 +
            piece_score * 2 +
            mobility_score * 1 +
            threat_score * 4 +
            center_score * 1 +
            escape_score * 5
        )

        return total

    def _evaluate_king_position(self, state):
        row, col = state.king_pos
        corners = [(0,0), (0,10), (10,0), (10,10)]

        if (row, col) in corners:
            return -1000

        distances = [abs(row-r)+abs(col-c) for r,c in corners]
        min_dist = min(distances)

        return min_dist * 20

    def _evaluate_piece_count(self, state):
        black_count = len(state.black_pieces)
        white_count = len(state.white_pieces)
        return (black_count - white_count) * 50

    def _evaluate_mobility(self, state):
        black_moves = len(state.get_legal_moves("black"))
        white_moves = len(state.get_legal_moves("white"))
        return (black_moves - white_moves) * 5

    def _evaluate_king_threat(self, state):
        row, col = state.king_pos
        surrounded = 0
        directions = [(0,1),(0,-1),(1,0),(-1,0)]

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 11 and 0 <= nc < 11:
                if state.board[nr][nc] == 'B':
                    surrounded += 1
            else:
                surrounded += 1

        return surrounded * 150

    def _evaluate_center_control(self, state):
        center_zone = [(4,4),(4,5),(4,6),(5,4),(5,5),(5,6),(6,4),(6,5),(6,6)]
        score = 0

        for r, c in center_zone:
            if state.board[r][c] == 'B':
                score += 20
            elif state.board[r][c] == 'W':
                score -= 20

        return score

    def _evaluate_escape_routes(self, state):
        row, col = state.king_pos
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        open_paths = 0

        for dr, dc in directions:
            r, c = row, col
            blocked = False

            while 0 <= r < 11 and 0 <= c < 11:
                if state.board[r][c] != '.':
                    blocked = True
                    break
                r += dr
                c += dc

            if not blocked:
                open_paths += 1

        return -open_paths * 200
