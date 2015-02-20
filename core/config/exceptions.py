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


class ModelBindingNameError(XMLNodeException):

    def __init__(self, binding):
        message = 'The binding has no name attribute'
        super(ModelBindingNameError, self).__init__(binding, message)


class ModelBindingViewAttributeError(XMLNodeException):

    def __init__(self, view, attribute_name, binding):
        message = 'The View {view_class} has no attribute called {name}'\
            .format(
                view_class=view.__class__.__name__,
                name=attribute_name
            )
        super(ModelBindingViewAttributeError, self).__init__(binding, message)


class ModelQuerymethodError(XMLNodeException):

    def __init__(self, view, model, querymethod_name, binding):
        message = 'The model {model_classname} setted on the view\
            {view_classname} dont\'t has a queymethod called {quermethod_name}\
            '.format(
            model_classname=model.__class__.__name__,
            view_classname=view.__class__.__name__,
            querymethod_name=querymethod_name)
        super(ModelQuerymethodError, self).__init__(binding, message)
