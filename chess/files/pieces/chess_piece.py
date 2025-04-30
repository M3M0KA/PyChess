class ChessPiece:
    def __init__(self, color):
        self.color = color  # 'W' oder 'B'

    def is_valid_move(self, start, end, board):
        raise NotImplementedError

    def __str__(self):
        return self.symbol + self.color

