import pygame
from pgu import gui

from Constants import *
from pgu.gui import Theme


class MainArea(pygame.Surface):
    def __init__(self, h, w):
        super(MainArea, self).__init__((h, w), pygame.SRCALPHA)
        self.selected = 0

        # pgu init
        self.pguApp = gui.App(Theme("./assets/themes/thinlauncher"))
        container = gui.Container(align=-1, valign=-1)
        pguTable = gui.Table()
        # pguTable.tr()
        # pguTable.td(gui.Button(value="This is a test"))
        # pguTable.tr()
        # pguTable.td(gui.Button(value="This is a test"))
        pguTable.tr()
        pguTable.td(gui.TextArea(value="This is a test"))
        container.add(pguTable, LEFT_MENU_WIDTH, TOP_MENU_HEIGHT)
        self.pguApp.init(container)

    def redraw(self, screen, x, y):
        self.fill((150, 150, 255, 100))
        screen.blit(self, self.get_rect(x=x, y=y))
