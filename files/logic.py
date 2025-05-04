from .pieces import Pawn, Rook, Knight, Bishop, Queen, King, EnPassantGhost, ChessPiece
import copy


def create_board():
    board = [[None for _ in range(8)] for _ in range(8)]

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

def set_global_variables():
    global w_has_king_moved, w_has_left_rook_moved, w_has_right_rook_moved
    global b_has_king_moved, b_has_left_rook_moved, b_has_right_rook_moved
    w_has_king_moved = False
    w_has_left_rook_moved = False
    w_has_right_rook_moved = False
    b_has_king_moved = False
    b_has_left_rook_moved = False
    b_has_right_rook_moved = False

def is_rochade_possible(board, side, current_color):
    if side == "right":
        if current_color == "W":
            copy_board = copy.deepcopy(board)
            if not is_check(copy_board, "W", find_king(copy_board, "W")):
                copy_board[7][5] = King('W')
                copy_board[7][4] = None
                if not is_check(copy_board, "W", find_king(copy_board, "W")):
                    copy_board[7][6] = King('W')
                    copy_board[7][5] = None
                    if not is_check(copy_board, "W", find_king(copy_board, "W")):
                        return True
            return False
        if current_color == "B":
            copy_board = copy.deepcopy(board)
            if not is_check(copy_board, "B", find_king(copy_board, "B")):
                copy_board[0][5] = King("B")
                copy_board[0][4] = None
                if not is_check(copy_board, "B", find_king(copy_board, "B")):
                    copy_board[0][6] = King("B")
                    copy_board[0][5] = None
                    if not is_check(copy_board, "B", find_king(copy_board, "B")):
                        return True
            return False
        
    if side == "left":
        if current_color == "W":
            copy_board = copy.deepcopy(board)
            if not is_check(copy_board, "W", find_king(copy_board, "W")):
                copy_board[7][3] = King('W')
                copy_board[7][4] = None
                if not is_check(copy_board, "W", find_king(copy_board, "W")):
                    copy_board[7][2] = King('W')
                    copy_board[7][3] = None
                    if not is_check(copy_board, "W", find_king(copy_board, "W")):
                        return True
            return False
        if current_color == "B":
            copy_board = copy.deepcopy(board)
            if not is_check(copy_board, "B", find_king(copy_board, "B")):
                copy_board[0][3] = King("B")
                copy_board[0][4] = None
                if not is_check(copy_board, "B", find_king(copy_board, "B")):
                    copy_board[0][2] = King("B")
                    copy_board[0][3] = None
                    if not is_check(copy_board, "B", find_king(copy_board, "B")):
                        return True
            return False



def move_piece(board, start, end, current_color, gui):
    global w_has_king_moved, w_has_left_rook_moved, w_has_right_rook_moved
    global b_has_king_moved, b_has_left_rook_moved, b_has_right_rook_moved
    x1, y1 = start
    x2, y2 = end
    piece = board[y1][x1]
    for y in range(8):
        for x in range(8):
            if isinstance(board[y][x], EnPassantGhost):
                if board[y][x].color == current_color:
                    board[y][x] = None
    


    if current_color == 'W' and isinstance(piece, King):
        if not w_has_king_moved and y1 == 7 and x1 == 4:
            if x2 == 6 and not w_has_right_rook_moved:
                if is_rochade_possible(board, "right", current_color):
                    if board[7][5] is None and board[7][6] is None:
                        board[7][6] = King('W')
                        board[7][4] = None
                        board[7][5] = Rook('W')
                        board[7][7] = None
                        w_has_king_moved = True
                        w_has_right_rook_moved = True
                        return True
                
            if x2 == 2 and not w_has_left_rook_moved:
                if is_rochade_possible(board, "left", current_color):
                    if board[7][3] is None and board[7][2] is None and board[7][1] is None:
                        board[7][2] = King('W')
                        board[7][4] = None
                        board[7][3] = Rook('W')
                        board[7][0] = None
                        w_has_king_moved = True
                        w_has_left_rook_moved = True
                        return True
                
    if current_color == 'B' and isinstance(piece, King):
        if not b_has_king_moved and y1 == 0 and x1 == 4:
            if x2 == 6 and not b_has_right_rook_moved:
                if is_rochade_possible(board, "right", current_color):
                    if board[0][5] is None and board[0][6] is None:
                        board[0][6] = King('B')
                        board[0][4] = None
                        board[0][5] = Rook('B')
                        board[0][7] = None
                        b_has_king_moved = True
                        b_has_right_rook_moved = True
                        return True
                
            if x2 == 2 and not b_has_left_rook_moved:
                if is_rochade_possible(board, "left", current_color):
                    if board[0][3] is None and board[0][2] is None and board[0][1] is None:
                        board[0][2] = King('B')
                        board[0][4] = None
                        board[0][3] = Rook('B')
                        board[0][0] = None
                        b_has_king_moved = True
                        b_has_left_rook_moved = True
                        return True
                
    
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
            if isinstance(board[y1][x1], King):
                if current_color == 'W':
                    w_has_king_moved = True
                else:
                    b_has_king_moved = True
            if isinstance(board[y1][x1], Rook):
                if current_color == 'W':
                    if x1 == 0:
                        w_has_left_rook_moved = True
                    elif x1 == 7:
                        w_has_right_rook_moved = True
                else:
                    if x1 == 0:
                        b_has_left_rook_moved = True
                    elif x1 == 7:
                        b_has_right_rook_moved = True

            if isinstance(piece, Pawn):
                if piece.color == 'W':
                    if y1 == 6 and y2 == 4:
                        board[5][x1] = EnPassantGhost("W")
                if piece.color == 'B':
                    if y1 == 1 and y2 == 3:
                        board[2][x1] = EnPassantGhost("B")
                
                if isinstance(target, EnPassantGhost):
                    if target.color == 'W':
                        board[y2 - 1][x2] = None
                    if target.color == 'B':
                        board[y2 + 1][x2] = None

            board[y2][x2] = piece
            board[y1][x1] = None
            if is_check(board, "W", find_king(board, 'W')) and current_color == 'B' and is_checkmate(board, 'W'):
                print("Schwarz hat gewonnen!")
            if is_check(board, "B", find_king(board, 'B')) and current_color == 'W' and is_checkmate(board, 'B'):
                print("Weiss hat gewonnen!")
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
            if piece and piece.color != king_color and isinstance(piece, ChessPiece):
                if piece.is_valid_move((x, y), king_pos, board):
                    return True

def is_checkmate(board, king_color):
    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece and piece.color == king_color:
                for temp_y in range(8):
                    for temp_x in range(8):
                        if piece.is_valid_move((x, y), (temp_x, temp_y), board):
                            temp_board = copy.deepcopy(board)
                            temp_board[temp_y][temp_x] = piece
                            temp_board[y][x] = None
                            if not is_check(temp_board, king_color, find_king(temp_board, king_color)):
                                print(temp_x, temp_y, piece.color, piece.symbol)
                                return False
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
