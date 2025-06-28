import pygame
import os
from .logic import move_piece, create_board, set_global_variables
from .pieces import ChessPiece

IMAGES_PATH = os.path.join(os.path.dirname(__file__), 'temp_images')
piece_images = {}
pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
colors = ['w', 'b']

class ChessGUI:
    def __init__(self, windowsize):
        self.windowsize = windowsize
        self.current_color = 'W'
        self.temp1 = None
        self.load_images()
        self.GREEN = (118, 150, 86)
        self.WHITE = (255, 255, 255)
        pygame.init()
        self.screen = pygame.display.set_mode((windowsize, windowsize))
        self.screen.fill((234,255,123))
        self.clock = pygame.time.Clock()
        self.clock.tick(60)
        pygame.display.set_caption("Schach")
        font = pygame.font.Font(None, 36)
        self.screen.blit(font.render("Schach", True, (0, 0, 0)), (350, 10))
        self.draw_board(self.screen)
        pygame.display.flip()
    
    def load_images(self):
        for piece in pieces:
            for color in colors:
                key = f"{color}_{piece}"
                image_path = os.path.join(IMAGES_PATH, f"{key}.png")

                if os.path.exists(image_path):
                    piece_images[key] = pygame.image.load(image_path)
                else:
                    print(f"Bild nicht gefunden: {image_path}")


    def update(self, board):
        self.draw_board(self.screen)
        self.draw_pieces(board, self.screen)
        pygame.display.flip()


    def draw_pieces(self, board, screen):
        for y in range(8):
            for x in range(8):
                piece = board[y][x]
                if piece:
                    if isinstance(piece, ChessPiece):
                        image_temp = f"{piece.color.lower()}_{piece.symbol.lower()}"
                        image = piece_images.get(image_temp)
                        if image:
                            image = pygame.transform.scale(image, ((0.0625 * self.windowsize), (0.0625 * self.windowsize)))
                            screen.blit(image, (x * (self.windowsize / 13.33333) + (0.205 * self.windowsize), y * (self.windowsize / 13.33333) + (0.205 * self.windowsize)))
                        

    def draw_board(self, screen):
        square_size = (self.windowsize / 13.33333)  # Grösse Schachfeld
        for y in range(8):
            for x in range(8):
                color = self.WHITE if (x + y) % 2 == 0 else self.GREEN
                pygame.draw.rect(screen, color, pygame.Rect(x * square_size + (self.windowsize / 5), y * square_size + (self.windowsize / 5), square_size, square_size))

    def handle_click(self, pos):
        x, y = pos
        x = int((x - (self.windowsize/5)) // (0.075 * self.windowsize))
        y = int((y - (self.windowsize/5)) // (0.075 * self.windowsize))
        print(x, y)
        if 0 <= x < 8 and 0 <= y < 8:
            if self.temp1 is None:
                if self.board[y][x] is None or self.board[y][x].color != self.current_color or isinstance(self.board[y][x], ChessPiece) == False:
                    return
                else:
                    self.temp1 = (x, y)
                    pygame.draw.rect(self.screen, (255, 0, 0), (x * (self.windowsize/13.33333) + (self.windowsize/5), y * (self.windowsize/13.33333) + (self.windowsize/5), (self.windowsize/13.33333), (self.windowsize/13.33333)), 3)
                    pygame.display.flip()
            else:
                self.temp2 = (x, y)
                start, end = self.temp1, self.temp2
                if start and end:
                    if move_piece(self.board, start, end, self.current_color, self):
                        self.current_color = 'B' if self.current_color == 'W' else 'W'
                    else:
                        print("Ungültiger Zug!")
                else:
                    print("Eingabefehler!")
                self.update(self.board)
                self.temp1 = None
                self.temp2 = None

    def win(self, winner):
        font = pygame.font.Font(None, 50)
        if winner == "stalemate":
            text = font.render("Unentschieden!", True, (0, 0, 0))
        else:
            text = font.render(f"{winner} gewinnt!", True, (0, 0, 0))
        self.screen.blit(text, ((0.4375 * self.windowsize), (0.875 * self.windowsize)))
        pygame.display.flip()
        global someone_won
        someone_won = True

    def promotion_options(self, screen):
        font = pygame.font.Font(None, 30)
        choices = {
            'Dame': ((0.18125 * self.windowsize), (0.125 * self.windowsize)),
            'Turm': ((0.34375 * self.windowsize), (0.125 * self.windowsize)),
            'Läufer': ((0.50625 * self.windowsize), (0.125 * self.windowsize)),
            'Springer': ((0.66875 * self.windowsize), (0.125 * self.windowsize))
        }   
        for name, pos in choices.items():
            text = font.render(name, True, (0, 0, 0))
            button = pygame.Rect(pos[0], pos[1], (0.15 * self.windowsize), (0.0625 * self.windowsize))
            pygame.draw.rect(screen, (200, 200, 200), button)
            screen.blit(text, (button.x + (0.0125 * self.windowsize), button.y + (0.0125 * self.windowsize)))
        pygame.display.flip()
        
    def wait_for_promotion(self):
        background = pygame.Rect(0, (0.125 * self.windowsize), self.windowsize, (0.0625 * self.windowsize))
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x > (0.18125 * self.windowsize) and x < (0.33125 * self.windowsize) and y > (self.windowsize * 0.125) and y < (0.1875 * self.windowsize):
                        pygame.draw.rect(self.screen, (234, 255, 123), background)
                        pygame.display.flip()
                        return 'Dame'
                    if x > (0.34375 * self.windowsize) and x < (0.49375 * self.windowsize) and y > (self.windowsize * 0.125) and y < (0.1875 * self.windowsize):
                        pygame.draw.rect(self.screen, (234, 255, 123), background)
                        pygame.display.flip()
                        return 'Turm'
                    if x > (0.50625 * self.windowsize) and x < (0.65625 * self.windowsize) and y > (self.windowsize * 0.125) and y < (0.1875 * self.windowsize):
                        pygame.draw.rect(self.screen, (234, 255, 123), background)
                        pygame.display.flip()
                        return 'Läufer'
                    if x > (0.66875 * self.windowsize) and x < (0.81875 * self.windowsize) and y > (self.windowsize * 0.125) and y < (0.1875 * self.windowsize):
                        pygame.draw.rect(self.screen, (234, 255, 123), background)
                        pygame.display.flip()
                        return 'Springer'

    def run(self):
        self.board = create_board()
        self.update(self.board)
        running = True
        is_first_move = True
        global someone_won
        someone_won = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if someone_won:
                        break
                    self.handle_click(event.pos)
                    if is_first_move:
                        set_global_variables()
                    is_first_move = False
                