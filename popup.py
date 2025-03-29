import pygame
from assets.ui_themes import get_theme, theme_definitions

class Popup:
    def __init__(self, font, title, message, theme, kind="yesno"):
        self.font = font
        self.title = title
        self.message = message
        self.kind = kind
        self.theme = theme
        self.theme_names = list(theme_definitions.keys())
        
        self.width = 360
        self.height = 180 if kind != "input" else 220
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (320, 240)

        self.visible = False
        self.result = None
        self.input_text = ""

        self.title_bar_height = 24
        self.button_width = 100
        self.button_height = 30

        self.colors = self._theme_colors()
        self.close_button_rect = pygame.Rect(self.rect.right - 28, self.rect.top + 4, 20, 16)

    def _theme_colors(self):
        return {
            "bg": self.theme.WIDGET_BG,
            "border": self.theme.GAME_OUTLINE,
            "title_bar": self.theme.WIDGET_BG_SELECTED,
            "title_outline": self.theme.WIDGET_SPACER,
            "text": self.theme.TEXT_COLOR,
            "close": (180, 60, 60)
        }

    def show(self):
        self.visible = True
        self.result = None
        self.input_text = ""

    def hide(self):
        self.visible = False

    def draw(self, screen):
        if not self.visible:
            return

        pygame.draw.rect(screen, self.colors["bg"], self.rect)
        pygame.draw.rect(screen, self.colors["border"], self.rect, 2)

        title_bar = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.title_bar_height)
        pygame.draw.rect(screen, self.colors["title_bar"], title_bar)
        pygame.draw.rect(screen, self.colors["title_outline"], title_bar, 1)

        title_surf = self.font.render(self.title, True, self.colors["text"])
        screen.blit(title_surf, (self.rect.left + 10, self.rect.top + 4))

        pygame.draw.rect(screen, self.colors["close"], self.close_button_rect)
        x_surf = self.font.render("X", True, self.colors["text"])
        screen.blit(x_surf, (self.close_button_rect.x + 5, self.close_button_rect.y + 2))

        msg_surf = self.font.render(self.message, True, self.colors["text"])
        screen.blit(msg_surf, (self.rect.left + 20, self.rect.top + 50))

        if self.kind == "yesno":
            self._draw_button(screen, "Yes", self.rect.left + 30, self.rect.bottom - 45)
            self._draw_button(screen, "No", self.rect.right - 130, self.rect.bottom - 45)
        elif self.kind == "ok":
            self._draw_button(screen, "OK", self.rect.centerx - self.button_width // 2, self.rect.bottom - 45)
        elif self.kind == "input":
            input_box = pygame.Rect(self.rect.left + 20, self.rect.top + 80, self.rect.width - 40, 30)
            pygame.draw.rect(screen, self.colors["border"], input_box, 2)
            input_surf = self.font.render(self.input_text, True, self.colors["text"])
            screen.blit(input_surf, (input_box.x + 5, input_box.y + 5))
            self._draw_button(screen, "OK", self.rect.left + 40, self.rect.bottom - 45)
            self._draw_button(screen, "Cancel", self.rect.right - 140, self.rect.bottom - 45)

    def _draw_button(self, screen, text, x, y):
        rect = pygame.Rect(x, y, self.button_width, self.button_height)
        pygame.draw.rect(screen, self.colors["border"], rect, 2)
        label = self.font.render(text, True, self.colors["text"])
        screen.blit(label, (rect.x + 20, rect.y + 5))
        setattr(self, f"{text.lower()}_rect", rect)

    def handle_event(self, event):
        if not self.visible:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button_rect.collidepoint(event.pos):
                self.result = "cancel"
                self.hide()
                return self.result

            if self.kind == "yesno":
                if self.yes_rect.collidepoint(event.pos):
                    self.result = "yes"
                    self.hide()
                    return self.result
                elif self.no_rect.collidepoint(event.pos):
                    self.result = "no"
                    self.hide()
                    return self.result

            elif self.kind == "ok":
                if self.ok_rect.collidepoint(event.pos):
                    self.result = "ok"
                    self.hide()
                    return self.result

            elif self.kind == "input":
                if self.ok_rect.collidepoint(event.pos):
                    self.result = self.input_text.strip()
                    self.hide()
                    return self.result
                elif self.cancel_rect.collidepoint(event.pos):
                    self.result = "cancel"
                    self.hide()
                    return self.result

        elif event.type == pygame.KEYDOWN and self.kind == "input":
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                self.result = self.input_text.strip()
                self.hide()
                return self.result
            else:
                self.input_text += event.unicode

        return None

class PopupSettings:
    def __init__(self, font, theme):
        self.font = font
        self.theme = theme
        self.visible = False
        self.result = None

        self.rect = pygame.Rect(0, 0, 480, 360)
        self.rect.center = (320, 240)

        self.tab_height = 32
        self.tabs = ['General', 'Themes', 'Controls']
        self.active_tab = 'General'
        self.tab_rects = []

        self.button_width = 100
        self.button_height = 30
        self.close_button_rect = pygame.Rect(self.rect.right - 28, self.rect.top + 4, 20, 16)

        self.dropdown_active = False
        self.theme_names = list(theme_definitions.keys())
        self.selected_theme = self.get_theme_name(theme)
        self.dropdown_rect = pygame.Rect(self.rect.left + 20, self.rect.top + 90, 140, 24)
        self.dropdown_items = [pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y + (i + 1) * 25, 140, 24)
                                for i in range(len(self.theme_names))]

        self._build_tabs()

    def get_theme_name(self, current_theme):
        for name, cls in theme_definitions.items():
            if isinstance(current_theme, cls):
                return name
        return 

    def _build_tabs(self):
        self.tab_rects = []
        x = self.rect.left + 10
        for tab in self.tabs:
            text_surf = self.font.render(tab, True, self.theme.TEXT_COLOR)
            rect = pygame.Rect(x, self.rect.top + 10, text_surf.get_width() + 20, self.tab_height)
            self.tab_rects.append((tab, rect))
            x += rect.width + 10


    def show(self):
        self.visible = True
        self.result = None

    def hide(self):
        self.visible = False

    def draw(self, screen):
        if not self.visible:
            return

        pygame.draw.rect(screen, self.theme.WIDGET_BG, self.rect)
        pygame.draw.rect(screen, self.theme.GAME_OUTLINE, self.rect, 2)

        pygame.draw.rect(screen, self.theme.CLOSE_COLOR, self.close_button_rect)
        x_surf = self.font.render("X", True, self.theme.TEXT_COLOR)
        screen.blit(x_surf, (self.close_button_rect.x + 5, self.close_button_rect.y + 2))

        for tab, rect in self.tab_rects:
            bg = self.theme.WIDGET_BG_SELECTED if tab == self.active_tab else self.theme.WIDGET_BG
            pygame.draw.rect(screen, bg, rect)
            pygame.draw.rect(screen, self.theme.GAME_OUTLINE, rect, 1)
            text_surf = self.font.render(tab, True, self.theme.TEXT_COLOR)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        content_rect = pygame.Rect(self.rect.left + 10, self.rect.top + self.tab_height + 30,
                                   self.rect.width - 20, self.rect.height - self.tab_height - 80)
        pygame.draw.rect(screen, self.theme.WIDGET_SPACER, content_rect)

        if self.active_tab == 'Themes':
            pygame.draw.rect(screen, self.theme.WIDGET_BG_SELECTED if self.dropdown_active else self.theme.WIDGET_BG, self.dropdown_rect)
            selected_text = self.font.render(self.selected_theme, True, self.theme.TEXT_COLOR)
            screen.blit(selected_text, (self.dropdown_rect.x + 5, self.dropdown_rect.y + 5))

            if self.dropdown_active:
                for i, rect in enumerate(self.dropdown_items):
                    pygame.draw.rect(screen, self.theme.WIDGET_BG_SELECTED, rect)
                    label = self.font.render(self.theme_names[i], True, self.theme.TEXT_COLOR)
                    screen.blit(label, (rect.x + 5, rect.y + 5))

        label = self.font.render(f"Settings: {self.active_tab} tab", True, self.theme.TEXT_COLOR)
        screen.blit(label, (content_rect.x + 10, content_rect.y + 10))

        accept_rect = pygame.Rect(self.rect.left + 30, self.rect.bottom - 40, self.button_width, self.button_height)
        cancel_rect = pygame.Rect(self.rect.right - 130, self.rect.bottom - 40, self.button_width, self.button_height)
        pygame.draw.rect(screen, self.theme.GAME_OUTLINE, accept_rect, 2)
        pygame.draw.rect(screen, self.theme.GAME_OUTLINE, cancel_rect, 2)
        screen.blit(self.font.render("Accept", True, self.theme.TEXT_COLOR), (accept_rect.x + 10, accept_rect.y + 5))
        screen.blit(self.font.render("Cancel", True, self.theme.TEXT_COLOR), (cancel_rect.x + 10, cancel_rect.y + 5))
        self.accept_rect = accept_rect
        self.cancel_rect = cancel_rect

    def handle_event(self, event):
        if not self.visible:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if self.close_button_rect.collidepoint(pos) or self.cancel_rect.collidepoint(pos):
                print("Settings cancelled")
                self.result = "cancel"
                self.hide()
                return self.result
            elif self.accept_rect.collidepoint(pos):
                print("Settings accepted")
                self.result = f"theme:{self.selected_theme}"
                self.hide()
                return self.result

            for tab, rect in self.tab_rects:
                if rect.collidepoint(pos):
                    self.active_tab = tab
                    return None

            if self.active_tab == 'Themes':
                if self.dropdown_rect.collidepoint(pos):
                    self.dropdown_active = not self.dropdown_active
                    return None
                if self.dropdown_active:
                    for i, rect in enumerate(self.dropdown_items):
                        if rect.collidepoint(pos):
                            self.selected_theme = self.theme_names[i]
                            self.dropdown_active = False
                            return None
                    self.dropdown_active = False

        elif event.type == pygame.MOUSEMOTION:
            if self.active_tab == 'Themes' and self.dropdown_active:
                bounds = self.dropdown_rect.unionall(self.dropdown_items)
                if not bounds.collidepoint(event.pos):
                    self.dropdown_active = False

        return None