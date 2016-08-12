import pygame


class Label(pygame.Surface):
    def __init__(self, width, height, color, text):
        super(Label, self).__init__((width, height))

        self.__color = color
        self.fill(color)
        self.__font = pygame.font.Font(None, 36)
        self.__text = text
        self.__textRender = self.__font.render(self.__text, 1, (255, 255, 255))
        self.__textPos = self.__textRender.get_rect(centerx=width/2, centery=height/2)
        self.blit(self.__textRender, self.__textPos)

    def get_blit(self):
        return self, self.get_rect()
