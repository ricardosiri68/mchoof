import os
# from PySide.Qtcore import SIGNAL
from .parser import ConfParser
from . import exceptions


class ModelBindingParser(ConfParser):

    def __init__(self, parent):
        conf_path = os.path.join(
            parent.__class__.__module__.split('.')[0],
            'conf',
            parent.models_binding_conf
        )
        self.parent = parent
        ConfParser.__init__(self, conf_path)
        self.bindModels()

    def bindModels(self):
        for binding in self.rootNode().childNodes:
            if binding.nodeName == 'model':
                self.bindModel(binding)

    def bindModel(self, binding):
        name = binding.getAttribute('name')

        if not name:
            raise exceptions.ModelBindingNameError(binding)

        try:
            model = getattr(self.parent, name, binding)
        except AttributeError:
            raise exceptions.ModelBindingViewAttributeError(
                self.parent,
                name,
                binding
            )

        if binding.hasAttribute('autoload'):


            querymethodname = binding.getAttribute('autoload')
            querymethodname = querymethodname if querymethodname else 'query'

            try:
                querymethod = getattr(model, querymethodname)
            except AttributeError:
                raise exceptions.ModelQuerymethodError(
                    self.parent,
                    model,
                    querymethod,
                    binding
                )

            querymethod()

        self.bindTables(model, binding.childNodes)

    def bindTables(self, model, childnodes):
        for element in childnodes:
            if element.nodeName == 'table':
                self.bindTable(model, element)

    def bindTable(self, model, element):
        name = element.getAttribute('name')

        if not name:
            raise exceptions.ModelBindingNameError(element)

        try:
            table = getattr(self.parent, name)
        except AttributeError:
            raise exceptions.ModelBindingViewAttributeError(
                self.parent,
                name,
                element
            )

        table.setModel(model)

        self.configTableFields(table, element.childNodes)

    def configTableFields(self, table, fields_elements):
        for field_element in fields_elements:
            if field_element.nodeName == 'field':
                self.configTableField(table, field_element)

    def configTableField(self, table, field_element):
        name = field_element.getAttribute('name')

        if not name:
            raise exceptions.ModelBindingNameError(field_element)

        if field_element.hasAttribute('hidden'):
            # hide field
            pass

        if field_element.hasAttribute('width'):
            # set with attr
            pass
