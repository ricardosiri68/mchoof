# -*- coding: utf-8 -*-
import sys
from mchoof.core.application import HoofApp
from main_app import views
import resource_rc


if __name__ == '__main__':
    app = HoofApp(sys.argv)
    app.initSettings()
    mainWindow = views.MainWindow(main_app=app)
    mainWindow.show()
    app.exec_()
