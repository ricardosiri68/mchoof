import os
from . import exceptions


class LoadStyleSheet:

    def __init__(self, parent):
        self.conf_path = os.path.join(
            'resources',
            parent.stylesheet_path
        )
        self.parent = parent
        self.loadStyleSheet()

    def loadStyleSheet(self):
        stylesheet = open(self.conf_path)
        self.parent.setStyleSheet(stylesheet.read())
        stylesheet.close()
