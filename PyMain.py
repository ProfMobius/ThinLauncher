import json
import os
import re
import shutil
import sys
import tempfile

import pygame
import subprocess

from pgu import gui
from pygame.locals import *

from Constants import *
from Logger import logger
from pgu.gui import Theme
from surfaces.LeftMenu import LeftMenu
from surfaces.MainArea import MainArea
from surfaces.StatusBar import StatusBar
from surfaces.TopMenu import TopMenu
from utils import AssetManager
from utils import FileSystemHelper

if not pygame.font:
    print 'Warning, fonts disabled'
if not pygame.mixer:
    print 'Warning, sound disabled'

BASE_COMMAND = "/usr/bin/xinit /usr/bin/dbus-launch --exit-with-session %s -- :0 -nolisten tcp vt7"


class PyMain(object):
    def __init__(self, configFile):
        pygame.init()
        logger.info("Using driver : " + pygame.display.get_driver())

        #self.disableMouse()
        self.initSurfaces()
        self.initJoysticks()

        self.temporaryFile = os.path.join(tempfile.gettempdir(), 'thinlauncher.tmp')
        self.jsondata = json.load(open(FileSystemHelper.findConfig(configFile), 'rb'))

        self.backgroundColor = eval(self.jsondata['backgroundColor'])
        if 'backgroundImage' in self.jsondata:
            self.backgroundImage = AssetManager.load_image(self.jsondata['backgroundImage'])
            self.backgroundImage = pygame.transform.smoothscale(self.backgroundImage, (self.screen.get_width(), self.screen.get_height()))
        else:
            self.backgroundImage = None

        self.topMenuSurface.init(self.jsondata['menus'])
        self.setTopSelected(0)
        self.setLeftSelected(0)

        self.redraw()

    def disableMouse(self):
        devices = subprocess.check_output(["xinput"]).splitlines()
        for line in devices:
            logger.debug(line)
            if re.search("(master|slave)\s*pointer", line):
                deviceID = re.findall("id=([0-9]+)", line)[0]
                logger.info("Trying to disable device %s" % deviceID)
                subprocess.call(["xinput", "disable", deviceID])

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

    def redraw(self, full=True):
        # TODO : The whole concept of only partially redrawing is bad.
        # TODO : Should try to figure out why redrawing is so expensive

        if full:
            self.screen.fill(self.backgroundColor)

            if self.backgroundImage:
                self.screen.blit(self.backgroundImage, self.backgroundImage.get_rect())

            self.topMenuSurface.redraw(self.screen, 0, 0)
            self.leftMenuSurface.redraw(self.screen, 0, TOP_MENU_HEIGHT)
            self.statusBarSurface.redraw(self.screen, 0, TOP_MENU_HEIGHT + self.leftMenuSurface.get_height())
            self.mainAreaSurface.redraw(self.screen, LEFT_MENU_WIDTH, TOP_MENU_HEIGHT)
        else:
            self.mainAreaSurface.redrawGUI()

        pygame.display.flip()

    def setTopSelected(self, index):
        self.topMenuSurface.setSelected(index)
        self.leftMenuSurface.init(self.jsondata['menus'][index]['entries'])
        self.setLeftSelected(0)

    def setLeftSelected(self, index):
        self.leftMenuSurface.setSelected(index)
        self.mainAreaSurface.init(self.leftMenuSurface.data[index])

    def writeCommand(self, entry, command):
        ff = open(self.temporaryFile, 'wb')
        ff.write(command)
        ff.close()
        logger.info("Launching %s with command %s" % (entry['name'], command))

    def loop(self):
        while 1:
            # event = pygame.event.wait()

            fullRedraw = False
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
                    fullRedraw = True

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT) \
                        or (event.type == pygame.JOYBUTTONDOWN and event.button == 12):
                    topMenuIndex = (self.topMenuSurface.getSelected() + 1) % len(self.topMenuSurface.buttons)
                    self.setTopSelected(topMenuIndex)
                    fullRedraw = True

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_UP) \
                        or (event.type == pygame.JOYBUTTONDOWN and event.button == 13):
                    leftMenuIndex = (self.leftMenuSurface.getSelected() - 1) % len(self.leftMenuSurface.buttons)
                    self.setLeftSelected(leftMenuIndex)
                    fullRedraw = True

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN) \
                        or (event.type == pygame.JOYBUTTONDOWN and event.button == 14):
                    leftMenuIndex = (self.leftMenuSurface.getSelected() + 1) % len(self.leftMenuSurface.buttons)
                    self.setLeftSelected(leftMenuIndex)
                    fullRedraw = True

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) \
                        or (event.type == pygame.JOYBUTTONDOWN and event.button == 0):
                    entry = self.leftMenuSurface.data[self.leftMenuSurface.getSelected()]

                    # We run a command if there is one
                    if 'command' in entry:
                        command = entry['command']
                        if command[0] == '#':
                            self.writeCommand(entry, command[1:])
                            sys.exit(0)
                        elif command[0] == '$':
                            subprocess.call(command[1:], shell=True)
                        else:
                            self.writeCommand(entry, BASE_COMMAND % command)
                            sys.exit(0)

                    # If we have a main area GUI, we should activate it and start working on it
                    if 'mainAreaGUI' in entry:
                        pass

                else:
                    self.mainAreaSurface.pguApp.event(event)

            self.redraw(full=fullRedraw)
