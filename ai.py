def can_place_x_y(board, stone, x, y):

    if board[y][x] != 0:
        return False  # 既に石がある場合は置けない

    opponent = 3 - stone  # 相手の石 (1なら2、2なら1)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True  # 石を置ける条件を満たす

    return False
    
class MaruAI(object):
    def __init__(self):
        # 基本的なスコアマップ
        self.score_map = [
            [200, -20, 10, 10, -20, 200],
            [-20, -50, -2, -2, -50, -20],
            [10, -2,  0,  0,  -2,  10],
            [10, -2,  0,  0,  -2,  10],
            [-20, -50, -2, -2, -50, -20],
            [200, -20, 10, 10, -20, 200],
        ]

    def face(self):
        return "🍊"

    def evaluate_board(self, board, stone):
        """
        現在の盤面全体を評価してスコアを返す。
        """
        score = 0
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == stone:
                    score += self.score_map[y][x]
                elif board[y][x] == -stone:
                    score -= self.score_map[y][x]
        return score

    def get_possible_moves(self, board, stone):
        """
        現在の石で置けるすべての座標を取得する。
        """
        moves = []
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    moves.append((x, y))
        return moves

    def can_place_x_y(self, board, stone, x, y):
        """
        指定した座標に石を置けるかどうかを判定する。
        """
        if board[y][x] != 0:  # 空のマスか確認
            return False

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dy, dx in directions:
            nx, ny = x + dx, y + dy
            found_opponent = False
            while 0 <= ny < len(board) and 0 <= nx < len(board[0]):
                if board[ny][nx] == -stone:  # 相手の石がある
                    found_opponent = True
                elif board[ny][nx] == stone:  # 自分の石に戻る
                    if found_opponent:
                        return True
                    break
                else:
                    break
                nx += dx
                ny += dy
        return False

    def simulate_move(self, board, stone, x, y):
        """
        指定した座標に石を置いた後の盤面をシミュレーション。
        """
        new_board = [row[:] for row in board]  # 盤面のコピー
        new_board[y][x] = stone

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dy, dx in directions:
            nx, ny = x + dx, y + dy
            stones_to_flip = []
            while 0 <= ny < len(board) and 0 <= nx < len(board[0]):
                if new_board[ny][nx] == -stone:
                    stones_to_flip.append((nx, ny))
                elif new_board[ny][nx] == stone:
                    for flip_x, flip_y in stones_to_flip:
                        new_board[flip_y][flip_x] = stone
                    break
                else:
                    break
                nx += dx
                ny += dy
        return new_board

    def place(self, board, stone):
        """
        最善の場所を計算して石を置く。
        """
        possible_moves = self.get_possible_moves(board, stone)
        if not possible_moves:
            return None  # 置ける場所がない場合はパス

        # シミュレーションによる評価を行い最善手を探す
        best_move = None
        best_score = float('-inf')
        for x, y in possible_moves:
            simulated_board = self.simulate_move(board, stone, x, y)
            score = self.evaluate_board(simulated_board, stone)
            if score > best_score:
                best_score = score
                best_move = (x, y)

        return best_move

move = whiteai.place(copy(board), WHITE)
if move is None:
    # パス処理
    print("白はパスします")
else:
    x, y = move
    # 石を置く処理
    print(f"白は({x}, {y})に置きます")
