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

        self.configModel()

    def configModel(self):

        try:

            col_count = int(self.model_element.getAttribute('col_count'))

        except ValueError:
            pass

        self.configColumns()
        self.configChildnodes()

    def configChildNodes(self):

        childnodes = None
        for element in self.model_element.childNodes:

            if element.nodeName == 'childnodes':

                childnodes = element

        if not childnodes:

            raise ModelConfigNotChildNodeError(
                self.model,
                self.model_element
            )

        childnodes_name = childnodes.getAttribute('name')

        if not childnodes_name:

            raise ModelConfigNotChildNodeError(
                self.model,
                self.model_element
            )

        if not hasattr(self.model.schema, childnodes_name):
            raise ModelConfigRelatedAttributeError(
                self.model,
                childnodes_name,
                self.model_element
            )

        self.model.childnodes_attr = childnodes_name
