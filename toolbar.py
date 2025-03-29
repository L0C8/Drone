import pygame

class Toolbar:
    def __init__(self, font, screen_width):
        self.font = font
        self.screen_width = screen_width
        self.height = 32
        self.items = ['File', 'Help']
        self.item_rects = []
        self.dropdown_active = None
        self.signal = None

        self.bg_color = (50, 50, 50)
        self.bg_color_selected = (65, 65, 65)
        self.text_color = (255, 255, 255)

        self.dropdowns = {
            0: [("New Game", "new_game"), ("Exit", "exit")],
            1: [("About", "about")]
        }

        self.dropdown_rects = {}

        self.build_layout()

    def build_layout(self):
        x = 10
        self.item_rects = []
        for item in self.items:
            text_surf = self.font.render(item, True, self.text_color)
            rect = pygame.Rect(x, 0, text_surf.get_width() + 20, self.height)
            self.item_rects.append((item, rect))
            x += rect.width + 10

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, (0, 0, self.screen_width, self.height))
        for item, rect in self.item_rects:
            color = self.bg_color_selected if self.dropdown_active == item else self.bg_color
            pygame.draw.rect(screen, color, rect)
            text_surf = self.font.render(item, True, self.text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        if self.dropdown_active:
            tab_index = self.items.index(self.dropdown_active)
            self.draw_dropdown(screen, tab_index)

    def draw_dropdown(self, screen, tab_index):
        x = self.item_rects[tab_index][1].x
        y = self.height
        width = 100
        item_height = self.height

        options = self.dropdowns.get(tab_index, [])
        self.dropdown_rects[tab_index] = []

        for i, (label, signal_value) in enumerate(options):
            rect = pygame.Rect(x, y + i * (item_height + 1), width, item_height)
            pygame.draw.rect(screen, self.bg_color_selected, rect)
            text = self.font.render(label, True, self.text_color)
            screen.blit(text, (rect.x + 5, rect.y + 8))
            self.dropdown_rects[tab_index].append((rect, signal_value))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            clicked_tab = False
            for item, rect in self.item_rects:
                if rect.collidepoint(pos):
                    clicked_tab = True
                    if self.dropdown_active == item:
                        self.dropdown_active = None
                    else:
                        self.dropdown_active = item
                    return

            if self.dropdown_active:
                tab_index = self.items.index(self.dropdown_active)
                for rect, signal_value in self.dropdown_rects.get(tab_index, []):
                    if rect.collidepoint(pos):
                        self.signal = signal_value

            if not clicked_tab:
                self.dropdown_active = None
