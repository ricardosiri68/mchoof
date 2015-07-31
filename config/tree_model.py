import os
from .parser import ConfParser
from .exceptions.model_config_exceptions import (
    ModelConfigNameError,
    ModelConfNotFound,
    ModelConfigNotChildNodeError,
    ModelConfigRelatedAttributeError,
)


class TreeModelConfig(ConfParser):

    model_element = None

    def __init__(self, model):
        conf_path = os.path.join(
            model.__class__.__module__.split('.')[0],
            'conf',
            model.model_config
        )
        self.model = model

        ConfParser.__init__(self, conf_path)

        for model_element in self.rootNode().childNodes:

            if model_element.nodeName == 'model':
                name = model_element.getAttribute('name')

                if not name:
                    raise ModelConfigNameError(
                        self.parent,
                        model_element
                    )

                if name == self.model.__class__.__name__:

                    self.model_element = model_element

                    break

        if not self.model_element:

            raise ModelConfNotFound(self.model)

        self.config()
        self.configColumns()

    def config(self):
        '''configura el modelo'''

        childnodes_attr = self.model_element.getAttribute('childnodes_attr')

        if not childnodes_attr:

            raise Exception('childnode_attr no esta definido en TreeModel')

        self.model.childnodes_attr = childnodes_attr

    def configColumns(self):

        for element in self.model_element.childNodes:

            if element.nodeName == 'column':

                self.configColumn(element)

    def configColumn(self, element):

        name = element.getAttribute('name')
        header = element.getAttribute('header')

        if not name:

            raise ModelConfigNameError(self.model, element)

        self.model.column_methods.append(getattr(self.model, name))

        self.model.headers.append(header if header else name)
