import pygame

from gui.DummyDisplay import DummyDisplay
from gui.NetworkDisplay import NetworkDisplay
from pgu import gui
from os.path import expanduser

from Constants import *
from pgu.gui import Theme

MARGIN = 10

class MainArea(pygame.Surface):
    def __init__(self, w, h):
        super(MainArea, self).__init__((w, h), pygame.SRCALPHA)
        self.selected = 0

        # pgu init
        self.pguApp = gui.App(Theme(expanduser("~/.config/thinlauncher/assets/themes/thinlauncher")))
        self.pguContainer = DummyDisplay(LEFT_MENU_WIDTH + MARGIN, TOP_MENU_HEIGHT)
        self.pguApp.init(self.pguContainer)

    def init(self, data):
        if 'mainAreaGUI' in data:
            # TODO : We might want to use a table instead of an eval so we have proper import handling
            self.pguContainer = eval(data['mainAreaGUI'])(LEFT_MENU_WIDTH + MARGIN, TOP_MENU_HEIGHT)
        else:
            self.pguContainer = DummyDisplay(LEFT_MENU_WIDTH + MARGIN, TOP_MENU_HEIGHT)

        self.pguApp.init(self.pguContainer)

    def redraw(self, screen, x, y):
        self.fill((150, 150, 255, 100))
        screen.blit(self, self.get_rect(x=x, y=y))
        self.redrawGUI()

    def redrawGUI(self):
        self.pguApp.paint()
