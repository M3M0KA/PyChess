from .pieces import Pawn, Rook, Knight, Bishop, Queen, King

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

def print_board(board):
    print(board)

def parse_input(move):
    try:
        start, end = move.split()
        x1, y1 = ord(start[0]) - ord('a'), 8 - int(start[1])
        x2, y2 = ord(end[0]) - ord('a'), 8 - int(end[1])
        return (x1, y1), (x2, y2)
    except:
        return None, None

def move_piece(board, start, end, current_color):
    x1, y1 = start
    x2, y2 = end
    piece = board[y1][x1]
    if piece and piece.color == current_color and piece.is_valid_move((x1, y1), (x2, y2), board):
        target = board[y2][x2]
        if target is None or target.color != current_color:
            board[y2][x2] = piece
            board[y1][x1] = None
            return True
    return False

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
