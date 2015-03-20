from PySide.QtCore import SIGNAL
from PySide.QtGui import QTreeView
from . import exceptions


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
            raise exceptions.ModelBindingNameError(element)

        if not hasattr(self.parent, name):
            raise exceptions.ViewAttributeError(self.parent, name, element)

        treeview = getattr(self.parent, name)

        if not isinstance(treeview, QTreeView):
            raise exceptions.ModelBindingTreeViewError(
                self.parent,
                name,
                element
            )

        treeview.setModel(model)
