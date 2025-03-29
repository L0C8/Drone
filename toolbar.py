import pygame

class Toolbar:
    def __init__(self, font, screen_width, theme):
        self.font = font
        self.screen_width = screen_width
        self.theme = theme

        self.height = 32
        self.items = ['File', 'Help']
        self.item_rects = []
        self.dropdown_active = None
        self.signal = None

        self.dropdowns = {
            0: [("New Game", "new_game"), ("Test", "test_string"), ("Exit", "exit")],
            1: [("About", "about")]
        }

        self.dropdown_rects = {}
        self.build_layout()

    def set_theme(self, theme):
        self.theme = theme
        self.build_layout()

    def build_layout(self):
        x = 10
        self.item_rects = []
        for item in self.items:
            text_surf = self.font.render(item, True, self.theme.TEXT_COLOR)
            rect = pygame.Rect(x, 0, text_surf.get_width() + 20, self.height)
            self.item_rects.append((item, rect))
            x += rect.width + 10

    def draw(self, screen):
        pygame.draw.rect(screen, self.theme.WIDGET_BG, (0, 0, self.screen_width, self.height))
        for item, rect in self.item_rects:
            color = self.theme.WIDGET_BG_SELECTED if self.dropdown_active == item else self.theme.WIDGET_BG
            pygame.draw.rect(screen, color, rect)
            text_surf = self.font.render(item, True, self.theme.TEXT_COLOR)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        if self.dropdown_active:
            tab_index = self.items.index(self.dropdown_active)
            self.draw_dropdown(screen, tab_index)

    def draw_dropdown(self, screen, tab_index):
        x = self.item_rects[tab_index][1].x
        y = self.height
        width = 140
        item_height = self.height

        options = self.dropdowns.get(tab_index, [])
        self.dropdown_rects[tab_index] = []

        for i, (label, signal_value) in enumerate(options):
            rect = pygame.Rect(x, y + i * (item_height + 1), width, item_height)
            pygame.draw.rect(screen, self.theme.WIDGET_BG_SELECTED, rect)
            text = self.font.render(label, True, self.theme.TEXT_COLOR)
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
