import os, sys
import json
import pygame
import sys
from pygame.locals import *

from Label import Label

if not pygame.font:
    print 'Warning, fonts disabled'
if not pygame.mixer:
    print 'Warning, sound disabled'


class PyMain(object):
    def __init__(self, width, height, jsonfilename):
        pygame.init()
        self.__width = width
        self.__height = height
        self.__assets = {}
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__background = pygame.Surface(self.__screen.get_size()).convert()
        self.__foreground = pygame.Surface(self.__screen.get_size()).convert()

        self.__jsondata = json.load(open(os.path.join("assets", jsonfilename), 'rb'))

        self.__screen.fill(eval(self.__jsondata['BackgroundColor']))

        self.__menus = self.__jsondata['Menus']
        self.__labelWidth = self.__screen.get_width() / len(self.__menus)
        self.__labels = [Label(self.__labelWidth, 40, eval(i['color']), i['name']) for i in self.__menus]
        self.__currentMenu = 0

        self.setSelected(self.__currentMenu)
        print "Using driver : " + pygame.display.get_driver()

    def redraw(self):
        for i, label in enumerate(self.__labels):
            label.redraw()
            self.__screen.blit(label, label.get_rect(x=i * self.__labelWidth))
        pygame.display.flip()

    def getScreen(self):
        return self.__screen

    def getForeground(self):
        return self.__foreground

    def getBackground(self):
        return self.__background

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
        self.__assets[key] = (image, image.get_rect())
        return image, image.get_rect()

    def get_asset(self, key):
        return self.__assets[key]

    def setSelected(self, menuIndex):
        [i.setSelected(False) for i in self.__labels]
        self.__labels[menuIndex].setSelected(True)
        self.redraw()

    def loop(self):
        while 1:
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)
                    elif event.key == pygame.K_LEFT:
                        self.__currentMenu = (self.__currentMenu - 1) % len(self.__menus)
                        self.setSelected(self.__currentMenu)
                    elif event.key == pygame.K_RIGHT:
                        self.__currentMenu = (self.__currentMenu + 1) % len(self.__menus)
                        self.setSelected(self.__currentMenu)
                    elif event.key == pygame.K_UP:
                        pass
                    elif event.key == pygame.K_DOWN:
                        pass
                    elif event.key == pygame.K_RETURN:
                        pass

                if event.type == pygame.QUIT:
                    sys.exit(0)
