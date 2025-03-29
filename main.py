import pygame
import sys
from toolbar import Toolbar
from assets.ui_themes import get_theme
from game import Game

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FONT_PATH = "assets/ndsbios_memesbruh03.ttf"
FONT_SIZE = 16

def main():

    def exit_program():
        game.stop() 
        pygame.quit()
        sys.exit()

    pygame.init()
    theme = get_theme("neon") 
    game = Game(WINDOW_WIDTH, WINDOW_HEIGHT, theme)
    game.update_theme()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Drone")
    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)

    toolbar = Toolbar(font, WINDOW_WIDTH, theme, exit_callback=exit_program)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            toolbar.handle_event(event)

        screen.fill((0, 0, 0))
        game.draw(screen)
        toolbar.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    exit_program()

if __name__ == "__main__":
    main()