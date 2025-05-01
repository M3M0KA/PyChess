import pygame
import os

IMAGES_PATH = os.path.join(os.path.dirname(__file__), 'images')
piece_images = {}
pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
colors = ['w', 'b']

class ChessGUI:
    def __init__(self):
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
        print(board)
        print("Update GUI")
        self.board = board
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
            print(f"Klick auf Feld: ({x}, {y})")
            if self.temp1 is None:
                self.temp1 = (x, y)
            else:
                temp2 = (x, y)
                print(f"Zug von {self.temp1} nach {temp2}")


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

if __name__ == "__main__":
    gui = ChessGUI()

    # Beispielbrett mit einer weißen Dame in der Mitte
    class DummyPiece:
        def __init__(self, color, symbol):
            self.color = color
            self.symbol = symbol

    board = [[None for _ in range(8)] for _ in range(8)]
    board[3][3] = DummyPiece('w', 'queen')  # d5

    gui.update(board)

    # Haupt-Loop, damit Fenster offen bleibt
    input("Drücke Enter, um das Fenster zu schließen...")
