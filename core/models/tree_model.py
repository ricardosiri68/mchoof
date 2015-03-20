from PySide.QtCore import QAbstractItemModel, Qt, QModelIndex
from .base import session, BaseModel
from .tree_node import Node
from mchoof.core.config.tree_model import TreeModelConfig


class TreeModel(QAbstractItemModel, BaseModel):

    records = []  # root_nodes
    session = session
    model_config = None
    filter_list = {}
    childnodes_attr = None
    rootNode = Node()

    def __init__(self, parent=None):
        super(TreeModel, self).__init__(parent)

        if self.model_config:
            TreeModelConfig(self)

        self.objects = self.session.query(self.schema)

    def columnCount(self, parent):

        if parent.isValid():

            return len(self.childSchema.__table__.columns.keys())

        else:

            return len(self.schema.__table__.columns.keys())

    def rowCount(self, parent):

        parentNode = parent.internalPointer() if parent.isValid() else\
            self.rootNode

        return parentNode.childCount()

    def headerData(self, section, orientation, role):
        return 'BZNGroup'

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role=Qt.DisplayRole):

        if not index.isValid():
            return

        node = index.internalPointer()

        if role == Qt.DisplayRole:
            record = node.record()
            keys = record.__table__.columns.keys()

            try:
                return getattr(record, keys[index.column()])

            except IndexError:
                pass

    def parent(self, index):
        node = index.internalPointer()
        parentNode = node.parent()

        return QModelIndex() if parentNode == self.rootNode else\
            self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent=QModelIndex()):

        parentNode = parent.internalPointer() if parent.isValid() else\
            self.rootNode

        child = parentNode.child(row)

        return self.createIndex(row, column, child) if child else QModelIndex()
