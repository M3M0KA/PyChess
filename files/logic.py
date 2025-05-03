from .pieces import Pawn, Rook, Knight, Bishop, Queen, King
import copy


# Spielbrett initialisieren
def create_board():
    board = [[None for _ in range(8)] for _ in range(8)]

    # Figuren platzieren
    for i in range(8):
        board[1][i] = Pawn('B')
        board[6][i] = Pawn('W')
    
    placement = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    for i, piece_class in enumerate(placement):
        board[0][i] = piece_class('B')
        board[7][i] = piece_class('W')
    
    return board


def parse_input(move):
    try:
        start, end = move.split()
        x1, y1 = ord(start[0]) - ord('a'), 8 - int(start[1])
        x2, y2 = ord(end[0]) - ord('a'), 8 - int(end[1])
        return (x1, y1), (x2, y2)
    except:
        return None, None

def move_piece(board, start, end, current_color, gui = None):
    x1, y1 = start
    x2, y2 = end
    piece = board[y1][x1]
    if piece and piece.color == current_color and piece.is_valid_move((x1, y1), (x2, y2), board):
        target = board[y2][x2]
        if target is None or target.color != current_color:
            temp_board = copy.deepcopy(board)
            temp_board[y1][x1] = None
            temp_board[y2][x2] = piece
            if is_check(temp_board, "W", find_king(temp_board, 'W')) and current_color == 'W':
                print("Weisser König im Schach!")
                return False
            if is_check(temp_board, "B", find_king(temp_board, 'B')) and current_color == 'B':
                print("Schwarzer König im Schach!")
                return False
            if isinstance(piece, Pawn):
                if piece.turn_to_differentpiece(y2):
                    gui.promotion_options(gui.screen)
                    new_piece = gui.wait_for_promotion()
                    if new_piece.lower() == 'dame':
                        board[y2][x2] = Queen(piece.color)
                        board[y1][x1] = None
                        return True
                    if new_piece.lower() == 'turm':
                        board[y2][x2] = Rook(piece.color)
                        board[y1][x1] = None
                        return True
                    if new_piece.lower() == 'läufer':
                        board[y2][x2] = Bishop(piece.color)
                        board[y1][x1] = None
                        return True
                    if new_piece.lower() == 'springer':
                        board[y2][x2] = Knight(piece.color)
                        board[y1][x1] = None
                        return True           
            board[y2][x2] = piece
            board[y1][x1] = None
            return True
    return False

def find_king(board, wanted_king_color):
    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if isinstance(piece, King) and piece.color == wanted_king_color:
                return (x, y)
    return None

def is_check(board, king_color, king_pos):
    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece and piece.color != king_color:
                if piece.is_valid_move((x, y), king_pos, board):
                    return True


def game_loop(gui):
    board = create_board()
    current_color = 'W'
    while True:
        gui.update(board)
        print(f"{'Weiss' if current_color == 'W' else 'Schwarz'} ist am Zug.")
        move = input("Bewege (z.B. e2 e4) oder 'quit': ")
        if move.lower() == 'quit':
            break
        start, end = parse_input(move)
        if start and end:
            if move_piece(board, start, end, current_color):
                current_color = 'B' if current_color == 'W' else 'W'
            else:
                print("Ungültiger Zug!")
        else:
            print("Eingabefehler!")
