import os
import threading
from .engine.engine import Engine

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from .logic import move_piece, create_board, set_global_variables, board_to_fen
from .pieces import ChessPiece
from .images import image_editor

piece_images = {}
pieces = ["pawn", "rook", "knight", "bishop", "queen", "king"]
colors = ["w", "b"]


class ChessGUI:
    def __init__(self, windowsize, boardcolor, path, darkmode, ai, playblack):
        self.engine = Engine()
        self.darkmode = darkmode
        self.ai = ai
        self.doupdate = False
        self.thinking = False
        self.playblack = playblack
        self.path = path
        self.windowsize = windowsize
        self.current_color = "W"
        self.temp1 = None
        self.load_images()

        print(self.darkmode)
        if self.darkmode == 1:
            self.WHITE = (0, 0, 0)
        else:
            self.WHITE = (255, 255, 255)

        if boardcolor == "classic1":
            self.DARK = (129, 169, 97)
            self.BRIGHT = (255, 250, 223)

        if boardcolor == "gray1":
            self.DARK = (191, 193, 139)
            self.BRIGHT = (236, 234, 240)

        if boardcolor == "classic2":
            self.DARK = (179, 136, 101)
            self.BRIGHT = (234, 219, 183)

        if boardcolor == "gold1":
            self.DARK = (189, 134, 21)
            self.BRIGHT = (204, 207, 189)

        if boardcolor == "pink1":
            self.DARK = (236, 119, 117)
            self.BRIGHT = (233, 241, 191)

        if boardcolor == "gray2":
            self.DARK = (132, 123, 197)
            self.BRIGHT = (171, 162, 145)

        if boardcolor == "blue1":
            self.DARK = (76, 119, 171)
            self.BRIGHT = (197, 203, 215)

        if boardcolor == "violet1":
            self.DARK = (149, 123, 179)
            self.BRIGHT = (229, 213, 241)

        if boardcolor == "green1":
            self.DARK = (88, 148, 96)
            self.BRIGHT = (239, 246, 182)

        if boardcolor == "gray3":
            self.DARK = (140, 162, 172)
            self.BRIGHT = (223, 227, 228)

        if boardcolor == "red1":
            self.DARK = (166, 208, 221)
            self.BRIGHT = (252, 59, 64)

        if boardcolor == "vanilla1":
            self.DARK = (237, 214, 180)
            self.BRIGHT = (255, 241, 206)

        if boardcolor == "gray4":
            self.DARK = (95, 94, 93)
            self.BRIGHT = (139, 156, 154)

        pygame.init()
        self.icon = pygame.image.load(
            os.path.join(os.path.dirname(__file__), "icon.png")
        )
        pygame.display.set_icon(self.icon)
        self.screen = pygame.display.set_mode((windowsize, windowsize))
        self.screen.fill((self.WHITE))
        self.clock = pygame.time.Clock()
        self.clock.tick(60)
        pygame.display.set_caption("Schach")
        font = pygame.font.Font(None, int(0.045 * self.windowsize))
        if self.darkmode:
            self.screen.blit(
                font.render("Schach", True, (255, 255, 255)),
                ((0.4375 * self.windowsize), (0.0125 * self.windowsize)),
            )
        else:
            self.screen.blit(
                font.render("Schach", True, (0, 0, 0)),
                ((0.4375 * self.windowsize), (0.0125 * self.windowsize)),
            )
        self.draw_board(self.screen)
        pygame.display.flip()

    def load_images(self):
        for piece in pieces:
            for color in colors:
                key = f"{color}_{piece}"
                image_path = os.path.join(self.path, f"{key}.png")

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
                            image = pygame.transform.scale(
                                image,
                                (
                                    (0.0625 * self.windowsize),
                                    (0.0625 * self.windowsize),
                                ),
                            )
                            screen.blit(
                                image,
                                (
                                    x * (self.windowsize / 13.33333)
                                    + (0.205 * self.windowsize),
                                    y * (self.windowsize / 13.33333)
                                    + (0.205 * self.windowsize),
                                ),
                            )

    def draw_board(self, screen):
        board_size = self.windowsize * 0.6
        square_size = board_size / 8
        for y in range(8):
            for x in range(8):
                color = self.BRIGHT if (x + y) % 2 == 0 else self.DARK
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(
                        x * square_size + (self.windowsize / 5),
                        y * square_size + (self.windowsize / 5),
                        square_size,
                        square_size,
                    ),
                )

    def handle_click(self, pos):
        x, y = pos
        x = int((x - (self.windowsize / 5)) // (0.075 * self.windowsize))
        y = int((y - (self.windowsize / 5)) // (0.075 * self.windowsize))
        if 0 <= x < 8 and 0 <= y < 8:
            if self.temp1 is None:
                if (
                    self.board[y][x] is None
                    or self.board[y][x].color != self.current_color
                    or not isinstance(self.board[y][x], ChessPiece)
                ):
                    return
                else:
                    self.temp1 = (x, y)
                    pygame.draw.rect(
                        self.screen,
                        (255, 0, 0),
                        (
                            x * (self.windowsize / 13.33333) + (self.windowsize / 5),
                            y * (self.windowsize / 13.33333) + (self.windowsize / 5),
                            (self.windowsize / 13.33333),
                            (self.windowsize / 13.33333),
                        ),
                        3,
                    )
                    pygame.display.flip()
            else:
                self.temp2 = (x, y)
                start, end = self.temp1, self.temp2
                if start and end:
                    if move_piece(
                        self.board, start, end, self.current_color, False, self
                    ):
                        self.current_color = "B" if self.current_color == "W" else "W"
                    else:
                        print("Ungültiger Zug!")
                else:
                    print("Eingabefehler!")
                self.update(self.board)
                self.temp1 = None
                self.temp2 = None

    def generate_ai_move(self):
        self.ai_move = self.engine.handle_fen(
            board_to_fen(self.board, self.current_color)
        )[0].uci()
        self.ai_do_move(
            *self.engine.twoindexreturn(self.engine.uci_to_index(self.ai_move)),
            self.ai_move,
        )

    def ai_do_move(self, pos1, pos2, move):
        if (
            self.board[pos1[1]][pos1[0]] is None
            or self.board[pos1[1]][pos1[0]].color != ("W" if self.playblack else "B")
            or not isinstance(self.board[pos1[1]][pos1[0]], ChessPiece)
        ):
            self.thinking = False
            print("NVM")
            print("AI move failed")
            print("Board FEN:", board_to_fen(self.board, self.current_color))
            print(*self.engine.twoindexreturn(self.engine.uci_to_index(move)))
            return "NVM"

        start, end = pos1, pos2
        if move_piece(
            self.board, start, end, "W" if self.playblack else "B", True, self
        ):
            self.thinking = False
            self.current_color = "B" if self.playblack else "W"
        else:
            self.thinking = False
            print("NVM")
            print("AI move failed")
            print("Board FEN:", board_to_fen(self.board, self.current_color))
            print(*self.engine.twoindexreturn(self.engine.uci_to_index(move)))
            return "NVM"
        self.doupdate = True

    def win(self, winner):
        font = pygame.font.Font(None, 50)
        if winner == "stalemate":
            if self.darkmode:
                text = font.render("Unentschieden!", True, (255, 255, 255))
            else:
                text = font.render("Unentschieden!", True, (0, 0, 0))
        else:
            if self.darkmode:
                text = font.render(f"{winner} gewinnt!", True, (255, 255, 255))
            else:
                text = font.render(f"{winner} gewinnt!", True, (0, 0, 0))
        self.screen.blit(text, ((0.4375 * self.windowsize), (0.875 * self.windowsize)))
        pygame.display.flip()
        self.someone_won = True

    def show_ai_thinking(self, thinking):
        if thinking:
            font = pygame.font.Font(None, int(0.0375 * self.windowsize))
            if self.darkmode:
                text = font.render("KI denkt...", True, (255, 255, 255))
            else:
                text = font.render("KI denkt...", True, (0, 0, 0))
            self.screen.blit(
                text,
                ((0.4375 * self.windowsize), (0.0625 * self.windowsize)),
            )
        else:
            if self.darkmode:
                color = (0, 0, 0)
            else:
                color = (255, 255, 255)
            rect = pygame.Rect(
                0,
                (0.0625 * self.windowsize),
                self.windowsize,
                (0.0375 * self.windowsize),
            )
            pygame.draw.rect(self.screen, color, rect)
        pygame.display.flip()

    def promotion_options(self, screen):
        font = pygame.font.Font(None, int(0.0375 * self.windowsize))
        choices = {
            "Dame": ((0.18125 * self.windowsize), (0.125 * self.windowsize)),
            "Turm": ((0.34375 * self.windowsize), (0.125 * self.windowsize)),
            "Läufer": ((0.50625 * self.windowsize), (0.125 * self.windowsize)),
            "Springer": ((0.66875 * self.windowsize), (0.125 * self.windowsize)),
        }
        for name, pos in choices.items():
            text = font.render(name, True, (0, 0, 0))
            button = pygame.Rect(
                pos[0], pos[1], (0.15 * self.windowsize), (0.0625 * self.windowsize)
            )
            pygame.draw.rect(screen, (200, 200, 200), button)
            screen.blit(
                text,
                (
                    button.x + (0.0125 * self.windowsize),
                    button.y + (0.0125 * self.windowsize),
                ),
            )
        pygame.display.flip()

    def wait_for_promotion(self):
        if self.ai and self.current_color == ("W" if self.playblack else "B"):
            return "Dame"
        background = pygame.Rect(
            0, (0.125 * self.windowsize), self.windowsize, (0.0625 * self.windowsize)
        )
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.darkmode:
                        color = (0, 0, 0)
                    else:
                        color = (255, 255, 255)
                    if (
                        x > (0.18125 * self.windowsize)
                        and x < (0.33125 * self.windowsize)
                        and y > (self.windowsize * 0.125)
                        and y < (0.1875 * self.windowsize)
                    ):
                        pygame.draw.rect(self.screen, color, background)
                        pygame.display.flip()
                        return "Dame"
                    if (
                        x > (0.34375 * self.windowsize)
                        and x < (0.49375 * self.windowsize)
                        and y > (self.windowsize * 0.125)
                        and y < (0.1875 * self.windowsize)
                    ):
                        pygame.draw.rect(self.screen, color, background)
                        pygame.display.flip()
                        return "Turm"
                    if (
                        x > (0.50625 * self.windowsize)
                        and x < (0.65625 * self.windowsize)
                        and y > (self.windowsize * 0.125)
                        and y < (0.1875 * self.windowsize)
                    ):
                        pygame.draw.rect(self.screen, color, background)
                        pygame.display.flip()
                        return "Läufer"
                    if (
                        x > (0.66875 * self.windowsize)
                        and x < (0.81875 * self.windowsize)
                        and y > (self.windowsize * 0.125)
                        and y < (0.1875 * self.windowsize)
                    ):
                        pygame.draw.rect(self.screen, color, background)
                        pygame.display.flip()
                        return "Springer"

    def run(self):
        self.board = create_board()
        self.update(self.board)
        self.running = True
        self.someone_won = False
        set_global_variables()
        clock = pygame.time.Clock()
        while self.running:
            if self.doupdate:
                self.update(self.board)
                self.show_ai_thinking(False)
                self.doupdate = False

            if self.someone_won:
                while True:
                    for event in pygame.event.get():
                        if (
                            event.type == pygame.QUIT
                            or event.type == pygame.MOUSEBUTTONDOWN
                        ):
                            self.running = False
                            break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if self.thinking:
                    continue
                if self.ai and self.current_color == ("W" if self.playblack else "B"):
                    self.thinking = True
                    self.show_ai_thinking(True)
                    threading.Thread(target=self.generate_ai_move).start()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            clock.tick(60)

        image_editor(None).rmv()
        pygame.quit()
