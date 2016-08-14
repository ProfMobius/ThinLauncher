import pygame
from Constants import *


class StatusBar(pygame.Surface):
    def __init__(self, h, w):
        super(StatusBar, self).__init__((h, w), pygame.SRCALPHA)

    def redraw(self, screen, x, y):
        self.fill((150, 150, 150, 150))
        screen.blit(self, self.get_rect(x=x, y=y))
