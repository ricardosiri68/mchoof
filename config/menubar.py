import os
from PySide.QtGui import QPixmap, QIcon, QKeySequence
from PySide.QtCore import SIGNAL, Qt
from .parser import ConfParser
from .exceptions.menu_exceptions import (
    MenuNameError,
    MenuTitleError,
    ActionTargetError,
    MenuShortcutError,
    MenuShortcutKeysecuenceError
)


class MenuBarParser(ConfParser):

    def __init__(self, parent):

        conf_path = os.path.join(
            parent.__class__.__module__.split('.')[0],
            'conf',
            parent.menubar_conf
        )

        self.parent = parent
        ConfParser.__init__(self, conf_path)
        parentMenu = self.parent.menubar

        self.bindActions(parentMenu, self.rootNode().childNodes)

    def bindActions(self, parentMenu, actions):

        for action in actions:

            if action.nodeName == 'action':

                if action.parentNode.tagName == 'root' and action.childNodes:

                    self.bindActions(
                        self.bindRootAction(parentMenu, action),
                        action.childNodes
                    )

                elif action.parentNode.tagName == 'action':

                    if action.childNodes:

                        self.bindActions(
                            self.bindMenuAction(parentMenu, action),
                            action.childNodes
                        )

                    elif action.parentNode.tagName == 'action':

                        self.bindAction(parentMenu, action)

    def bindMenu(self, format_name, parentMenu, action):
        name = action.getAttribute('name').capitalize()
        title = action.getAttribute('title')
        disabled = action.hasAttribute('disabled')

        if not name:
            raise MenuNameError(action)

        if not title:
            raise MenuTitleError(action)

        menu = parentMenu.addMenu(title)

        setattr(
            parentMenu,
            format_name % name,
            menu
        )

        if disabled:
            menu.setEnabled(False)

        return menu

    def bindRootAction(self, rootMenu, action):

        return self.bindMenu('rootMenu%s', rootMenu, action)

    def bindMenuAction(self, parentMenu, action):

        return self.bindMenu('menu%s', parentMenu, action)

    def bindAction(self, parentMenu, action):

        name = action.getAttribute('name')
        target = action.getAttribute('target')
        title = action.getAttribute('title')
        icon = action.getAttribute('icon')
        shortcut = action.getAttribute('shortcut')
        disabled = action.hasAttribute('disabled')

        if not name:
            raise MenuNameError(action)

        if not title:
            raise MenuTitleError(action)

        if not target:
            raise ActionTargetError(action)

        actionMenu = parentMenu.addAction(title)

        setattr(
            parentMenu,
            'action%s' % name.capitalize(),
            actionMenu
        )

        if ":" in target:

            self.bindView(actionMenu, target)

        else:

            actionMenu.connect(
                SIGNAL('triggered()'),
                getattr(self.parent, target)
            )

        if icon:
            actionMenu.setIcon(QIcon(QPixmap(icon)))

        if not shortcut and action.hasAttribute('shortcut'):

            raise MenuShortcutError(action)

        elif shortcut:

            try:

                keysequence = QKeySequence(self.getKeySecuence(shortcut))
                actionMenu.setShortcut(keysequence)

            except AttributeError:

                raise MenuShortcutKeysecuenceError(
                    self.parent,
                    shortcut,
                    action
                )

        actionMenu.setEnabled(not disabled)

    def getKeySecuence(self, shortcut):
        secuence = shortcut.split("+")

        if len(secuence) > 1:
            return reduce(
                lambda x, y: getattr(Qt, x) + getattr(Qt, y),
                secuence
            )

        else:
            return getattr(Qt, secuence[0])

    def bindView(self, actionMenu, target):

            package_app, viewClassName = target.split(':')

            viewClassName = ''.join([
                name_peace.capitalize()
                for name_peace in viewClassName.split('-')
            ])

            view_module = __import__('%s.views' % package_app)
            class_view = getattr(view_module.views, viewClassName)

            actionMenu.connect(
                SIGNAL('triggered()'),
                self.parent.loadPanelView(class_view)
            )
