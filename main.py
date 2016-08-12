#!/usr/bin/python2

import os, sys

import pygame

from PyMain import PyMain
from Label import Label


def main():
    pyMain = PyMain(1280, 720, "menu.json")

    # label = Label(250, 40, (255, 0, 0), "Test")
    # pyMain.getScreen().blit(label, label.get_rect())

    pyMain.load_image("cursor", "mouse_cursor.png")
    pyMain.loop()


if __name__ == "__main__":
    main()
