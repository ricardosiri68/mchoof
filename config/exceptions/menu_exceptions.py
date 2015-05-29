from .base_exceptions import XMLNodeException


class MenuNameError(XMLNodeException):

    def __init__(self, action):

        message = 'The menu item has no name attibute'

        super(MenuNameError, self).__init__(action, message)


class MenuTitleError(XMLNodeException):

    def __init__(self, action):

        message = 'The menu item has no title attibute'

        super(MenuTitleError, self).__init__(action, message)


class MenuShortcutError(XMLNodeException):

    def __init__(self, action):

        message = 'The menu item has a shortcut with no value'

        super(MenuShortcutError, self).__init__(action, message)


class MenuShortcutKeysecuenceError(XMLNodeException):

    def __init__(self, view, shortcut, action):

        message = 'Wrong keysecuence on in the shortcut {shortcut} setted on\
            the view {view_classname}'.format(
            shortcut=shortcut,
            view_classname=view.__class__.__name__
        )

        super(MenuShortcutKeysecuenceError, self).__init__(action, message)


class MenuWidgetValueError(XMLNodeException):

    def __init__(self, binding):

        message = 'The menu has no valid widget attribute'

        super(MenuWidgetValueError, self).__init__(binding, message)


class ActionTargetError(XMLNodeException):  # menu_exceptions

    def __init__(self, action):

        message = 'The action menu item has no target'

        super(ActionTargetError, self).__init__(action, message)
