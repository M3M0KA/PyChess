from .ChessPiece import ChessPiece
from .Rook import Rook
from .Bishop import Bishop

class Queen(ChessPiece):
    symbol = 'queen'

    def is_valid_move(self, start, end, board):
        return Rook(self.color).is_valid_move(start, end, board) or Bishop(self.color).is_valid_move(start, end, board)