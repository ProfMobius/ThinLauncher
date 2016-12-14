from pgu import gui


class DummyDisplay(gui.Container):
    def __init__(self, x, y):
        super(DummyDisplay, self).__init__(align=-1, valign=-1)