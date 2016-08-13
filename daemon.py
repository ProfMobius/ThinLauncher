#!/usr/bin/python2

import json
import os
import subprocess
import sys
import tempfile

BASE_COMMAND = "/usr/bin/xinit /usr/bin/dbus-launch --exit-with-session %s -- :0 -nolisten tcp vt7"

jsondata = json.load(open(os.path.join("assets", "menu.json"), 'rb'))
while True:
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


