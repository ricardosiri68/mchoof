import os
from PySide import QtGui
from PySide.QtCore import QMetaObject
from PySide.QtUiTools import QUiLoader
from mchoof.config import menubar, model_binding, contextual_menu,\
    view_signals, stylesheet
from . import exceptions


class UiLoader(QUiLoader):
    """
    Subclass :class:`~PySide.QtUiTools.QUiLoader` to create the user interface
    in a base instance.
    Unlike :class:`~PySide.QtUiTools.QUiLoader` itself this class does not
    create a new instance of the top-level widget, but creates the user
    interface in an existing instance of the top-level class.
    This mimics the behaviour of :func:`PyQt4.uic.loadUi`.
    """

    def __init__(self, baseinstance):
        """
        Create a loader for the given ``baseinstance``.
        The user interface is created in ``baseinstance``, which must be an
        instance of the top-level class in the user interface to load, or a
        subclass thereof.
        ``parent`` is the parent object of this loader.
        """
        QUiLoader.__init__(self, baseinstance)
        self.baseinstance = baseinstance

    def createWidget(self, class_name, parent=None, name=''):
        if parent is None and self.baseinstance:
            # supposed to create the top-level widget, return the base instance
            # instead
            return self.baseinstance
        else:
            # create a new widget for child widgets
            widget = QUiLoader.createWidget(self, class_name, parent, name)
            if self.baseinstance:
                # set an attribute for the new child widget on the base
                # instance, just like PyQt4.uic.loadUi does.
                setattr(self.baseinstance, name, widget)
            return widget


def loadUi(uifile, baseinstance=None):
    """
    Dynamically load a user interface from the given ``uifile``.
    ``uifile`` is a string containing a file name of the UI file to load.
    If ``baseinstance`` is ``None``, the a new instance of the top-level widget
    will be created.  Otherwise, the user interface is created within the given
    ``baseinstance``.  In this case ``baseinstance`` must be an instance of the
    top-level widget class in the UI file to load, or a subclass thereof.  In
    other words, if you've created a ``QMainWindow`` interface in the designer,
    ``baseinstance`` must be a ``QMainWindow`` or a subclass thereof, too.  You
    cannot load a ``QMainWindow`` UI file with a plain
    :class:`~PySide.QtGui.QWidget` as ``baseinstance``.
    :method:`~PySide.QtCore.QMetaObject.connectSlotsByName()` is called on the
    created user interface, so you can implemented your slots according to its
    conventions in your widget class.
    Return ``baseinstance``, if ``baseinstance`` is not ``None``.  Otherwise
    return the newly created instance of the user interface.
    """
    loader = UiLoader(baseinstance)
    widget = loader.load(uifile)
    QMetaObject.connectSlotsByName(widget)


def modal_wrapper(modal=None):

    def modal_decorator(func):

        def modal_wrapper(parent):

            modalinstance = modal(parent)
            result = modalinstance.exec_()
            func(parent, result)

        return modal_wrapper

    return modal_decorator


class BaseView(object):

    models_binding_conf = None
    contextual_menus_conf = None
    signals_conf = None

    def __init__(self):

        if not self.template_name:
            raise exceptions.NoTemplateError()

        loadUi(os.path.join('templates', self.template_name), self)

        if self.models_binding_conf:
            model_binding.ModelBindingParser(self)

        if self.contextual_menus_conf:
            contextual_menu.ContextMenuParser(self)

        if self.signals_conf:
            view_signals.SignalConfParser(self)

    def showContextMenu(self, menu, widget):

        return lambda point: menu.exec_(widget.mapToGlobal(point))


class View(BaseView, QtGui.QWidget):

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        BaseView.__init__(self)


class MainView(BaseView, QtGui.QMainWindow):

    toolbar_widget = None
    main_widget = None
    menubar_conf = None
    stylesheet_path = None

    def __init__(self, parent=None, main_app=None):
        QtGui.QMainWindow.__init__(self, parent)
        BaseView.__init__(self)

        self.main_app = main_app

        if not self.main_widget:
            raise exceptions.MainWidgetError()

        self.setCentralWidget(self.main_widget(self))

        if self.menubar_conf:
            menubar.MenuBarParser(self)

        if self.stylesheet_path:
            stylesheet.LoadStyleSheet(self)

        if self.toolbar_widget and hasattr(self, 'toolBar'):
            self.toolbar_view = self.toolbar_widget(self)
            self.toolBar.addWidget(self.toolbar_view)

    def actionExit(self):
        pass

    def loadPanelView(self, ViewClass):

        return lambda: self.setCentralWidget(ViewClass(self))


class ModalView(BaseView, QtGui.QDialog):

    modal = True

    def __init__(self, parent):

        QtGui.QDialog.__init__(self, parent)
        BaseView.__init__(self)

        parent.setEnabled(False)
        self.setEnabled(True)

        parent = self.parent()

        self.centerModal(
            parent.geometry().center().x(),
            parent.geometry().center().y()
        )

    def centerModal(self, x, y):
        self.move(
            x - (self.geometry().center().x()),
            y - (self.geometry().center().y())
        )

    def done(self, success):

        self.parent().setEnabled(True)

        super(ModalView, self).done(success)


class PanelView(View):

    def __init__(self, parent=None):

        View.__init__(self, parent)
