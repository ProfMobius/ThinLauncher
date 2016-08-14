import pygame

from utils import FileSystemHelper

assets = {}


def load_image(filename, colorkey=None):
    fullname = FileSystemHelper.findAsset(filename)

    if fullname in assets:
        return assets[fullname]

    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', filename
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    assets[fullname] = image
    return image


def get_font(name, size):
    if name is None:
        return None

    fontName = FileSystemHelper.findAsset(name)
    key = '%s_%s'%(fontName, size)

    if key in assets:
        return assets[key]

    font = pygame.font.Font(fontName, size)
    assets[key] = font
    return font
