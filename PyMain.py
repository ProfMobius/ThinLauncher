import os, sys
import json
import tempfile

import pygame
import sys
from pygame.locals import *

from Label import Label

if not pygame.font:
    print 'Warning, fonts disabled'
if not pygame.mixer:
    print 'Warning, sound disabled'


class PyMain(object):
    def __init__(self, jsonfilename):
        pygame.init()
        self.screen = pygame.display.set_mode()
        # self.__background = pygame.Surface(self.__screen.get_size()).convert()
        # self.__foreground = pygame.Surface(self.__screen.get_size()).convert()

        self.jsondata = json.load(open(os.path.join("assets", jsonfilename), 'rb'))

        self.backgroundColor = eval(self.jsondata['backgroundColor'])
        if 'backgroundImage' in self.jsondata:
            self.backgroundImage = self.load_image('bgimage', self.jsondata['backgroundImage'])
            self.backgroundImage = pygame.transform.smoothscale(self.backgroundImage, (self.screen.get_width(), self.screen.get_height()))
        else:
            self.backgroundImage = None

        self.menus = self.jsondata['menus']
        self.menuWidth = (self.screen.get_width() - len(self.menus)) / len(self.menus)
        self.menuHeight = 40
        self.menuLabels = [
            Label(self.menuWidth, self.menuHeight, eval(i['colorUnselected']), eval(i['fontColorUnselected']),
                  eval(i['colorSelected']), eval(i['fontColorSelected']),
                  i['name']) for
            i in self.menus]

        self.entries = []
        self.entryWidth = 250
        self.entryHeight = 80
        self.entryLabels = []

        self.currentMenu = 0
        self.currentEntry = 0

        self.setSelectedMenu(self.currentMenu)

        print "Using driver : " + pygame.display.get_driver()

    def redraw(self):
        self.screen.fill(self.backgroundColor)

        if self.backgroundImage:
            self.screen.blit(self.backgroundImage, self.backgroundImage.get_rect())

        for i, label in enumerate(self.menuLabels):
            label.redraw()
            self.screen.blit(label, label.get_rect(x=i * self.menuWidth + i))

        for i, label in enumerate(self.entryLabels):
            label.redraw()
            self.screen.blit(label, label.get_rect(y=i * self.entryHeight + 1 + i + self.menuHeight))

        pygame.display.flip()

    def getScreen(self):
        return self.screen

    def get_asset(self, key):
        return self.assets[key]

    def setSelectedMenu(self, menuIndex):
        self.currentMenu = menuIndex

        [i.setSelected(False) for i in self.menuLabels]
        self.menuLabels[menuIndex].setSelected(True)
        self.entries = self.menus[menuIndex]['entries']

        self.entryLabels = [
            Label(self.entryWidth, self.entryHeight, eval(i['colorUnselected']), eval(i['fontColorUnselected']),
                  eval(i['colorSelected']), eval(i['fontColorSelected']),
                  i['name']) for i in self.entries]
        self.setSelectedEntry(0)

        self.redraw()

    def setSelectedEntry(self, entryIndex):
        self.currentEntry = entryIndex

        [i.setSelected(False) for i in self.entryLabels]
        self.entryLabels[entryIndex].setSelected(True)
        self.redraw()

    def loop(self):
        while 1:
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)
                    elif event.key == pygame.K_LEFT:
                        self.setSelectedMenu((self.currentMenu - 1) % len(self.menus))
                    elif event.key == pygame.K_RIGHT:
                        self.setSelectedMenu((self.currentMenu + 1) % len(self.menus))
                    elif event.key == pygame.K_UP:
                        self.setSelectedEntry((self.currentEntry - 1) % len(self.entries))
                    elif event.key == pygame.K_DOWN:
                        self.setSelectedEntry((self.currentEntry + 1) % len(self.entries))
                    elif event.key == pygame.K_RETURN:
                        entry = self.menus[self.currentMenu]['entries'][self.currentEntry]
                        ff = open(os.path.join(tempfile.gettempdir(), 'thinlauncher.tmp'), 'wb')
                        ff.write(entry['command'])
                        ff.close()
                        print "Launching %s with command %d"%(entry['name'], entry['command'])
                        sys.exit(0)

                if event.type == pygame.QUIT:
                    ff = open(os.path.join(tempfile.gettempdir(), 'thinlauncher.tmp'), 'wb')
                    ff.write("")
                    ff.close()
                    sys.exit(0)

    def load_image(self, key, filename, colorkey=None):
        fullname = os.path.join('assets', filename)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', filename
            raise SystemExit(message)
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image
