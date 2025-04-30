import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BROWN = (118, 150, 86)
GRASS_GREEN = (238, 238, 210)


def gui():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    screen.fill((255, 255, 255))

    clock = pygame.time.Clock()
    clock.tick(60)

    pygame.display.set_caption("Schach")
    font = pygame.font.Font(None, 36)
    screen.blit(font.render("Schach", True, (0, 0, 0)), (350, 10))
    draw_board(screen)
    pygame.display.flip()

def draw_board(screen):
    square_size = 60  # Grösse Schachfeld
    for y in range(8):
        for x in range(8):
            color = GRASS_GREEN if (x + y) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
    

if __name__ == "__main__":
    gui()
    input("Drücke Enter um das Programm zu beenden")
        