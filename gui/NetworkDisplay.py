from pgu import gui


class NetworkDisplay(gui.Container):
    def __init__(self, x, y):
        super(NetworkDisplay, self).__init__(align=-1, valign=-1)

        pguTable = gui.Table()
        pguTable.tr()
        pguTable.td(gui.TextArea(value="This is a test"))
        pguTable.td(gui.TextArea(value="This is another test"))
        self.add(pguTable, x, y)
