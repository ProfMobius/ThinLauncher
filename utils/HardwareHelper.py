import subprocess

def getInterfaces():
    return [i.strip().split(' ')[1][:-1] for i in subprocess.check_output(["ip", "link"]).splitlines() if not i.strip().startswith("link")]

