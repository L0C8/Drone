import pygame
import random

class Game:
    def __init__(self, screen_width, screen_height, theme, map_width=64, map_height=64):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.theme = theme
        self.bg_color = self.theme.GAME_BG
        self.camera_x = 0
        self.camera_y = 0

        self.map_width = map_width
        self.map_height = map_height
        self.tile_size = 16

        self.display_rect = pygame.Rect(32, 40, 416, 416)

        self.font = pygame.font.Font("assets/ndsbios.ttf", 16)

        self.map_data = [[" " for _ in range(self.map_width)] for _ in range(self.map_height)]

        self._generate_walls()
        self.drone_pos = self._place_drone()

        self.compass_center = (self.display_rect.right + 96, 96)
        self.compass_radius = 40
    
    def _generate_walls(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                if x == 0 or y == 0 or x == self.map_width - 1 or y == self.map_height - 1:
                    self.map_data[y][x] = "#"

    def _place_drone(self):
        while True:
            x = random.randint(1, self.map_width - 2)
            y = random.randint(1, self.map_height - 2)
            if self.map_data[y][x] == " ":
                self.map_data[y][x] = "$"
                return (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.display_rect)

        visible_cols = self.display_rect.width // self.tile_size
        visible_rows = self.display_rect.height // self.tile_size

        for y in range(visible_rows):
            for x in range(visible_cols):
                map_x = self.camera_x + x
                map_y = self.camera_y + y
                if 0 <= map_x < self.map_width and 0 <= map_y < self.map_height:
                    char = self.map_data[map_y][map_x]
                    color = self.theme.TEXT_COLOR
                    if (map_x, map_y) == self.drone_pos:
                        color = self.theme.WIDGET_BG_SELECTED
                    char_surface = self.font.render(char, True, color)
                    screen.blit(char_surface, (self.display_rect.x + x * self.tile_size,
                                               self.display_rect.y + y * self.tile_size))

        pygame.draw.rect(screen, self.theme.GAME_OUTLINE, self.display_rect, 2)
        self._draw_compass(screen)

    def _draw_compass(self, screen):
        x, y = self.compass_center
        pygame.draw.circle(screen, self.theme.WIDGET_SPACER, self.compass_center, self.compass_radius, 2)
        pygame.draw.polygon(screen, self.theme.TEXT_COLOR, [(x, y - 30), (x - 10, y - 10), (x + 10, y - 10)])  # North
        pygame.draw.polygon(screen, self.theme.TEXT_COLOR, [(x, y + 30), (x - 10, y + 10), (x + 10, y + 10)])  # South
        pygame.draw.polygon(screen, self.theme.TEXT_COLOR, [(x - 30, y), (x - 10, y - 10), (x - 10, y + 10)])  # West
        pygame.draw.polygon(screen, self.theme.TEXT_COLOR, [(x + 30, y), (x + 10, y - 10), (x + 10, y + 10)])  # East

