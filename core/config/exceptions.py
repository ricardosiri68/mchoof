class XMLNodeException(Exception):

    name_list = []

    def __init__(self, action, message):
        self.traceName(action)
        self.name_list.append(" >>> \n%s" % action.toprettyxml())
        error_message = '{message} on:\n {trace}'.\
            format(
                message=message,
                trace=" | ".join(self.name_list)
            )
        super(XMLNodeException, self).__init__(error_message)

    def traceName(self, action):
        self.name_list.insert(0, action.nodeName)
        if action.parentNode:
            self.traceName(action.parentNode)


class MenuNameError(XMLNodeException):

    def __init__(self, action):
        message = 'The menu item has no name attibute'
        super(MenuNameError, self).__init__(action, message)


class MenuTitleError(XMLNodeException):

    def __init__(self, action):
        message = 'The menu item has no title attibute'
        super(MenuTitleError, self).__init__(action, message)


class ActionTargetError(XMLNodeException):

    def __init__(self, action):
        message = 'The action menu item has no target'
        super(ActionTargetError, self).__init__(action, message)
