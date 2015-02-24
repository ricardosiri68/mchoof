import os
from PySide.QtCore import SIGNAL
from PySide.QtGui import QMenu
from .parser import ConfParser
from . import exceptions


class ContextMenuParser(ConfParser):

    def __init__(self, parent):

        conf_path = os.path.join(
            parent.__class__.__module__.split('.')[0],
            'conf',
            parent.contextual_menus_conf
        )
        self.parent = parent
        ConfParser.__init__(self, conf_path)
        self.bindContextualMenus(self.rootNode().childNodes)

    def bindContextualMenus(self, childnodes):
        for childnode in childnodes:
            if childnode.nodeName == 'menu':
                self.bindContextualMenu(childnode)

    def bindContextualMenu(self, menu_element):
        name = menu_element.getAttribute('name')
        widgetname = menu_element.getAttribute('widget')

        if not name:
            raise exceptions.MenuNameError(menu_element)

        if not widgetname:
            raise exceptions.MenuWidgetValueError(menu_element)

        try:
            widget = getattr(self.parent, widgetname)

        except AttributeError:
            raise exceptions.ViewAttributeError(
                self.parent,
                widgetname,
                menu_element
            )

        menu = QMenu(widget)
        setattr(self.parent, 'menu%s' % name.capitalize(), menu)

        widget.connect(
            SIGNAL("customContextMenuRequested(QPoint)"),
            self.parent.showContextMenu(menu, widget)
        )
        self.bindChildItems(menu, menu_element.childNodes)

    def bindChildItems(self, menu, childnodes):
        for childnode in childnodes:

            if childnode.nodeName == 'menu':
                self.bindMenu(menu, childnode)

            elif childnode.nodeName == 'action':
                self.bindAction(menu, childnode)

    def bindMenu(self, menu, menu_element):
        name = menu_element.getAttribute('name')
        title = menu_element.getAttribute('title')

        if not name:
            raise exceptions.MenuNameError(menu_element)

        if not title:
            raise exceptions.MenuTitleError(menu_element)

        submenu = menu.addMenu(title)
        setattr(menu, 'menu%s' % name.capitalize(), submenu)
        self.bindChildItems(submenu, menu_element.childNodes)

    def bindAction(self, menu, action_element):
        name = action_element.getAttribute('name')
        target = action_element.getAttribute('target')
        # shortcut = action_element.getAttribute('shortcut')
        title = action_element.getAttribute('title')

        if not name:
            raise exceptions.MenuNameError(action_element)

        if not target:
            raise exceptions.ActionTargetError(action_element)

        if not title:
            raise exceptions.MenuTitleError(action_element)

        if not hasattr(self.parent, target):
            raise exceptions.ViewAttributeError(
                self.parent,
                target,
                action_element
            )

        action = menu.addAction(title)
        setattr(menu, 'action%s' % name, action)
        action.connect(
            SIGNAL('triggered()'),
            getattr(self.parent, target)
        )
