import pygame

from Label import Label


class LeftMenu(pygame.Surface):
    def __init__(self, h, w):
        super(LeftMenu, self).__init__((h, w), pygame.SRCALPHA)
        self.selected = 0
        self.buttons = []
        self.data = None

    def redraw(self, screen, x, y):
        self.fill((100, 100, 100, 150))

        for i, button in enumerate(self.buttons):
            button.redraw(self, i * 0, i * 120)

        screen.blit(self, self.get_rect(x=x, y=y))

    def init(self, data):
        self.data = data
        self.buttons = []
        self.buttons = [Label(500, 120, i) for i in data]
        self.setSelected(0)

    def getSelected(self):
        return self.selected

    def setSelected(self, index):
        self.selected = index
        for button in self.buttons:
            button.setSelected(False)
        self.buttons[index].setSelected(True)
