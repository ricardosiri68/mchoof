import os
from .db_session import get_session
from PySide.QtGui import QApplication


class HoofApp(QApplication):

    def initSettings(self, settings_module):
        '''
        inizializa las variables de configuracion como atributos del la app
        '''
        os.environ.setdefault('MCHOOF_SETTINGS', settings_module)
