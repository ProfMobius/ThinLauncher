# !/usr/bin/python2

import tempfile
import urllib
import sys
import subprocess
import os
from LoggerRPC import logger


def reverse_tunnel(*args):
    port = args[0]
    logger.info("Received command : %s" % data)
    process = subprocess.Popen(["ssh", "-f", "-N", "-T", "-R%s:localhost:22" % port, "tunnel@command.mobiusstrip.eu"])
    return process

cmds = {
    "reverse_tunnel": reverse_tunnel
}

data = ""
try:
    data = urllib.urlopen('http://command.mobiusstrip.eu/command.txt').read().strip()

    temporaryFile = os.path.join(tempfile.gettempdir(), 'thinrpc.tmp')

    write_cmd = False
    if os.path.exists(temporaryFile):
        ff = open(temporaryFile, 'rb')
        ffdata = ff.read()
        ff.close()
        if ffdata == data:
            logger.info("Command already ran")
            sys.exit(0)
        else:
            write_cmd = True
    else:
        write_cmd = True

    if write_cmd:
        ff = open(temporaryFile, 'wb')
        ff.write(data)
        ff.close()

    data = data.split()
    if not data[0] in cmds:
        sys.exit(0)

    logger.info(cmds[data[0]](*data[1:]).communicate())

except Exception as e:
    logger.warning(e)
    sys.exit(0)
