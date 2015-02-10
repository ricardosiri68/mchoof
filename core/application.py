from .db_session import get_session
from PySide.QtGui import QApplication


class HoofApp(QApplication):

    def initSettings(self, settings_module):
        '''
        inizializa las variables de configuracion como atributos del la app
        '''
        if hasattr(settings_module, 'DATABASE_URL'):
            self.session = get_session(settings_module.DATABASE_URL)
