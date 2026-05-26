from .ChessPiece import ChessPiece
from .Rook import Rook
from .Bishop import Bishop

class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'queen'
        self.short_name = 'q'

    def is_valid_move(self, start, end, board):
        return Rook(self.color).is_valid_move(start, end, board) or Bishop(self.color).is_valid_move(start, end, board)