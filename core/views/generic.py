import os
from PySide import QtCore, QtGui
from PySide.QtCore import Slot, QMetaObject
from PySide.QtUiTools import QUiLoader
from mchoof.core.config import menubar
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
    return widget


class BaseView(object):

    def __init__(self):

        if not self.template_name:
            raise exceptions.NoTemplateError()

        loadUi(os.path.join('templates', self.template_name), self)


class View(BaseView, QtGui.QFrame):

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        BaseView.__init__(self)


class MainView(BaseView, QtGui.QMainWindow):

    main_widget = None
    menubar_conf = None

    def __init__(self, parent=None, main_app=None):
        QtGui.QMainWindow.__init__(self, parent)
        BaseView.__init__(self)

        self.main_app = main_app

        if not self.main_widget:
            raise exceptions.MainWidgetError()

        self.setCentralWidget(self.main_widget(self))

        if self.menubar_conf:
            menubar.MenuBarParser(self)

    def actionExit(self):
        pass

    def loadPanelView(self, ViewClass):
        return lambda: self.setCentralWidget(ViewClass(self))


class PanelView(BaseView, QtGui.QFrame):

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        BaseView.__init__(self)
