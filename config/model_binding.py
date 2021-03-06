import os
from .parser import ConfParser
from .exceptions.model_binding_exceptions import (
    ModelBindingNameError,
    ModelBindingViewAttributeError,
    ModelQuerymethodError
)
from .bind_mapper import ModelBindMapperParser
from .bind_table import ModelBindTableParser
from .bind_list import ModelBindListParser
from .bind_tree import ModelBindTreeParser
from .bind_filter import ModelBindFilterParser
from .bind_completer import ModelBindCompleterParser


class ModelBindingParser(ConfParser):

    def __init__(self, parent):

        conf_path = os.path.join(
            parent.__class__.__module__.split('.')[0],
            'conf',
            parent.models_binding_conf
        )
        self.parent = parent
        ConfParser.__init__(self, conf_path)

        self.mapper_parser = ModelBindMapperParser(self)
        self.table_parser = ModelBindTableParser(self)
        self.list_parser = ModelBindListParser(self)
        self.tree_parser = ModelBindTreeParser(self)
        self.filter_parser = ModelBindFilterParser(self)
        self.completer_parser = ModelBindCompleterParser(self)

        self.bindModels()

    def bindModels(self):

        for binding in self.rootNode().childNodes:
            if binding.nodeName == 'model':
                self.bindModel(binding)

    def bindModel(self, binding):

        name = binding.getAttribute('name')

        if not name:
            raise ModelBindingNameError(binding)

        try:
            model = getattr(self.parent, name, binding)
        except AttributeError:
            raise ModelBindingViewAttributeError(
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
                raise ModelQuerymethodError(
                    self.parent,
                    model,
                    querymethod,
                    binding
                )

            querymethod()

        modelmro = [mro.__name__ for mro in model.__class__.__mro__]

        if 'TableModel' in modelmro:

            self.table_parser.bindTables(model, binding.childNodes)
            self.list_parser.bindLists(model, binding.childNodes)
            self.mapper_parser.bindMappers(model, binding.childNodes)
            self.filter_parser.bindFilters(model, binding.childNodes)
            self.completer_parser.bindCompleters(model, binding.childNodes)

        elif 'TreeModel' in modelmro:

            self.tree_parser.bindTrees(model, binding.childNodes)
