from .chess_piece import ChessPiece

class King(ChessPiece):
    symbol = 'K'

    def is_valid_move(self, start, end, board):
        x1, y1 = start
        x2, y2 = end
        return max(abs(x1 - x2), abs(y1 - y2)) == 1 and (board[y2][x2] is None or board[y2][x2].color != self.color)