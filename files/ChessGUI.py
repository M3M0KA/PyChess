import pygame
import os
from .logic import move_piece, create_board, set_global_variables


IMAGES_PATH = os.path.join(os.path.dirname(__file__), 'images')
piece_images = {}
pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
colors = ['w', 'b']

class ChessGUI:
    def __init__(self):
        self.current_color = 'W'
        self.temp1 = None
        self.load_images()
        self.GREEN = (118, 150, 86)
        self.WHITE = (255, 255, 255)
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
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
                    image_temp = f"{piece.color.lower()}_{piece.symbol.lower()}"
                    image = piece_images.get(image_temp)
                    if image: 
                        image = pygame.transform.scale(image, (50, 50))
                        screen.blit(image, (x * 60 + 164, y * 60 + 164)) 
                        

    def draw_board(self, screen):
        square_size = 60  # Grösse Schachfeld
        for y in range(8):
            for x in range(8):
                color = self.WHITE if (x + y) % 2 == 0 else self.GREEN
                pygame.draw.rect(screen, color, pygame.Rect(x * square_size + 160, y * square_size + 160, square_size, square_size))

    def handle_click(self, pos):
        x, y = pos
        x = (x - 160) // 60
        y = (y - 160) // 60
        if 0 <= x < 8 and 0 <= y < 8:
            if self.temp1 is None:
                if self.board[y][x] is None or self.board[y][x].color != self.current_color:
                    return
                else:
                    self.temp1 = (x, y)
                    pygame.draw.rect(self.screen, (255, 0, 0), (x * 60 + 160, y * 60 + 160, 60, 60), 3)
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

    def promotion_options(self, screen):
        font = pygame.font.Font(None, 30)
        self.size_temp = 147.5
        choices = {
            'Dame': (145, 100),
            'Turm': (275, 100),
            'Läufer': (405, 100),
            'Springer': (535, 100)
        }   
        for name, pos in choices.items():
            text = font.render(name, True, (0, 0, 0))
            button = pygame.Rect(pos[0], pos[1], 120, 50)
            pygame.draw.rect(screen, (200, 200, 200), button)
            screen.blit(text, (button.x + 10, button.y + 10))
        pygame.display.flip()
        
    def wait_for_promotion(self):
        background = pygame.Rect(0, 100, 1000, 50)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x > 145 and x < 265 and y > 100 and y < 150:
                        pygame.draw.rect(self.screen, (234, 255, 123), background)
                        pygame.display.flip()
                        return 'Dame'
                    if x > 275 and x < 395 and y > 100 and y < 150:
                        pygame.draw.rect(self.screen, (234, 255, 123), background)
                        pygame.display.flip()
                        return 'Turm'
                    if x > 405 and x < 525 and y > 100 and y < 150:
                        pygame.draw.rect(self.screen, (234, 255, 123), background)
                        pygame.display.flip()
                        return 'Läufer'
                    if x > 535 and x < 655 and y > 100 and y < 150:
                        pygame.draw.rect(self.screen, (234, 255, 123), background)
                        pygame.display.flip()
                        return 'Springer'

    def run(self):
        self.board = create_board()
        self.update(self.board)
        running = True
        is_first_move = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                    if is_first_move:
                        set_global_variables()
                    is_first_move = False
                