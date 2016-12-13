#!/usr/bin/python2
import sys

from Logger import logger
from PyMain import PyMain

try:
    def main(configFile):
        pyMain = PyMain(configFile)
        pyMain.loop()


    if __name__ == "__main__":
        if len(sys.argv) > 1:
            main(sys.argv[1])
        else:
            main(None)

except Exception as e:
    logger.error(str(e))
