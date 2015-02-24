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


class MenuWidgetValueError(XMLNodeException):

    def __init__(self, binding):
        message = 'The menu has no valid widget attribute'
        super(MenuWidgetValueError, self).__init__(binding, message)


class ViewAttributeError(XMLNodeException):

    def __init__(self, view, attribute_name, binding):
        message = 'The view {view_classname} has no attribute called\
            {attribute_name}'.format(
            view_classname=view.__class__.__name__,
            attribute_name=attribute_name
        )
        super(ViewAttributeError, self).__init__(binding, message)


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
            querymethod_name=querymethod_name
        )
        super(ModelQuerymethodError, self).__init__(binding, message)


class ModelBindingTableWidthFieldError(XMLNodeException):
    def __init__(self, view, fieldname, binding):
        message = 'The width of the field {fieldname} is not AUTO or a int on\
            the view {view_classname}'.format(
            view_classname=view.__class__.__name__,
            fieldname=fieldname
        )
        super(ModelBindingTableWidthFieldError, self).__init__(
            binding,
            message
        )


class ModelBindingTableFieldnameError(XMLNodeException):

    def __init__(self, view, model, fieldname, binding):
        message = 'The fieldname "{fieldname}" doesn\'t exist on the model\
            {model_classname} on the view {view_classname}'.format(
            fieldname=fieldname,
            model_classname=model.schema.__class__.__name__,
            view_classname=view.__class__.__name__
        )
        super(ModelBindingTableFieldnameError, self).__init__(binding, message)


class ModelBindingMapperAttributeError(XMLNodeException):

    def __init__(self, view, attribute_name, binding):
        message = 'The View {view_class} already has a attribute called\
            {name}'.format(
            view_class=view.__class__.__name__,
            name=attribute_name
        )
        super(ModelBindingMapperAttributeError, self).__init__(
            binding,
            message
        )


class ModelBindingMapperSelectorViewError(XMLNodeException):

    def __init__(self, binding):
        message = 'The selector view on the mapper config is empty'
        super(ModelBindingMapperSelectorViewError, self).__init__(
            binding,
            message
        )


class ModelBindingMappingAttributeError(XMLNodeException):

    def __init__(self, view, attrname, binding):
        message = 'The mapper don\'t has {attrname} defined on the view\
            {view_classname}'.format(
            attrname=attrname,
            view_classname=view.__class__.__name__
        )
        super(ModelBindingMappingAttributeError, self).__init__(
            binding,
            message
        )


class ModelBindingMappingFieldError(XMLNodeException):

    def __init__(self, mapper, fieldname, binding):
        message = 'Fail to map de the field {fieldname}\
            on view {view_classname} from the model\
            {model_classname}'.format(
            fieldname=fieldname,
            view_classname=mapper.parent().__class__.__name__,
            model_classname=mapper.model().__class__.__name__
        )
        super(ModelBindingMappingFieldError, self).__init__(binding, message)
