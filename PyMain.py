import json
import os
import shutil
import sys
import tempfile

import pygame
from pygame.locals import *

from Label import Label
from Logger import logger
from surfaces.LeftMenu import LeftMenu
from surfaces.MainArea import MainArea
from surfaces.StatusBar import StatusBar
from surfaces.TopMenu import TopMenu

if not pygame.font:
    print 'Warning, fonts disabled'
if not pygame.mixer:
    print 'Warning, sound disabled'

#Change to 0,0 on release !
SCREEN_RES_X = 1440
SCREEN_RES_Y = 900
TOP_MENU_HEIGHT = 80
STATUS_BAR_HEIGHT = 40
LEFT_MENU_WIDTH = 500
LEFT_MENU_BUTTON_HEIGHT = 120

class PyMain(object):
    def __init__(self):
        pygame.init()
        self.initSurfaces()
        self.initJoysticks()

        self.temporaryFile = os.path.join(tempfile.gettempdir(), 'thinlauncher.tmp')
        self.jsondata = json.load(open(self.findConfig(), 'rb'))

        self.backgroundColor = eval(self.jsondata['backgroundColor'])
        if 'backgroundImage' in self.jsondata:
            self.backgroundImage = self.load_image('bgimage', self.jsondata['backgroundImage'])
            self.backgroundImage = pygame.transform.smoothscale(self.backgroundImage, (self.screen.get_width(), self.screen.get_height()))
        else:
            self.backgroundImage = None

        self.menus = self.jsondata['menus']
        self.menuWidth = (self.screen.get_width() - len(self.menus)) / len(self.menus)
        self.menuHeight = TOP_MENU_HEIGHT
        self.menuLabels = [
            Label(self.menuWidth, self.menuHeight, eval(i['colorUnselected']), eval(i['fontColorUnselected']), eval(i['colorSelected']), eval(i['fontColorSelected']), i['name'])
            for i in self.menus
        ]
        logger.debug("Top menu button size : %dx%d" % (self.menuLabels[0].get_width(), self.menuLabels[0].get_height()))

        self.entries = []
        self.entryWidth = LEFT_MENU_WIDTH
        self.entryHeight = 120
        self.entryLabels = []
        logger.debug("Left menu button size : %dx%d" % (self.entryWidth, self.entryHeight))

        self.currentMenu = 0
        self.currentEntry = 0

        self.leftMenu = pygame.Surface((self.entryWidth, self.screen.get_height() - self.menuHeight - 1), SRCALPHA)
        self.leftMenu.fill(eval(self.jsondata['leftMenuColor']))

        self.setSelectedMenu(self.currentMenu)

        logger.info("Using driver : " + pygame.display.get_driver())

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

        # self.screen.blit(self.leftMenu, self.leftMenu.get_rect(y=self.menuHeight + 1))
        #
        # for i, label in enumerate(self.menuLabels):
        #     label.redraw()
        #     self.screen.blit(label, label.get_rect(x=i * self.menuWidth + i))
        #
        # for i, label in enumerate(self.entryLabels):
        #     label.redraw()
        #     self.screen.blit(label, label.get_rect(y=i * self.entryHeight + 1 + i + self.menuHeight))

        pygame.display.flip()

    def getScreen(self):
        return self.screen

    def setSelectedMenu(self, menuIndex):
        self.currentMenu = menuIndex

        [i.setSelected(False) for i in self.menuLabels]
        self.menuLabels[menuIndex].setSelected(True)
        self.entries = self.menus[menuIndex]['entries']

        self.entryLabels = [
            Label(self.entryWidth, self.entryHeight, eval(i['colorUnselected']), eval(i['fontColorUnselected']), eval(i['colorSelected']), eval(i['fontColorSelected']), i['name'])
            for i in self.entries
        ]
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
                # if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) \
                # or (event.type == pygame.JOYBUTTONDOWN and event.button == 1):
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) \
                or (event.type == pygame.QUIT):
                    if os.path.exists(self.temporaryFile):
                        os.remove(self.temporaryFile)
                    sys.exit(0)

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT) \
                or (event.type == pygame.JOYBUTTONDOWN and event.button == 11):
                    self.setSelectedMenu((self.currentMenu - 1) % len(self.menus))

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT) \
                or (event.type == pygame.JOYBUTTONDOWN and event.button == 12):
                    self.setSelectedMenu((self.currentMenu + 1) % len(self.menus))

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_UP) \
                or (event.type == pygame.JOYBUTTONDOWN and event.button == 13):
                    self.setSelectedEntry((self.currentEntry - 1) % len(self.entries))

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN) \
                or (event.type == pygame.JOYBUTTONDOWN and event.button == 14):
                    self.setSelectedEntry((self.currentEntry + 1) % len(self.entries))

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) \
                or (event.type == pygame.JOYBUTTONDOWN and event.button == 0):
                    entry = self.menus[self.currentMenu]['entries'][self.currentEntry]
                    ff = open(self.temporaryFile, 'wb')
                    ff.write(entry['command'])
                    ff.close()
                    print "Launching %s with command %d" % (entry['name'], entry['command'])
                    sys.exit(0)

    def load_image(self, key, filename, colorkey=None):
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
