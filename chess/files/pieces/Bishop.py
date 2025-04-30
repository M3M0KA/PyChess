from .chess_piece import ChessPiece

class Bishop(ChessPiece):
    symbol = 'B'

    def is_valid_move(self, start, end, board):
        x1, y1 = start
        x2, y2 = end
        if abs(x1 - x2) != abs(y1 - y2):
            return False
        dx = 1 if x2 > x1 else -1
        dy = 1 if y2 > y1 else -1
        x, y = x1 + dx, y1 + dy
        while (x, y) != (x2, y2):
            if board[y][x] is not None:
                return False
            x += dx
            y += dy
        return board[y2][x2] is None or board[y2][x2].color != self.color