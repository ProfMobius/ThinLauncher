import netifaces
import subprocess


def getInterfaces():
    # Neat method but we might not use it at all since netifaces is returning basically the same thing
    return [i.strip().split(' ')[1][:-1] for i in subprocess.check_output(["ip", "link"]).splitlines() if not i.strip().startswith("link")]


def getWifiInterfaces():
    interfaces = []

    for interface in netifaces.interfaces():
        if subprocess.call(["iw", interface, "info"]) != 237:
            interfaces.append(interface)

    return interfaces


def getLineInterfaces():
    interfaces = []

    for interface in netifaces.interfaces():
        if subprocess.call(["iw", interface, "info"]) == 237:
            interfaces.append(interface)

    return interfaces
