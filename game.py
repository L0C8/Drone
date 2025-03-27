import pygame

class Game:
    def __init__(self, screen_width, screen_height, theme):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = (0, 0, 0)  
        self.theme = theme

    def draw(self, screen):
        screen.fill(self.bg_color)

    def update_theme(self):
        self.bg_color = self.theme.GAME_BG