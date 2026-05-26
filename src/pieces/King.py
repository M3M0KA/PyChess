from .ChessPiece import ChessPiece

class King(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'king'
        self.short_name = 'k'

    def is_valid_move(self, start, end, board):
        x1, y1 = start
        x2, y2 = end
        return max(abs(x1 - x2), abs(y1 - y2)) == 1 and (board[y2][x2] is None or board[y2][x2].color != self.color)