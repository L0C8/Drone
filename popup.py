import pygame

class Popup:
    def __init__(self, font, message, theme):
        self.font = font
        self.message = message
        self.bg_color = theme.BG_COLOR
        self.text_color = theme.TEXT_COLOR
        self.rect = pygame.Rect(0, 0, 300, 100)
        self.rect.center = (320, 240)
        self.visible = False

        self.ok_rect = pygame.Rect(self.rect.right - 90, self.rect.bottom - 40, 70, 30)
        self.cancel_rect = pygame.Rect(self.rect.left + 20, self.rect.bottom - 40, 70, 30)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, screen):
        if not self.visible:
            return
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.text_color, self.rect, 2)

        text_surface = self.font.render(self.message, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

        pygame.draw.rect(screen, self.text_color, self.ok_rect, 1)
        screen.blit(self.font.render("OK", True, self.text_color), (self.ok_rect.x + 15, self.ok_rect.y + 5))

        pygame.draw.rect(screen, self.text_color, self.cancel_rect, 1)
        screen.blit(self.font.render("Cancel", True, self.text_color), (self.cancel_rect.x + 5, self.cancel_rect.y + 5))

    def handle_event(self, event):
        if not self.visible:
            return None
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.ok_rect.collidepoint(event.pos):
                return "ok"
            elif self.cancel_rect.collidepoint(event.pos):
                self.hide()
                return "cancel"