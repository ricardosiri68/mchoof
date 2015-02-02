import sys
from mchoof.core.application import HoofApp
from main_app import views, settings


if __name__ == '__main__':
    app = HoofApp(sys.argv)
    app.initSettings(settings)
    mainWindow = views.MainWindow(main_app=app)
    mainWindow.show()
    app.exec_()
