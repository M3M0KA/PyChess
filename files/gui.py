import pygame
import os

IMAGES_PATH = os.path.join(os.path.dirname(__file__), 'images')
piece_images = {}
pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
colors = ['w', 'b']

class ChessGUI:
    def __init__(self):
        self.load_images()
        self.DARK_BROWN = (118, 150, 86)
        self.GRASS_GREEN = (238, 238, 210)
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.screen.fill((255, 255, 255))
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
                    print(f"Bild geladen: {image_path}")
                else:
                    print(f"Bild nicht gefunden: {image_path}")


    def update(self, board):
        print("Update GUI")
        self.board = board
        self.draw_board(self.screen)  # ← Brett neu zeichnen
        self.draw_pieces(board, self.screen)
        pygame.display.flip()


    def draw_pieces(self, board, screen):
        for y in range(8):
            for x in range(8):
                piece = board[y][x]
                if piece:
                    image_temp = f"{piece.color.lower()}_{piece.symbol.lower()}"
                    image = piece_images.get(image_temp)
                    print("image loaded")
                    if image: 
                        image = pygame.transform.scale(image, (50, 50))
                        screen.blit(image, (x * 60 + 160, y * 60 + 160))

    def draw_board(self, screen):
        square_size = 60  # Grösse Schachfeld
        for y in range(8):
            for x in range(8):
                color = self.GRASS_GREEN if (x + y) % 2 == 0 else self.DARK_BROWN
                pygame.draw.rect(screen, color, pygame.Rect(x * square_size + 160, y * square_size + 160, square_size, square_size))
    
gui = ChessGUI()