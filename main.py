#!/usr/bin/python2

import os, sys

import pygame

from PyMain import PyMain
from Label import Label


def main():
    pyMain = PyMain(1280, 720, "menu.json")
    pyMain.loop()


if __name__ == "__main__":
    main()
