import logging

logger = logging.getLogger("RunLog")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handlerFile = logging.FileHandler("/var/tmp/thinlauncher.log")
handler.setFormatter(logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s'))
handlerFile.setFormatter(logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.addHandler(handlerFile)
