from Core.game_state import GameState
from AI.alphabeta import get_best_move

DIFFICULTY_DEPTH = {
    "Easy"   : 1,
    "Medium" : 3,
    "Hard"   : 4
}


class AIPlayer:
    def __init__(self, side: str, difficulty: str):
        self.side       = side
        self.difficulty = difficulty
        self.depth      = DIFFICULTY_DEPTH[difficulty]

    def get_move(self, board, turn):
        state = GameState(board, turn)
        move  = get_best_move(state, self.depth, self.side)
        return move