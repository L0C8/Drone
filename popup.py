import pygame

class Popup:
    def __init__(self, font, title, message, theme, kind="yesno"):
        self.font = font
        self.title = title
        self.message = message
        self.kind = kind  # yesno, ok, input
        self.theme = theme

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
