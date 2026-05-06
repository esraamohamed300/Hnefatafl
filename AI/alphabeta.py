from Core.game_state import GameState
from AI.evaluation import evaluate

INF = float('inf')


def alphabeta(state: GameState, depth: int, alpha: float, beta: float,
              maximizing: bool, ai_player: str) -> float:
    """
    Alpha-Beta Pruning algorithm.
    
    state       : current GameState
    depth       : how many moves ahead to search
    alpha       : best score maximizer can guarantee so far
    beta        : best score minimizer can guarantee so far
    maximizing  : True if current player is trying to maximize score
    ai_player   : the AI's side ("ATTACKER" or "DEFENDER")
    
    Returns the best score found.
    """


    if depth == 0 or state.is_terminal():
        return evaluate(state, ai_player)

    legal_moves = state.get_legal_moves()


    if not legal_moves:
        return evaluate(state, ai_player)


    if maximizing:
        max_score = -INF

        for move in legal_moves:
            new_state = state.apply_move(move)
            score = alphabeta(new_state, depth - 1, alpha, beta, False, ai_player)

            max_score = max(max_score, score)
            alpha = max(alpha, score)


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

            
            if beta <= alpha:
                break

        return min_score


def get_best_move(state: GameState, depth:
                int, ai_player: str):
    """
    Calls alphabeta for every legal move and returns the best one.
    
    depth is set by difficulty:
    Easy   → depth 1
    Medium → depth 3
    Hard   → depth 5
    """
    best_move  = None
    best_score = -INF
    alpha      = -INF
    beta       =  INF

    legal_moves = state.get_legal_moves()

    for move in legal_moves:
        new_state = state.apply_move(move)


        score = alphabeta(new_state, depth - 1, alpha, beta, False, ai_player)

        if score > best_score:
            best_score = score
            best_move  = move

        alpha = max(alpha, score)

    return best_move
