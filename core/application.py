import os
from PySide.QtGui import QApplication


class HoofApp(QApplication):

    def initSettings(self):
        '''
        inizializa las variables de configuracion como atributos del la app
        '''
        os.environ.setdefault('MCHOOF_SETTINGS', 'main_app.settings')
