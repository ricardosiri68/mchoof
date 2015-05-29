from PySide.QtCore import SIGNAL
from .exceptions.view_exceptinos import ViewAttributeError
from .exceptions.model_binding_exceptions import (
    ModelBindingNameError,
    ModelBindingListDisplayFieldError
)


class ModelBindListParser:

    def __init__(self, parser_parent):
        self.parser_parent = parser_parent
        self.parent = parser_parent.parent

    def bindLists(self, model, childnodes):
        for element in childnodes:
            if element.nodeName == 'list':
                self.bindList(model, element)

    def bindList(self, model, element):
        name = element.getAttribute('name')
        displayfield = element.getAttribute('displayfield')

        if not name:

            raise ModelBindingNameError(element)

        if not displayfield:

            raise ModelBindingListDisplayFieldError(
                self.parent,
                model,
                element
            )

        if not hasattr(self.parent, name):
            raise ViewAttributeError(self.parent, name, element)

        uilist = getattr(self.parent, name)

        self.configList(model, uilist, element, displayfield=displayfield)

    def configList(self, model, uilist, element, **kwargs):
        uilist.setModel(model)
        uilist.setModelColumn(model.get_field_index(kwargs['displayfield']))
