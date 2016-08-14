#!/usr/bin/python2

from Logger import logger
from PyMain import PyMain

try:
    def main():
        pyMain = PyMain()
        pyMain.loop()


    if __name__ == "__main__":
        main()
except Exception as e:
    logger.error(str(e))
