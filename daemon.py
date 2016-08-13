import json
import os
import subprocess
import sys

BASE_COMMAND = "/usr/bin/xinit /usr/bin/dbus-launch --exit-with-session %s -- :0 -nolisten tcp vt7"

jsondata = json.load(open(os.path.join("assets", "menu.json"), 'rb'))
while True:
    returnCode = subprocess.call("python2 main.py", shell=True)
    if returnCode == 0:
        sys.exit(0)

    for menu in jsondata['menus']:
        for entry in menu['entries']:
            if entry['return'] == returnCode and 'command' in entry:
                subprocess.call(BASE_COMMAND%entry['command'], shell=True)

