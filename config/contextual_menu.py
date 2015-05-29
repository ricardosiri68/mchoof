import os
from PySide.QtCore import SIGNAL, Qt
from PySide.QtGui import QMenu, QShortcut, QKeySequence, QIcon, QPixmap
from .parser import ConfParser
from .exceptions.view_exceptions import (
    ViewAttributeError,
    ViewTargetNotCallableError
)
from .exceptions.menu_exceptions import (
    MenuNameError,
    MenuWidgetValueError,
    MenuTitleError,
    ActionTargetError,
    MenuShortcutError,
    MenuShortcutKeysecuenceError
)


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
        onshow = menu_element.getAttribute('onshow')

        if not name:
            raise MenuNameError(menu_element)

        if not widgetname:
            raise MenuWidgetValueError(menu_element)

        try:
            widget = getattr(self.parent, widgetname)

        except AttributeError:
            raise ViewAttributeError(
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

        if onshow:
            if hasattr(self.parent, onshow):
                onshow_method = getattr(self.parent, onshow)

                if callable(onshow_method):

                    menu.aboutToShow.connect(onshow_method)

                else:

                    raise ViewTargetNotCallableError(
                        self.parent,
                        onshow,
                        menu_element
                    )
            else:
                raise ViewAttributeError(
                    self.parent,
                    onshow,
                    menu_element
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
            raise MenuNameError(menu_element)

        if not title:
            raise MenuTitleError(menu_element)

        submenu = menu.addMenu(title)
        setattr(menu, 'menu%s' % name.capitalize(), submenu)
        self.bindChildItems(submenu, menu_element.childNodes)

    def bindAction(self, menu, action_element):

        name = action_element.getAttribute('name')
        target = action_element.getAttribute('target')
        shortcut = action_element.getAttribute('shortcut')
        title = action_element.getAttribute('title')
        icon = action_element.getAttribute('icon')
        disabled = action_element.hasAttribute('disabled')

        if not name:
            raise MenuNameError(action_element)

        if not target:
            raise ActionTargetError(action_element)

        if not title:
            raise MenuTitleError(action_element)

        if not hasattr(self.parent, target):
            raise ViewAttributeError(
                self.parent,
                target,
                action_element
            )

        action = menu.addAction(title)
        setattr(menu, 'action%s' % name.capitalize(), action)
        attr_target = getattr(self.parent, target)
        action.connect(
            SIGNAL('triggered()'),
            attr_target
        )

        if icon:
            action.setIcon(QIcon(QPixmap(icon)))

        if not shortcut and action_element.hasAttribute('shortcut'):
            raise MenuShortcutError(action_element)

        elif shortcut:

            try:

                keysequence = QKeySequence(self.getKeySecuence(shortcut))
                shortcut_attr = QShortcut(keysequence, self.parent)
                shortcut_attr.connect(
                    SIGNAL('activated()'),
                    attr_target
                )
                shortcut_attr.setEnabled(not disabled)
                action.setShortcut(keysequence)
                setattr(action, 'actionShortcut', shortcut_attr)

            except AttributeError:

                raise MenuShortcutKeysecuenceError(
                    self.parent,
                    shortcut,
                    action_element
                )

        action.setEnabled(not disabled)

    def getKeySecuence(self, shortcut):
        secuence = shortcut.split("+")

        if len(secuence) > 1:
            return reduce(
                lambda x, y: getattr(Qt, x) + getattr(Qt, y),
                secuence
            )
        else:
            return getattr(Qt, secuence[0])
