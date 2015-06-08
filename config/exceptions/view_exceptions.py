from .base_exceptions import XMLNodeException


class ViewAttributeError(XMLNodeException):

    def __init__(self, view, attribute_name, binding):

        message = 'The view {view_classname} has no attribute called\
            {attribute_name}'.format(
            view_classname=view.__class__.__name__,
            attribute_name=attribute_name
        )

        super(ViewAttributeError, self).__init__(binding, message)


class ViewTargetNotCallableError(XMLNodeException):

    def __init__(self, view, attribute_name, binding):

        message = 'The attribute {attribute_name} of de view {view_classname}\
            is not callable'.format(
            attribute_name=attribute_name,
            view_classname=view.__class__.__name__
        )

        super(ViewTargetNotCallableError, self).__init__(binding, message)


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


class NoCompletionFieldException(XMLNodeException):

    def __init__(self, view, element):

        message = 'No completionfield on the {view_classname} view'.format(
            view_classname=view.__class__.__name__
        )

        super(NoCompletionFieldException, self).__init__(element, message)


class NoCompletitionDataException(XMLNodeException):

    def __init__(self, view, element):

        message = ''


class NoOnNewTargetException(XMLNodeException):

    def __init__(self, view, element):

        message = 'No onnew on the completer binding on the {view_classnaame}\
            view'.format(
            view_classname=view.__class__.__name__
        )

        super(NoOnNewTargetException, self).__init__(element, message)
