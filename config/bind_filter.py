from PySide.QtCore import SIGNAL
from .exceptions.view_exceptions import ViewAttributeError
from .exceptions.model_binding_exceptions import (
    ModelBindingFilterNonInputError,
    ModelBindingFilterTypeMethodError,
    ModelBindingFilterNonTypeError,
    ModelBindingFilterMethodError,
    ModelBindingNonFilterMethodError
)


class ModelBindFilterParser:

    def __init__(self, parser_parent):
        self.parser_parent = parser_parent
        self.parent = parser_parent.parent

    def bindFilters(self, model, model_bindings):
        for model_binding in model_bindings:
            if model_binding.nodeName == 'filter':
                self.bindFilter(model, model_binding)

    def bindFilter(self, model, model_binding):
        input = model_binding.getAttribute('input')
        filter_type = model_binding.getAttribute('type')
        model_method = model_binding.getAttribute('method')

        if input:
            if hasattr(self.parent, input):
                input_attr = getattr(self.parent, input)

            else:
                raise ViewAttributeError(
                    self.parent,
                    input,
                    model_binding
                )
        else:
            raise ModelBindingFilterNonInputError(
                self.parent,
                model_binding
            )

        if filter_type:
            if hasattr(self, filter_type):
                filter_type_method = getattr(self, filter_type)

            else:
                raise ModelBindingFilterTypeMethodError(
                    self.parent,
                    filter_type,
                    model_binding
                )
        else:
            raise ModelBindingFilterNonTypeError(
                self.parent,
                model_binding
            )

        if model_method:
            if hasattr(model, model_method):
                filter_method = getattr(model, model_method)

            else:
                raise ModelBindingFilterMethodError(
                    model,
                    model_method,
                    model_binding
                )
        else:
            raise ModelBindingNonFilterMethodError(
                model,
                model_binding
            )

        filter_type_method(input_attr, filter_method)

    def text(self, input, filter_method):
        input.connect(
            SIGNAL('textChanged(QString)'),
            filter_method
        )
