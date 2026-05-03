from evaluation import Evaluation

evaluation = Evaluation()

transposition_table = {}

def alphabeta(state, depth, alpha, beta, maximizing_player, player):
    state_key = (
        tuple(map(tuple, state.board)),
        depth,
        player
    )

    if state_key in transposition_table:
        return transposition_table[state_key]

    if depth == 0 or state.is_game_over():
        score = evaluation.evaluate(state)
        transposition_table[state_key] = score
        return score

    moves = order_moves(state.get_legal_moves(player))

    if maximizing_player:
        max_eval = -float('inf')

        for move in moves:
            new_state = state.apply_move(move)

            eval_score = alphabeta(
                new_state,
                depth - 1,
                alpha,
                beta,
                False,
                "white"
            )

            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)

            if beta <= alpha:
                break

        transposition_table[state_key] = max_eval
        return max_eval

    else:
        min_eval = float('inf')

        for move in moves:
            new_state = state.apply_move(move)

            eval_score = alphabeta(
                new_state,
                depth - 1,
                alpha,
                beta,
                True,
                "black"
            )

            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)

            if beta <= alpha:
                break

        transposition_table[state_key] = min_eval
        return min_eval


def order_moves(moves):
    def move_score(move):
        score = 0

        if hasattr(move, 'get_captured_pieces'):
            score += len(move.get_captured_pieces()) * 100

        if hasattr(move, 'to_pos'):
            r, c = move.to_pos
            score -= abs(r - 5) + abs(c - 5)

        return score

    return sorted(moves, key=move_score, reverse=True)
