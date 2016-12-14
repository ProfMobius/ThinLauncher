from pgu import gui
import netifaces


class NetworkDisplay(gui.Container):
    def __init__(self, x, y):
        super(NetworkDisplay, self).__init__(align=-1, valign=-1)
        self.add(self.createTable(), x, y)

    def createTable(self):

        gateways = netifaces.gateways()
        interfaces = []
        if netifaces.AF_INET in gateways:
            interfaces = [(j, netifaces.ifaddresses(j)[netifaces.AF_INET]) for j in [i[1] for i in gateways[netifaces.AF_INET]]]

        print interfaces

        pguTable = gui.Table()
        if netifaces.AF_INET in gateways:
            for gateway in gateways[netifaces.AF_INET]:
                pguTable.tr()
                pguTable.td(gui.Label(value="Gateway"), align=-1)
                pguTable.td(gui.Label(value="  "), align=-1)
                pguTable.td(gui.Label(value=gateway[0]), align=-1)

        for interface in interfaces:
            pguTable.tr()
            pguTable.td(gui.Label(value=interface[0]), align=-1)
            for addr in interface[1]:
                pguTable.td(gui.Label(value="  "), align=-1)
                pguTable.td(gui.Label(value=addr['addr']), align=-1)

        return pguTable
