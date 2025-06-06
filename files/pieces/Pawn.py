from .ChessPiece import ChessPiece

class Pawn(ChessPiece):
    symbol = 'pawn'
    
    def is_valid_move(self, start, end, board):
        x1, y1 = start
        x2, y2 = end
        direction = -1 if self.color == 'W' else 1
        start_row = 6 if self.color == 'W' else 1


        if x1 == x2 and y2 == y1 + direction and board[y2][x2] is None:
            return True

        if x1 == x2 and y1 == start_row and y2 == y1 + 2 * direction and board[y1 + direction][x1] is None and board[y2][x2] is None:
            return True

        if abs(x2 - x1) == 1 and y2 == y1 + direction and board[y2][x2] is not None and board[y2][x2].color != self.color:
            return True
        return False
    
    def turn_to_differentpiece(self, end_y):
        if self.color == 'B' and end_y == 7:
            return True
        if self.color == 'W' and end_y == 0:
            return True
        return False