import pygame

from gui.DummyDisplay import DummyDisplay
from gui.NetworkDisplay import NetworkDisplay
from pgu import gui

from Constants import *
from pgu.gui import Theme


class MainArea(pygame.Surface):
    def __init__(self, w, h):
        super(MainArea, self).__init__((w, h), pygame.SRCALPHA)
        self.selected = 0

        # pgu init
        self.pguApp = gui.App(Theme("./assets/themes/thinlauncher"))
        self.pguContainer = DummyDisplay(LEFT_MENU_WIDTH, TOP_MENU_HEIGHT)
        self.pguApp.init(self.pguContainer)

    def init(self, data):
        if 'mainAreaGUI' in data:
            self.pguContainer = eval(data['mainAreaGUI'])(LEFT_MENU_WIDTH, TOP_MENU_HEIGHT)
        else:
            self.pguContainer = DummyDisplay(LEFT_MENU_WIDTH, TOP_MENU_HEIGHT)

        self.pguApp.init(self.pguContainer)

    def redraw(self, screen, x, y):
        self.fill((150, 150, 255, 100))
        screen.blit(self, self.get_rect(x=x, y=y))
        self.redrawGUI()

    def redrawGUI(self):
        self.pguApp.paint()
