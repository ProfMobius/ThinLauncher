import pygame
from pygame.rect import Rect


class Label(pygame.Surface):
    def __init__(self, width, height, color, text):
        super(Label, self).__init__((width, height))

        self.__selected = False
        self.__width = width
        self.__height = height
        self.__color = color
        self.__font = pygame.font.Font(None, 36)
        self.__text = text
        self.__textRender = None
        self.__textPos = None
        self.redraw()

    def setSelected(self, selected):
        self.__selected = selected

    def get_blit(self):
        return self, self.get_rect()

    def redraw(self):
        self.fill(self.__color)
        self.__textRender = self.__font.render(self.__text, 1, (255, 255, 255))
        self.__textPos = self.__textRender.get_rect(centerx=self.__width / 2, centery=self.__height / 2)
        self.blit(self.__textRender, self.__textPos)
        if self.__selected:
            pygame.draw.rect(self, (255, 255, 255), Rect(0, self.__height - 5, 50, 5))
