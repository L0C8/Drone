import pygame
import sys
from popup import Popup

class Toolbar:
    def __init__(self, font, screen_width, theme):
        self.font = font
        self.height = 32
        self.bg_color = theme.BG_COLOR
        self.bg_color_selected = theme.BG_COLOR_SELECTED
        self.bg_spacer = theme.BG_SPACER
        self.text_color = theme.TEXT_COLOR
        self.items = ['File', 'Help']
        self.item_rects = []
        self.dropdown_active = None
        self.screen_width = screen_width
        self.exit_rect = None
        self.about_rect = None
        self.new_game_rect = None
        self.build_toolbar()
        self.popup = Popup(font, "Are you sure you want to exit?", theme)

    def build_toolbar(self):
        x_offset = 10
        self.item_rects = []
        for item in self.items:
            text_surface = self.font.render(item, True, self.text_color)
            rect = pygame.Rect(x_offset, 0, text_surface.get_width() + 20, self.height)
            self.item_rects.append((item, rect))
            x_offset += rect.width + 10

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, (0, 0, self.screen_width, self.height))
        for item, rect in self.item_rects:
            color = self.bg_color_selected if self.dropdown_active == item else self.bg_color
            pygame.draw.rect(screen, color, rect)
            text_surface = self.font.render(item, True, self.text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

        if self.dropdown_active == 'File':
            self.draw_file_dropdown(screen)
        elif self.dropdown_active == 'Help':
            self.draw_help_dropdown(screen)
        
        self.popup.draw(screen)

    def draw_file_dropdown(self, screen):
        x = self.item_rects[0][1].left
        y = self.height
        width = 100
        item_height = self.height

        new_game_rect = pygame.Rect(x, y, width, item_height)
        exit_rect = pygame.Rect(x, y + item_height + 1, width, item_height)

        pygame.draw.rect(screen, self.bg_color_selected, new_game_rect)
        new_game_text = self.font.render("New Game", True, self.text_color)
        screen.blit(new_game_text, (new_game_rect.left + 5, new_game_rect.top + 8))

        pygame.draw.line(screen, self.bg_spacer, (x, y + item_height), (x + width-1, y + item_height))

        pygame.draw.rect(screen, self.bg_color_selected, exit_rect)
        exit_text = self.font.render("Exit", True, self.text_color)
        screen.blit(exit_text, (exit_rect.left + 5, exit_rect.top + 8))

        self.new_game_rect = new_game_rect
        self.exit_rect = exit_rect

    def draw_help_dropdown(self, screen):
        about_rect = pygame.Rect(self.item_rects[1][1].left, self.height, 100, self.height)
        pygame.draw.rect(screen, self.bg_color_selected, about_rect)
        about_text = self.font.render("About", True, self.text_color)
        screen.blit(about_text, (about_rect.left + 5, about_rect.top + 8))
        self.about_rect = about_rect

    def handle_event(self, event):
        if self.popup.visible:
            result = self.popup.handle_event(event)
            if result == "ok":
                pygame.quit()
                sys.exit()
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            clicked_on_tab = False
            for item, rect in self.item_rects:
                if rect.collidepoint(mouse_pos):
                    clicked_on_tab = True
                    if self.dropdown_active == item:
                        self.dropdown_active = None
                    else:
                        self.dropdown_active = item
                    return

            if self.dropdown_active == 'File':
                if self.new_game_rect and self.new_game_rect.collidepoint(mouse_pos):
                    print("New Game clicked")
                elif self.exit_rect and self.exit_rect.collidepoint(mouse_pos):
                    self.popup.show()

            if self.dropdown_active == 'Help' and self.about_rect and self.about_rect.collidepoint(mouse_pos):
                print("About clicked")

            if not clicked_on_tab:
                self.dropdown_active = None

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            dropdown_rect = None
            tab_rect = None

            if self.dropdown_active == 'File' and self.new_game_rect and self.exit_rect:
                dropdown_rect = self.new_game_rect.union(self.exit_rect)
                tab_rect = self.item_rects[0][1]
            elif self.dropdown_active == 'Help' and self.about_rect:
                dropdown_rect = self.about_rect
                tab_rect = self.item_rects[1][1]

            if dropdown_rect and tab_rect:
                combined_area = dropdown_rect.union(tab_rect)
                if not combined_area.collidepoint(mouse_pos):
                    self.dropdown_active = None