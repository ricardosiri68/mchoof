import os
from .parser import ConfParser


class MenuBarParser(ConfParser):

    def __init__(self, parent):
        conf_path = os.path.join(
            parent.__class__.__module__.split('.')[0],
            'conf',
            parent.menubar_conf
        )
        ConfParser.__init__(self, conf_path)
        parentMenu = parent.menubar
        self.bindActions(parentMenu, self.document().childNodes)

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

    def bindRootAction(self, rootMenu, action):
        menu = rootMenu.addMenu(action.getAttribute('title'))
        setattr(
            rootMenu,
            'rootMenu%s' % action.getAttribute('name').capitalize(),
            menu
        )
        return menu

    def bindMenuAction(self, parentMenu, action):
        menu = parentMenu.addMenu(action.getAttribute('title'))
        setattr(
            parentMenu,
            'menu%s' % action.getAttribute('name').capitalize(),
            menu
        )
        return menu

    def bindAction(self, parentMenu, action):
        pass
