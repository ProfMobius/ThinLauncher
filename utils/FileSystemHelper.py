import os
import shutil

import sys

import pygame

from Logger import logger


def findAsset(name):
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


def findConfig():
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
