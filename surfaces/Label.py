import pygame
from pygame.rect import Rect
from Constants import *
from utils import AssetManager
from utils import FileSystemHelper


class Label(pygame.Surface):
    def __init__(self, width, height, data, align=ALIGN_CENTER, logo=False):
        super(Label, self).__init__((width, height), pygame.SRCALPHA)
        self.data = data
        self.selected = False
        self.align = align
        self.logo = logo

    def setSelected(self, selected):
        self.selected = selected

    def redraw(self, surface, x, y):
        if self.selected:
            color = 'colorS'
            fontColor = 'fontcolorS'
            texture = 'textureS'
        else:
            color = 'colorU'
            fontColor = 'fontcolorU'
            texture = 'textureU'

        if texture in self.data:
            self.fill((0, 0, 0, 0))
            background = AssetManager.load_image(self.data[texture])
            background = pygame.transform.smoothscale(background, (self.get_width(), self.get_height()))
            self.blit(background, background.get_rect())
        else:
            self.fill(eval(self.data[color]))

        textSurface = AssetManager.get_font(FONT_NAME, FONT_SIZE).render(self.data['name'], 1, eval(self.data[fontColor]))
        textPos = textSurface.get_rect

        offsetX = self.get_height() / 2 if self.logo else 0

        if self.align == ALIGN_CENTER:
            textPos = textSurface.get_rect(centerx=((self.get_width() - offsetX) / 2) + offsetX, centery=self.get_height() / 2)
        elif self.align == ALIGN_LEFT:
            textPos = textSurface.get_rect(x=MENU_MARGIN + offsetX, centery=self.get_height() / 2)
        elif self.align == ALIGN_RIGHT:
            raise Exception("Not implemented")

        self.blit(textSurface, textPos)

        if self.logo and 'logo' in self.data:
            image = AssetManager.load_image(self.data['logo'])
            image = pygame.transform.smoothscale(image, (self.get_height() / 2, self.get_height() / 2))
            self.blit(image, image.get_rect(x=image.get_width() / 2, centery=self.get_height() / 2))

        if self.selected and texture not in self.data:
            pygame.draw.rect(self, (0, 0, 0), Rect(0, self.get_height() - 2, self.get_width() - 20, 2))

        surface.blit(self, self.get_rect(x=x, y=y))
