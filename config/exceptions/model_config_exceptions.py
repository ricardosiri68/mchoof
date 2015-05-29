from base_exceptions import XMLNodeException


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

        super(ModelConfNotFound, self).__init__(message)


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


class ModelConfigNotChildNodeError(XMLNodeException):

    def __init__(self, model, element):

        message = 'The model config of {model_classname} don\'t has or has a\
            wrong childnodes element'.format(
            model_classname=model.__class__.__name__
        )

        super(ModelConfigNotChildNode, self).__init_(element, message)
