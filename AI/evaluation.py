from utils.helpers import EMPTY, ATTACKER, DEFENDER, KING, BOARD_SIZE, CORNERS, SPECIAL_SQUARES
from Core.game_state import GameState


# ── weights ───────────────────────────────────────────────────────────────────
WIN_SCORE          =  100000
LOSE_SCORE         = -100000

ATTACKER_PIECE     =  10     # score per attacker alive
DEFENDER_PIECE     =  12     # defenders worth slightly more (fewer pieces)
KING_MOBILITY      =  8      # score per legal move the king has
KING_CORNER_DIST   =  25     # score per step CLOSER to nearest corner
KING_SAFE          =  30     # bonus if king has a clear path to a corner
ATTACKER_SURROUND  =  15     # score per attacker adjacent to king
DEFENDER_GUARD     =  10     # score per defender adjacent to king


def evaluate(state: GameState, ai_player: str) -> int:
    """
    Returns a score from the perspective of ai_player.
    Positive = good for ai_player, Negative = bad.
    """
    # ── terminal states ───────────────────────────────────────────────────────
    if state.is_terminal():
        winner = state.get_winner()
        if winner == ai_player:
            return WIN_SCORE
        else:
            return LOSE_SCORE

    score = 0
    king_pos = state.find_king()

    if king_pos is None:
        return LOSE_SCORE if ai_player == "DEFENDER" else WIN_SCORE

    kr, kc = king_pos
    attackers, defenders = state.get_piece_counts()

    # ── 1. piece advantage ────────────────────────────────────────────────────
    # more attackers = good for attacker, more defenders = good for defender
    piece_score = (attackers * ATTACKER_PIECE) - (defenders * DEFENDER_PIECE)
    # piece_score > 0 → attacker advantage
    # piece_score < 0 → defender advantage

    # ── 2. king distance to nearest corner ───────────────────────────────────
    # closer king to corner = good for defender
    min_dist = min(abs(kr - cr) + abs(kc - cc) for cr, cc in CORNERS)
    corner_score = -min_dist * KING_CORNER_DIST
    # more negative distance = closer to corner = better for defender

    # ── 3. king mobility ──────────────────────────────────────────────────────
    king_moves = _count_king_moves(state.board, kr, kc)
    mobility_score = king_moves * KING_MOBILITY

    # ── 4. attackers surrounding the king ────────────────────────────────────
    surround_score = _count_adjacent(state.board, kr, kc, ATTACKER) * ATTACKER_SURROUND

    # ── 5. defenders guarding the king ───────────────────────────────────────
    guard_score = _count_adjacent(state.board, kr, kc, DEFENDER) * DEFENDER_GUARD

    # ── 6. king has open path to corner ──────────────────────────────────────
    safe_bonus = KING_SAFE if _king_has_open_path(state.board, kr, kc) else 0

    # ── combine from DEFENDER perspective ────────────────────────────────────
    # defender wants: king close to corner, king mobile, king guarded, few attackers
    defender_score = (
        - piece_score       # fewer attackers = better
        + corner_score      # king close to corner = better  (corner_score is negative of dist)
        + mobility_score    # king can move = better
        - surround_score    # fewer attackers around king = better
        + guard_score       # more defenders around king = better
        + safe_bonus        # open path to corner = better
    )

    # ── flip if ai is attacker ────────────────────────────────────────────────
    if ai_player == "ATTACKER":
        return -defender_score
    return defender_score


# ── helpers ───────────────────────────────────────────────────────────────────

def _count_king_moves(board, kr, kc):
    """Count how many squares the king can move to."""
    count = 0
    for tr in range(BOARD_SIZE):
        for tc in range(BOARD_SIZE):
            if (tr != kr or tc != kc) and board[tr][tc] == EMPTY:
                # simple rook reachability check
                if tr == kr or tc == kc:
                    if _path_clear(board, kr, kc, tr, tc):
                        count += 1
    return count


def _count_adjacent(board, r, c, piece_type):
    """Count how many pieces of piece_type are adjacent to (r, c)."""
    count = 0
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
            if board[nr][nc] == piece_type:
                count += 1
    return count


def _path_clear(board, sr, sc, tr, tc):
    """Check if path is clear between two squares (rook movement)."""
    if sr == tr:
        step = 1 if tc > sc else -1
        for c in range(sc+step, tc, step):
            if board[sr][c] != EMPTY:
                return False
    elif sc == tc:
        step = 1 if tr > sr else -1
        for r in range(sr+step, tr, step):
            if board[r][sc] != EMPTY:
                return False
    return True


def _king_has_open_path(board, kr, kc):
    """Return True if the king has at least one clear straight line to a corner."""
    for cr, cc in CORNERS:
        if kr == cr or kc == cc:
            if _path_clear(board, kr, kc, cr, cc):
                return True
    return False