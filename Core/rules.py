"""Core Hnefatafl rules engine.

This module implements the key Hnefatafl rules used by the GUI:
- Movement like a rook: any number of empty squares in a straight line.
- No passing through other pieces, no sharing a square.
- Custodial capture by sandwiching opponents horizontally or vertically.
- Special capture squares: throne and corner spaces act as capturing partners.
- The king cannot assist in captures.
- King escape and king capture conditions.
"""

BOARD_SIZE = 9
EMPTY = 0
ATTACKER = 1
DEFENDER = 2
KING = 3

SPECIAL_SQUARES = {(0, 0), (0, 8), (8, 0), (8, 8), (4, 4)}


def is_path_clear(board, sr, sc, tr, tc):
    # حركة أفقي
    if sr == tr:
        step = 1 if tc > sc else -1
        for c in range(sc + step, tc, step):
            if board[sr][c] != EMPTY:
                return False

    # حركة رأسي
    elif sc == tc:
        step = 1 if tr > sr else -1
        for r in range(sr + step, tr, step):
            if board[r][sc] != EMPTY:
                return False

    return True


def is_capture_partner(board, moving_piece, r, c):
    if moving_piece == KING:
        return False

    if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
        target = board[r][c]
        if target == moving_piece and target != KING:
            return True
        if (r, c) in SPECIAL_SQUARES:
            return True

    return False


def would_be_captured(board, tr, tc, moving_piece):
    # King is never blocked by sandwich logic — handled separately
    if moving_piece == KING:
        return False

    enemy = ATTACKER if moving_piece in (DEFENDER, KING) else DEFENDER

    # Horizontal
    if 0 <= tc - 1 and tc + 1 < BOARD_SIZE:
        left = board[tr][tc - 1]
        right = board[tr][tc + 1]
        left_special = (tr, tc - 1) in SPECIAL_SQUARES
        right_special = (tr, tc + 1) in SPECIAL_SQUARES
        if (left == enemy or left_special) and (right == enemy or right_special):
            return True

    # Vertical
    if 0 <= tr - 1 and tr + 1 < BOARD_SIZE:
        above = board[tr - 1][tc]
        below = board[tr + 1][tc]
        above_special = (tr - 1, tc) in SPECIAL_SQUARES
        below_special = (tr + 1, tc) in SPECIAL_SQUARES
        if (above == enemy or above_special) and (below == enemy or below_special):
            return True

    return False

def is_valid_move(board, sr, sc, tr, tc):
    # نفس الصف أو نفس العمود فقط
    if sr != tr and sc != tc:
        return False
    # لا يتم التحرك إلى نفس الموقع
    if sr == tr and sc == tc:
        return False

    # الهدف لازم يكون فاضي
    if board[tr][tc] != EMPTY:
        return False

    piece = board[sr][sc]
    # Only the King may enter corners or the throne
    if (tr, tc) in SPECIAL_SQUARES and piece != KING:
        return False
    
    # الطريق لازم يكون فاضي
    if not is_path_clear(board, sr, sc, tr, tc):
        return False

    # لا يمكن أن تتوقف القطعة داخل ساندويتش
    if would_be_captured(board, tr, tc, board[sr][sc]):
        return False

    return True

def apply_capture(board, r, c):
    moved_piece = board[r][c]
    if moved_piece == EMPTY:
        return
    if moved_piece == KING:
        return

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dr, dc in directions:
        r1, c1 = r + dr, c + dc
        r2, c2 = r + 2 * dr, c + 2 * dc

        if 0 <= r1 < BOARD_SIZE and 0 <= c1 < BOARD_SIZE:
            target = board[r1][c1]
            #  NEVER capture the king through regular sandwich logic
            if target == EMPTY or target == moved_piece or target == KING:
                continue
            if is_capture_partner(board, moved_piece, r2, c2):
                board[r1][c1] = EMPTY

def is_king_win(board):
    corners = [(0, 0), (0, 8), (8, 0), (8, 8)]
    return any(board[r][c] == KING for r, c in corners)


def is_king_captured(board):
    # Find the king
    king_pos = None
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == KING:
                king_pos = (r, c)
                break
        if king_pos:
            break

    if king_pos is None:
        return True

    r, c = king_pos

    def is_hostile(nr, nc):
        # Out of bounds = wall = hostile
        if not (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE):
            return True
        # Only attackers count, NOT special squares
        return board[nr][nc] == ATTACKER or (nr, nc) in [(0,0),(0,8),(8,0),(8,8)]

    above = is_hostile(r-1, c) 
    below = is_hostile(r+1, c)
    left  = is_hostile(r, c-1)
    right = is_hostile(r, c+1)

    # Corner: 2 sides are walls, needs the other 2 to be attackers
    """
if (r, c) in [(0,1),(1,0), (7,0), (8,1), (0,7), (1,8), (7,8), (8,7)]:
        return above and below and left and right


"""
    
    if (r, c) in [(0,0), (0,8), (8,0), (8,8)]:
        return above and below and left and right  
    

    # Edge: 1 side is a wall, needs the other 3 to be attackers
    if r == 0 or r == BOARD_SIZE-1 or c == 0 or c == BOARD_SIZE-1:
        return above and below and left and right

    # Open board: needs all 4 sides to be attackers
    return above and below and left and right