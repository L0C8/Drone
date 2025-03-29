import pygame
import sys
import os
from toolbar import Toolbar
from popup import Popup, PopupSettings
from assets.ui_themes import get_theme

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

        self.theme_name = self.load_data()
        self.theme = get_theme(self.theme_name)
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

        self.toolbar = Toolbar(self.font, WINDOW_WIDTH, self.theme)
        self.popups = []

    def load_data(self):
        save_path = ".runtimedata"
        if not os.path.exists(save_path):
            with open(save_path, "w") as f:
                f.write("dark")
            return "dark"
        with open(save_path, "r") as f:
            theme_name = f.read().strip()
            return theme_name if theme_name else "dark"

    def save_data(self):
        with open(".runtimedata", "w") as f:
            f.write(self.theme_name)

    def set_theme(self, theme_name):
        self.theme_name = theme_name
        self.theme = get_theme(theme_name)
        self.toolbar.set_theme(self.theme)
        self.save_data()

    def _quit(self):
        self.running = False

    def handle_popup_result(self, popup, result):
        title = popup.title.lower()
        if title == "confirm exit" and result == "yes":
            self._quit()
        elif title == "new game" and result == "yes":
            print("Starting new game!")
        elif title == "enter string" and result != "cancel":
            print(f"User input: {result}")
        else:
            print(f"Popup result for '{title}': {result}")

    def create_popup_from_signal(self, signal):
        popup = None
        if signal == "exit":
            popup = Popup(self.font, "Confirm Exit", "Are you sure you want to quit?", self.theme, kind="yesno")
        elif signal == "new_game":
            popup = Popup(self.font, "New Game", "Start a new game?", self.theme, kind="yesno")
        elif signal == "test_string":
            popup = Popup(self.font, "Enter String", "Give me a string?", self.theme, kind="input")
        elif signal == "settings":
            popup = PopupSettings(self.font, self.theme)
        elif signal.startswith("theme:"):
            new_theme = signal.split(":")[1]
            print("Switching theme to:", new_theme)
            self.set_theme(new_theme)
            return
        else:
            print(f"Unhandled signal: {signal}")

        if popup:
            popup.show()
            self.popups.append(popup)

    def handle_event(self, event):
        if self.popups:
            popup = self.popups[-1]
            result = popup.handle_event(event)
            if result:
                self.handle_popup_result(popup, result)
                self.popups.pop()
            return

        self.toolbar.handle_event(event)
        if self.toolbar.signal:
            self.create_popup_from_signal(self.toolbar.signal)
            self.toolbar.signal = None

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit()
                self.handle_event(event)

            self.screen.fill(self.theme.GAME_BG)
            self.toolbar.draw(self.screen)
            for popup in self.popups:
                popup.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = MainApp()
    app.run()