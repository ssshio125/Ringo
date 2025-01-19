import math
import copy
from collections import defaultdict

BLACK = 1
WHITE = 2

evaluation_weights = [
    [120, -40, 20, 20, -40, 120],
    [-40, -60, 1, 1, -60, -40],
    [20, 1, 5, 5, 1, 20],
    [20, 1, 5, 5, 1, 20],
    [-40, -60, 1, 1, -60, -40],
    [120, -40, 20, 20, -40, 120],
]

class RingoAI:
    def face(self):
        return "🍎"

    def place(self, board, stone):
        # 有効な手を取得
        valid_moves = self.get_valid_moves(board, stone)
        if not valid_moves:
            return None  # スキップ

        best_move = None
        best_score = -math.inf

        # ムーブオーダリングを使用して候補手を評価
        valid_moves.sort(key=lambda move: self.evaluate_move(board, stone, move), reverse=True)
        for x, y in valid_moves:
            temp_board = self.apply_move(board, stone, x, y)
            score = -self.negamax(temp_board, 3 - stone, depth=6, alpha=-math.inf, beta=math.inf)
            if score > best_score:
                best_score = score
                best_move = (x, y)

        return best_move

    def get_valid_moves(self, board, stone):
        valid_moves = []
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    valid_moves.append((x, y))
        return valid_moves

    def apply_move(self, board, stone, x, y):
        """
        石を置いて新しい盤面を返す。
        """
        new_board = [row[:] for row in board]
        new_board[y][x] = stone

        opponent = 3 - stone
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            stones_to_flip = []

            while 0 <= nx < len(new_board[0]) and 0 <= ny < len(new_board) and new_board[ny][nx] == opponent:
                stones_to_flip.append((nx, ny))
                nx += dx
                ny += dy

            if stones_to_flip and 0 <= nx < len(new_board[0]) and 0 <= ny < len(new_board) and new_board[ny][nx] == stone:
                for flip_x, flip_y in stones_to_flip:
                    new_board[flip_y][flip_x] = stone

        return new_board

    def can_place_x_y(self, board, stone, x, y):
        """
        指定した座標に石を置けるか確認する。
        """
        if board[y][x] != 0:
            return False

        opponent = 3 - stone
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            found_opponent = False

            while 0 <= nx < len(board[0]) and 0 <= ny < len(board):
                if board[ny][nx] == opponent:
                    found_opponent = True
                elif board[ny][nx] == stone and found_opponent:
                    return True
                else:
                    break
                nx += dx
                ny += dy

        return False

    def negamax(self, board, stone, depth, alpha, beta):
        valid_moves = self.get_valid_moves(board, stone)

        if depth == 0 or not valid_moves:
            return self.evaluate_board(board, stone)

        max_eval = -math.inf
        for x, y in valid_moves:
            new_board = self.apply_move(board, stone, x, y)
            eval = -self.negamax(new_board, 3 - stone, depth - 1, -beta, -alpha)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        return max_eval

    def evaluate_board(self, board, stone):
        score = 0
        opponent = 3 - stone
        stone_count = 0
        opponent_count = 0
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == stone:
                    score += evaluation_weights[y][x]
                    stone_count += 1
                elif board[y][x] == opponent:
                    score -= evaluation_weights[y][x]
                    opponent_count += 1

        # 駒を取りすぎないよう調整 (駒の数を減点要素に追加)
        score -= (stone_count - opponent_count) * 5
        return score

    def evaluate_move(self, board, stone, move):
        x, y = move
        temp_board = self.apply_move(board, stone, x, y)
        return self.evaluate_board(temp_board, stone)

