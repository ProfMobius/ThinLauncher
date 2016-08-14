import pygame
from pygame.rect import Rect


class Label(pygame.Surface):
    def __init__(self, width, height, data):
        super(Label, self).__init__((width, height), pygame.SRCALPHA)
        self.data = data
        self.selected = False

    def setSelected(self, selected):
        self.selected = selected

    def redraw(self, surface, x, y):
        if self.selected:
            color = 'colorS'
            fontColor = 'fontcolorS'
        else:
            color = 'colorU'
            fontColor = 'fontcolorU'

        self.fill(eval(self.data[color]))

        textSurface = pygame.font.Font(None, 72).render(self.data['name'], 1, eval(self.data[fontColor]))
        textPos = textSurface.get_rect(centerx=self.get_width() / 2, centery=self.get_height() / 2)
        self.blit(textSurface, textPos)

        if self.selected:
            pygame.draw.rect(self, (0,0,0), Rect(0, self.get_height() - 2, self.get_width() - 20, 2))

        surface.blit(self, self.get_rect(x=x, y=y))
