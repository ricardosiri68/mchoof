import re


class XMLNodeException(Exception):

    name_list = []

    def __init__(self, action, message):

        message = re.sub('\s+', ' ', message)
        self.traceName(action)
        self.name_list.append(" >>> \n%s" % action.toprettyxml())

        error_message = '{message} on:\n {trace}'.format(
            message=message,
            trace=" | ".join(self.name_list)
        )

        super(XMLNodeException, self).__init__(error_message)

    def traceName(self, action):

        self.name_list.insert(0, action.nodeName)
        if action.parentNode:
            self.traceName(action.parentNode)
