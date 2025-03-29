import pygame
import random

class Game:
    def __init__(self, screen_width, screen_height, theme, map_width=64, map_height=64):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.theme = theme
        self.bg_color = self.theme.GAME_BG

        self.map_width = map_width
        self.map_height = map_height
        self.tile_size = 16 

        self.display_rect = pygame.Rect(32, 40, 416, 416)

        self.font = pygame.font.Font("assets/ndsbios.ttf", 16)

        self.map_data = [[" " for _ in range(self.map_width)] for _ in range(self.map_height)]

        self._sprinkle_test_chars()

    def _sprinkle_test_chars(self):
        total_tiles = self.map_width * self.map_height
        num_sprites = total_tiles // 4 
        for _ in range(num_sprites):
            x = random.randint(0, self.map_width - 1)
            y = random.randint(0, self.map_height - 1)
            self.map_data[y][x] = "%"

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.display_rect)

        visible_cols = self.display_rect.width // self.tile_size
        visible_rows = self.display_rect.height // self.tile_size

        for y in range(visible_rows):
            for x in range(visible_cols):
                map_x = x
                map_y = y
                char = self.map_data[map_y][map_x]
                char_surface = self.font.render(char, True, self.theme.TEXT_COLOR)
                screen.blit(char_surface, (self.display_rect.x + x * self.tile_size,
                                           self.display_rect.y + y * self.tile_size))

        pygame.draw.rect(screen, self.theme.GAME_OUTLINE, self.display_rect, 2)

    def update_theme(self):
        self.bg_color = self.theme.GAME_BG
