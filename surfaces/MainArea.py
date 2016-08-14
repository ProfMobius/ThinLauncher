import pygame


class MainArea(pygame.Surface):
    def __init__(self, h, w):
        super(MainArea, self).__init__((h, w), pygame.SRCALPHA)
        self.selected = 0

    def redraw(self, screen, x, y):
        self.fill((255, 0, 255, 150))
        screen.blit(self, self.get_rect(x=x, y=y))