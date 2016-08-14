#!/usr/bin/python2

import os, sys

import pygame

from PyMain import PyMain
from Label import Label
from Logger import logger

try:
    def main():
        pyMain = PyMain()
        pyMain.loop()


    if __name__ == "__main__":
        main()
except Exception as e:
    logger.error(str(e))