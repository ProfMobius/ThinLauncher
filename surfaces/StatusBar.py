import pygame
from Constants import *


class StatusBar(pygame.Surface):
    def __init__(self, w, h):
        super(StatusBar, self).__init__((w, h), pygame.SRCALPHA)

    def redraw(self, screen, x, y):
        self.fill((150, 150, 150, 150))
        screen.blit(self, self.get_rect(x=x, y=y))
