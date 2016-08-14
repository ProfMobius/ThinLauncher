import pygame

from Label import Label


class TopMenu(pygame.Surface):
    def __init__(self, h, w):
        super(TopMenu, self).__init__((h, w), pygame.SRCALPHA)
        self.selected = 0
        self.buttons = []
        self.buttonWidth = 0
        self.data = None

    def redraw(self, screen, x, y):
        self.fill((0, 0, 0, 0))

        for i, button in enumerate(self.buttons):
            button.redraw(self, i * self.buttonWidth, 0)

        screen.blit(self, self.get_rect(x=x, y=y))

    def init(self, data):
        self.data = data
        self.buttonWidth = self.get_width()/len(data)
        self.buttons = [Label(self.buttonWidth, 80, i) for i in data]
        self.setSelected(0)

    def getSelected(self):
        return self.selected

    def setSelected(self, index):
        self.selected = index
        for button in self.buttons:
            button.setSelected(False)
        self.buttons[index].setSelected(True)
