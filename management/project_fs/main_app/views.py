from mchoof.core.views import generic


class MainFrame(generic.View):

    template_name = 'main_app/mainFrame.ui'


class MainWindow(generic.MainView):

    template_name = 'main_app/mainWindow.ui'
    main_widget = MainFrame
