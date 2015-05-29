class NoTemplateError(Exception):

    def __init__(self):
        message = '{class_name} Don\'t has defined template name'.format(
            class_name=self.__class__.__name__
        )
        super(NoTemplateError, self).__init__(message)


class MainWidgetError(Exception):

    def __init__(self):
        message = '{class_name} Don\'t have defined a main_widget'.format(
            class_name=self.__class__.__name__
        )
        super(MainWidgetError, self).__init__(message)
