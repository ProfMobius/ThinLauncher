import pygame
from pygame.rect import Rect


class Label(pygame.Surface):
    def __init__(self, width, height, colorUnselected, fontColorUnselected, colorSelected, fontSelected, text):
        super(Label, self).__init__((width, height), pygame.SRCALPHA)

        self.__selected = False
        self.__width = width
        self.__height = height
        self.__colorUnselected = colorUnselected
        self.__fontColorUnselected = fontColorUnselected
        self.__colorSelected = colorSelected
        self.__fontColorSelected = fontSelected
        self.__font = pygame.font.Font(None, 72)
        self.__text = text
        self.__textRender = None
        self.__textPos = None
        self.redraw()

    def setSelected(self, selected):
        self.__selected = selected

    def get_blit(self):
        return self, self.get_rect()

    def redraw(self):
        if self.__selected:
            color = self.__colorSelected
            fontColor = self.__fontColorSelected
        else:
            color = self.__colorUnselected
            fontColor = self.__fontColorUnselected

        self.fill(color)
        self.__textRender = self.__font.render(self.__text, 1, fontColor)
        self.__textPos = self.__textRender.get_rect(centerx=self.__width / 2, centery=self.__height / 2)
        self.blit(self.__textRender, self.__textPos)
        if self.__selected:
            pygame.draw.rect(self, (0, 0, 0), Rect(0, self.__height - 2, self.__width, 2))
