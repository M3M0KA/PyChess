class ChessPiece:
    def __init__(self, color, image):
        self.color = color  # 'W' oder 'B'
        self.image = image

    def is_valid_move(self, start, end, board):
        raise NotImplementedError("is_valid_move() muss in der Unterklasse implementiert werden.")

    def __str__(self):
        return self.symbol + self.color

