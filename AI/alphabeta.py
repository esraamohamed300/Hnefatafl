from Core.game_state import GameState
from AI.evaluation import evaluate

INF = float('inf')


def alphabeta(state: GameState, depth: int, alpha: float, beta: float,
              maximizing: bool, ai_player: str) -> float:


    if depth == 0 or state.is_terminal():
        return evaluate(state, ai_player)

    legal_moves = state.get_legal_moves()

<<<<<<< HEAD

=======
>>>>>>> a48031c (Last Version)
    if not legal_moves:
        return evaluate(state, ai_player)


    if maximizing:
        max_score = -INF

        for move in legal_moves:
            new_state = state.apply_move(move)
            score = alphabeta(new_state, depth - 1, alpha, beta, False, ai_player)

            max_score = max(max_score, score)
            alpha = max(alpha, score)

<<<<<<< HEAD

=======
>>>>>>> a48031c (Last Version)
            if beta <= alpha:
                break

        return max_score


    else:
        min_score = INF

        for move in legal_moves:
            new_state = state.apply_move(move)
            score = alphabeta(new_state, depth - 1, alpha, beta, True, ai_player)

            min_score = min(min_score, score)
            beta = min(beta, score)
<<<<<<< HEAD

            
=======
>>>>>>> a48031c (Last Version)
            if beta <= alpha:
                break

        return min_score


<<<<<<< HEAD
def get_best_move(state: GameState, depth:
                int, ai_player: str):
    """
    Calls alphabeta for every legal move and returns the best one.
    
    depth is set by difficulty:
    Easy   → depth 1
    Medium → depth 3
    Hard   → depth 5
    """
=======
def get_best_move(state: GameState, depth: int, ai_player: str):
  
>>>>>>> a48031c (Last Version)
    best_move  = None
    best_score = -INF
    alpha      = -INF
    beta       =  INF

    legal_moves = state.get_legal_moves()

    for move in legal_moves:
        new_state = state.apply_move(move)

<<<<<<< HEAD

=======
>>>>>>> a48031c (Last Version)
        score = alphabeta(new_state, depth - 1, alpha, beta, False, ai_player)

        if score > best_score:
            best_score = score
            best_move  = move

        alpha = max(alpha, score)

    return best_move
