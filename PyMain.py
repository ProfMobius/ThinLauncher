import json
import os
import shutil
import sys
import tempfile

import pygame
from pygame.locals import *

from Logger import logger
from surfaces.LeftMenu import LeftMenu
from surfaces.MainArea import MainArea
from surfaces.StatusBar import StatusBar
from surfaces.TopMenu import TopMenu

if not pygame.font:
    print 'Warning, fonts disabled'
if not pygame.mixer:
    print 'Warning, sound disabled'

# Change to 0,0 on release !
SCREEN_RES_X = 1440
SCREEN_RES_Y = 900
TOP_MENU_HEIGHT = 80
STATUS_BAR_HEIGHT = 40
LEFT_MENU_WIDTH = 500
LEFT_MENU_BUTTON_HEIGHT = 120


class PyMain(object):
    def __init__(self):
        pygame.init()
        logger.info("Using driver : " + pygame.display.get_driver())

        self.initSurfaces()
        self.initJoysticks()

        self.temporaryFile = os.path.join(tempfile.gettempdir(), 'thinlauncher.tmp')
        self.jsondata = json.load(open(self.findConfig(), 'rb'))

        self.backgroundColor = eval(self.jsondata['backgroundColor'])
        if 'backgroundImage' in self.jsondata:
            self.backgroundImage = self.load_image(self.jsondata['backgroundImage'])
            self.backgroundImage = pygame.transform.smoothscale(self.backgroundImage, (self.screen.get_width(), self.screen.get_height()))
        else:
            self.backgroundImage = None

        self.topMenuSurface.init(self.jsondata['menus'])
        self.setTopSelected(0)

        self.redraw()

    def initSurfaces(self):
        self.screen = pygame.display.set_mode((SCREEN_RES_X, SCREEN_RES_Y), SRCALPHA)
        screenWidth = self.screen.get_width()
        screenHeight = self.screen.get_height()

        self.topMenuSurface = TopMenu(screenWidth, TOP_MENU_HEIGHT)
        self.leftMenuSurface = LeftMenu(LEFT_MENU_WIDTH, screenHeight - TOP_MENU_HEIGHT - STATUS_BAR_HEIGHT)
        self.statusBarSurface = StatusBar(screenWidth, STATUS_BAR_HEIGHT)
        self.mainAreaSurface = MainArea(screenWidth - LEFT_MENU_WIDTH, screenHeight - TOP_MENU_HEIGHT - STATUS_BAR_HEIGHT)

        logger.info("Screen created with resolution of %dx%d" % (screenWidth, screenHeight))
        logger.info("TopMenu created with resolution of %dx%d" % (self.topMenuSurface.get_width(), self.topMenuSurface.get_height()))
        logger.info("LeftMenu created with resolution of %dx%d" % (self.leftMenuSurface.get_width(), self.leftMenuSurface.get_height()))
        logger.info("StatusBar created with resolution of %dx%d" % (self.statusBarSurface.get_width(), self.statusBarSurface.get_height()))
        logger.info("MainArea created with resolution of %dx%d" % (self.mainAreaSurface.get_width(), self.mainAreaSurface.get_height()))

    def initJoysticks(self):
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            logger.info("Found joystick %s" % (joystick.get_name(),))

    def redraw(self):
        self.screen.fill(self.backgroundColor)

        if self.backgroundImage:
            self.screen.blit(self.backgroundImage, self.backgroundImage.get_rect())

        self.topMenuSurface.redraw(self.screen, 0, 0)
        self.leftMenuSurface.redraw(self.screen, 0, TOP_MENU_HEIGHT)
        self.statusBarSurface.redraw(self.screen, 0, TOP_MENU_HEIGHT + self.leftMenuSurface.get_height())
        self.mainAreaSurface.redraw(self.screen, LEFT_MENU_WIDTH, TOP_MENU_HEIGHT)

        pygame.display.flip()

    def setTopSelected(self, index):
        self.topMenuSurface.setSelected(index)
        self.leftMenuSurface.init(self.jsondata['menus'][index]['entries'])

    def loop(self):
        while 1:
            for event in pygame.event.get():
                # if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) \
                # or (event.type == pygame.JOYBUTTONDOWN and event.button == 1):
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) \
                or (event.type == pygame.QUIT):
                    if os.path.exists(self.temporaryFile):
                        os.remove(self.temporaryFile)
                    sys.exit(0)

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT) \
                or (event.type == pygame.JOYBUTTONDOWN and event.button == 11):
                    topMenuIndex = (self.topMenuSurface.getSelected() - 1) % len(self.topMenuSurface.buttons)
                    self.setTopSelected(topMenuIndex)

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT) \
                or (event.type == pygame.JOYBUTTONDOWN and event.button == 12):
                    topMenuIndex = (self.topMenuSurface.getSelected() + 1) % len(self.topMenuSurface.buttons)
                    self.setTopSelected(topMenuIndex)

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_UP) \
                or (event.type == pygame.JOYBUTTONDOWN and event.button == 13):
                    self.leftMenuSurface.setSelected((self.leftMenuSurface.getSelected() - 1) % len(self.leftMenuSurface.buttons))

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN) \
                or (event.type == pygame.JOYBUTTONDOWN and event.button == 14):
                    self.leftMenuSurface.setSelected((self.leftMenuSurface.getSelected() + 1) % len(self.leftMenuSurface.buttons))

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) \
                or (event.type == pygame.JOYBUTTONDOWN and event.button == 0):
                    entry = self.leftMenuSurface.data[self.leftMenuSurface.getSelected()]
                    ff = open(self.temporaryFile, 'wb')
                    ff.write(entry['command'])
                    ff.close()
                    logger.info("Launching %s with command %s" % (entry['name'], entry['command']))
                    sys.exit(0)

                self.redraw()

    def load_image(self, filename, colorkey=None):
        fullname = self.findAsset(filename)
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

    def findAsset(self, name):
        pathUsrShare = "/usr/share/thinlauncher/assets"
        pathHome = os.path.join(os.path.expanduser("~"), ".config/thinlauncher/assets")
        pathDev = "./assets"

        if not os.path.exists(pathHome):
            os.makedirs(pathHome)

        if os.path.exists(os.path.join(pathHome, name)):
            return os.path.join(pathHome, name)

        if os.path.exists(os.path.join(pathUsrShare, name)):
            return os.path.join(pathUsrShare, name)

        if os.path.exists(os.path.join(pathDev, name)):
            return os.path.join(pathDev, name)

    def findConfig(self):
        configName = "thinlauncher.cfg"
        pathUsrShare = "/usr/share/thinlauncher/"
        pathHome = os.path.join(os.path.expanduser("~"), ".config/thinlauncher/")
        pathDev = "./"

        if not os.path.exists(pathHome):
            os.makedirs(pathHome)

        if os.path.exists(os.path.join(pathHome, configName)):
            return os.path.join(pathHome, configName)

        if os.path.exists(os.path.join(pathUsrShare, configName)):
            shutil.copy(pathUsrShare + configName, pathHome + configName)
            return os.path.join(pathHome, configName)

        if os.path.exists(os.path.join(pathDev, configName)):
            return os.path.join(pathDev, configName)

        logger.error("Can't find a valid config file !")
        sys.exit(1)
