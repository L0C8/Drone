import pygame
import sys
from toolbar import Toolbar

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 60
FONT_PATH = "assets/ndsbios.ttf"
FONT_SIZE = 16

class MainApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Drone")
        self.clock = pygame.time.Clock()
        self.running = True

        # Load font
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

        # Core components
        self.toolbar = Toolbar(self.font, WINDOW_WIDTH)
        self.game = None  # To be added later

    def handle_global_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        # Pass event to components
        if self.toolbar:
            self.toolbar.handle_event(event)
        if self.game:
            self.game.handle_event(event)

    def process_signals(self):
        if self.toolbar and self.toolbar.signal:
            signal = self.toolbar.signal

            if signal == "exit":
                self.running = False
            elif signal == "new_game":
                print("New Game triggered (not yet implemented)")
            elif signal == "about":
                print("About clicked (popup not implemented)")
            else:
                print("undefined action")

            self.toolbar.signal = None

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_global_event(event)

            self.process_signals()

            self.screen.fill((30, 30, 30))  # fallback background

            if self.game:
                self.game.draw(self.screen)
            if self.toolbar:
                self.toolbar.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = MainApp()
    app.run()
