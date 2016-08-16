import pygame
from Constants import *
from Label import Label


class LeftMenu(pygame.Surface):
    def __init__(self, h, w):
        super(LeftMenu, self).__init__((h, w), pygame.SRCALPHA)
        self.selected = 0
        self.buttons = []
        self.data = None

    def redraw(self, screen, x, y):
        self.fill((100, 100, 100, 50))

        for i in range(len(self.buttons) -1, -1, -1):
            if i != self.selected:
                self.buttons[i].redraw(self, i * 0, i * (LEFT_MENU_BUTTON_HEIGHT - 10))
        self.buttons[self.selected].redraw(self, self.selected * 0, self.selected * (LEFT_MENU_BUTTON_HEIGHT - 10))

        screen.blit(self, self.get_rect(x=x, y=y))

    def init(self, data):
        self.data = data
        self.buttons = []
        self.buttons = [Label(LEFT_MENU_WIDTH, LEFT_MENU_BUTTON_HEIGHT, i, align=ALIGN_LEFT, logo=True) for i in data]
        self.setSelected(0)

    def getSelected(self):
        return self.selected

    def setSelected(self, index):
        self.selected = index
        for button in self.buttons:
            button.setSelected(False)
        self.buttons[index].setSelected(True)
