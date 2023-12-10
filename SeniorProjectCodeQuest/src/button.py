import pygame

class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.color = (0, 128, 255)
        self.hover_color = (0, 200, 255)
        self.clicked = False

    def draw(self, surface):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(surface, color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False
