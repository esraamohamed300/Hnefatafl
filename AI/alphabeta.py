from evaluation import Evaluation

evaluation = Evaluation()
transposition_table = {}

def alphabeta(state, depth, alpha, beta, maximizing):
    key = (tuple(map(tuple, state.board)), depth, state.turn)

    if key in transposition_table:
        return transposition_table[key]

    if depth == 0 or state.is_terminal():
        score = evaluation.evaluate(state)
        transposition_table[key] = score
        return score

    moves = state.get_legal_moves()

    if maximizing:
        value = -float('inf')
        for move in moves:
            new_state = state.apply_move(move)
            value = max(value, alphabeta(new_state, depth-1, alpha, beta, False))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        transposition_table[key] = value
        return value
    else:
        value = float('inf')
        for move in moves:
            new_state = state.apply_move(move)
            value = min(value, alphabeta(new_state, depth-1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        transposition_table[key] = value
        return value
