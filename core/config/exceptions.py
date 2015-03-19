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


class ModelBindingListDisplayFieldError(XMLNodeException):

    def __init__(self, view, model, element):
        message = 'The model binding of {model_classname} list on\
            {view_classname} don\'t has a display field'.format(
            model_classname=model.__class__.__name__,
            view_classname=view.__class__.__name__
        )
        super(ModelBindingListDisplayFieldError, self).__init__(
            element,
            message
        )


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
        message = 'Fail to map de the field {fieldname} on view\
            {view_classname} from the model {model_classname}'.format(
            fieldname=fieldname,
            view_classname=mapper.parent().__class__.__name__,
            model_classname=mapper.model().__class__.__name__
        )
        super(ModelBindingMappingFieldError, self).__init__(binding, message)


class ModelBindingMappingCommiterError(XMLNodeException):

    def __init__(self, view, commiter, element):
        message = 'The commiter {commiter} on the view {view_classname} is not\
            a QDialogButtonBox'.format(
            commiter=commiter,
            view_classname=view.__class__.__name__
        )
        super(ModelBindingMappingCommiterError, self).__init__(
            element,
            message
        )


class ModelBindingFilterNonInputError(XMLNodeException):

    def __init__(self, view, element):
        message = 'The model binding filter of {view_classname} has no input\
            attribute'.format(view_classname=view.__class__.__name__)
        super(ModelBindingFilterNonInputError, self).__init__(element, message)


class ModelBindingFilterTypeMethodError(XMLNodeException):

    def __init__(self, view, filter_type, element):
        message = 'The model binding filter type {filter_type} of\
            {view_clasname} non exist'.format(
            view_classname=view.__class__.__name__,
            filter_type=filter_type
        )
        super(ModelBindingFilterTypeMethodError, self).__init__(
            element,
            message
        )


class ModelBindingFilterNonTypeError(XMLNodeException):

    def __init__(self, view, element):
        message = 'The model binding filter of {view_classname} has no type'\
            .format(view_classname=view.__class__.__name__)
        super(ModelBindingFilterNonTypeError, self).__init__(element, message)


class ModelBindingFilterMethodError(XMLNodeException):

    def __init__(self, view, model, model_method, element):
        message = 'The model binding filter {model_method} on the model\
            {model_classname} defined on the view {view_classname} non exist'\
            .format(
            model_method=model_method,
            model__classname=model.__class__.__name__,
            view_classname=view.__class__.__name__
        )
        super(ModelBindingFilterMethodError, self).__init__(element, message)


class ModelBindingNonFilterMethodError(XMLNodeException):

    def __init__(self, view, element):
        message = 'The model binding filter of {view_classname} non exist'\
            .format(view_classname=view.__class__.__name__)
        super(ModelBindingNonFilterMethodError, self).__init__(
            element,
            message
        )


class ModelConfigNameError(XMLNodeException):

    def __init__(self, model, element):
        message = 'A model conf setted on {model_classname} has no name\
            attribute'.format(
            model_classname=model.__class__.__name__
        )
        super(ModelConfigNameError, self).__init__(element, message)


class ModelConfNotFound(Exception):

    def __init__(self, model):
        message = 'The model conf of {model_classname} is not setted on\
            model_config file'.format(
            model_classname=model.__class__.__name__
        )
        super(ModelConfNotFound).__init__(message)


class ModelConfigFieldnameError(XMLNodeException):

    def __init__(self, model, element):
        message = 'The model config of {model_classname} don\'t has fieldname'\
            .format(model_classname=model.__class__.__name__)
        super(ModelConfigFieldnameError, self).__init__(element, message)


class ModelConfigNotHasFieldError(XMLNodeException):

    def __init__(self, model, fieldname, element):
        message = 'The model config of {model_classname} don\'t has the field\
            {fieldname} on his schema'.format(
            model_classname=model.__class__.__name__,
            fieldname=fieldname
        )
        super(ModelConfigNotHasFieldError, self).__init__(element, message)


class ModelConfigHexColorError(XMLNodeException):

    def __init__(self, model, attrname, hexcolor, element):
        message = '{hexcolor} is not a valid hexadecimal notation color on the\
            attribute {attrname} on {model_classname}'\
            .format(
            hexcolor=hexcolor,
            attrname=attrname,
            model_classname=model.__class__.__name__
        )
        super(ModelConfigHexColorError, self).__init__(element, message)


class ModelConfigRelatedFieldError(XMLNodeException):

    def __init__(self, model, element):
        message = 'The model config of {model_classname} has a invalid\
            relatedfield attribute'.format(
            model_classname=model.__class__.__name__
        )
        super(ModelConfigRelatedFieldError, self).__init__(element, message)


class ModelConfigRelatedAttributeError(XMLNodeException):

    def __init__(self, model, related_attr, element):
        message = 'The model config of {model_classname} don\'t has a\
            {related_attr} attribute on it\'s schema'.format(
            model_classname=model.__class__.__name__,
            related_attr=related_attr
        )
        super(ModelConfigRelatedAttributeError, self).__init__(
            element,
            message
        )


class SignalNameError(XMLNodeException):

    def __init__(self, view, element):
        message = 'The signal config on the view {view_classname} has no name'\
            .format(view_classname=view.__class__.__name__)
        super(SignalNameError, self).__init__(element, message)


class SignalTargetError(XMLNodeException):

    def __init__(self, view, element):
        message = 'The signal config on the view {view_classname} has no\
            target'.format(view_classname=view.__class__.__name__)
        super(SignalTargetError, self).__init__(element, message)


class SignalInvalidTargetError(XMLNodeException):

    def __init__(self, view, target, element):
        message = 'The view {view_classname} has no attribute called {target}'\
            .format(
                view_classname=view.__class__.__name__,
                target=target
            )
        super(SignalInvalidTargetError, self).__init__(element, message)


class SignalAttributeSenderNonValueError(XMLNodeException):

    def __init__(self, view, qobject, element):

        if view is qobject:
            message = 'The signal config on {view_classname} has a non value \
                sender'.format(view_classname=view.__class__.__name__)
        else:
            message = 'The signal config on {view_classname} has a attribute\
            called {qobject_name} with non value sender'.format(
                view_classname=view.__class__.__name__,
                qobject_name=element.parentNode.getAttribute('name')
            )

        super(SignalAttributeSenderNonValueError, self).__init__(
            element,
            message
        )


class SignalQObjectNonHasAttrError(XMLNodeException):

    def __init__(self, view,  qobject, attrname, element):
        if view is qobject:
            message = 'The signal config on {view_classname} who don\'t has\
                attrname called {attrname}'.format(
                view_classname=view.__class__name__,
                attrname=attrname
            )
        else:
            message = 'The signal config on {view_classname} has a qobject\
                {qobject_name} who don\'t has attrname called {attrname}'\
                .format(
                view_classname=view.__class__.__name__,
                qobject=element.parentNode.getAttribute('name'),
                attrname=attrname
            )
        super(SignalQObjectNonHasAttrError, self).__init__(element, message)


class SignalAttributeSenderNameError(XMLNodeException):

    def __init__(self, view, element):
        message = 'The signal  congig on {view_classname} has don\'t has name\
            of the sender attribute'.format(
            view_classname=view.__class__.__name__
        )
        super(SignalAttributeSenderNameError, self).__init__(element, message)
