import os
from PySide.QtCore import SIGNAL
from .parser import ConfParser
from . import exceptions


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

        if not name:
            raise exceptions.MenuNameError(action)

        if not title:
            raise exceptions.MenuTitleError(action)

        menu = parentMenu.addMenu(title)

        setattr(
            parentMenu,
            format_name % name,
            menu
        )

        return menu

    def bindRootAction(self, rootMenu, action):

        return self.bindMenu('rootMenu%s', rootMenu, action)

    def bindMenuAction(self, parentMenu, action):

        return self.bindMenu('menu%s', parentMenu, action)

    def bindAction(self, parentMenu, action):

        name = action.getAttribute('name')
        target = action.getAttribute('target')
        title = action.getAttribute('title')

        if not name:
            raise exceptions.MenuNameError(action)

        if not title:
            raise exceptions.MenuTitleError(action)

        if not target:
            raise exceptions.ActionTargetError(action)

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
