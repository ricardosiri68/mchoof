from .base_exceptions import XMLNodeException


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


class ModelBindingTreeViewError(XMLNodeException):

    def __init__(self, view, attr_name, element):

        message = 'The model binding {attr_name} tree of {view_classname} is\
            not a instance of QTreeView'.format(
            attr_name=attr_name,
            view_classname=view.__class__.__name__
        )

        super(ModelBindingTreeViewError, self).__init__(element, message)
