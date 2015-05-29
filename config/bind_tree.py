from PySide.QtGui import QTreeView
from .exceptions.view_exceptions import ViewAttributeError
from .exceptions.model_binding_exceptions import (
    ModelBindingNameError,
    ModelBindingTreeViewError
)


class ModelBindTreeParser:

    def __init__(self, parser_parent):

        self.parser_parent = parser_parent
        self.parent = parser_parent.parent

    def bindTrees(self, model, childnodes):
        for element in childnodes:
            if element.nodeName == 'tree':
                self.bindTree(model, element)

    def bindTree(self, model, element):
        name = element.getAttribute('name')

        if not name:
            raise ModelBindingNameError(element)

        if not hasattr(self.parent, name):
            raise ViewAttributeError(self.parent, name, element)

        treeview = getattr(self.parent, name)

        if not isinstance(treeview, QTreeView):
            raise ModelBindingTreeViewError(
                self.parent,
                name,
                element
            )

        treeview.setModel(model)
        treeview.setColumnWidth(0, 50)
        self.configColumns(model, treeview, element.childNodes)

    def configColumns(self, model, treeview, childnodes):

        for element in childnodes:
            if element.nodeName == 'column':
                self.configColumn(model, treeview, element)

    def configColumn(self, model, treeview, column_element):

        name = column_element.getAttribute('name')
        width = column_element.getAttribute('width')
        hidden = column_element.getAttribute('hidden')
