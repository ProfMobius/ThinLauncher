#!/usr/bin/python2

import os
import subprocess
import sys
import tempfile
from Logger import logger

BASE_COMMAND = "/usr/bin/xinit /usr/bin/dbus-launch --exit-with-session %s -- :0 -nolisten tcp vt7"

try:
    logger.debug("Starting ThinLauncher Daemon")

    while True:
        logger.debug("Launching ThinLauncher GUI")
        returnCode = subprocess.call(BASE_COMMAND%"/home/kodi/ThinLauncher/main.py", shell=True)

        if returnCode != 0:
            sys.exit(returnCode)

        temporaryFile = os.path.join(tempfile.gettempdir(), 'thinlauncher.tmp')
        if os.path.exists(temporaryFile):
            ff = open(temporaryFile, 'rb')
            command = ff.read()
            ff.close()
            subprocess.call(BASE_COMMAND % command, shell=True)
            os.remove(temporaryFile)
        else:
            sys.exit(0)
except Exception as e:
    logger.error(str(e))

