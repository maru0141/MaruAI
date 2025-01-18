import random

BLACK = 1
WHITE = 2

board = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 2, 0, 0],
        [0, 0, 2, 1, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
]

def can_place_x_y(board, stone, x, y):
    if board[y][x] != 0:
        return False

    opponent = 3 - stone  # 相手の石
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True

    return False

def can_place(board, stone):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                return True
    return False

def get_corner_moves():
    return [(0, 0), (0, 5), (5, 0), (5, 5)]

def get_edge_moves():
    edge_moves = []
    for i in range(6):
        edge_moves.append((0, i))  # 上辺
        edge_moves.append((5, i))  # 下辺
        edge_moves.append((i, 0))  # 左辺
        edge_moves.append((i, 5))  # 右辺
    return edge_moves

def score_move(board, stone, x, y):
    """
    石を置いたときの反転する石の数を計算する関数。
    """
    opponent = 3 - stone
    flipped_count = 0
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        temp_flipped_count = 0

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            temp_flipped_count += 1

        if 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            flipped_count += temp_flipped_count

    return flipped_count

def find_best_move(board, stone):
    """
    最良の手を見つける関数。角優先、辺、反転数、安定した石を考慮する。
    石を置ける場所が見つからない場合はNoneを返さず、他の選択肢を提供します。
    """
    corners = get_corner_moves()
    edge_moves = get_edge_moves()
    
    # 角に置ける場所を最優先
    for x, y in corners:
        if can_place_x_y(board, stone, x, y):
            return x, y
    
    # 次に辺に置ける場所
    for x, y in edge_moves:
        if can_place_x_y(board, stone, x, y):
            return x, y
    
    # 反転数を最大化する場所を選ぶ
    best_score = -1
    best_move = None
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                score = score_move(board, stone, x, y)
                if score > best_score:
                    best_score = score
                    best_move = (x, y)
    
    # もし適切な場所が見つからない場合、ランダムな場所を選ぶ
    if best_move is None:
        return random_place(board, stone)

    return best_move


class MaruAI(object):
    def face(self):
        return "🍊"

    def place(self, board, stone):
        x, y = find_best_move(board, stone)
        return x, y
