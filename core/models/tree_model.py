from PySide.QtCore import QAbstractItemModel, Qt, QModelIndex, QSize
from .base import BaseModel
from .tree_node import Node
from mchoof.core.config.tree_model import TreeModelConfig


class TreeModel(QAbstractItemModel, BaseModel):

    childnodes_attr = None
    rootNode = Node()
    first_col_size = QSize(10, 20)
    rest_col_size = QSize(100, 20)

    def __init__(self, parent=None):
        QAbstractItemModel.__init__(self, parent)
        BaseModel.__init__(self)

        self.data_methods.update({
            Qt.SizeHintRole: self.data_size
        })

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

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role=Qt.DisplayRole):

        if not index.isValid():
            return

        return BaseModel.data(self, index, role)

    def data_display(self, index):

        if index.column():
            node = index.internalPointer()
            record = node.record()
            keys = record.__table__.columns.keys()

            return getattr(record, keys[index.column()])

    def data_edit(self, index):

        node = index.internalPointer()
        record = node.record()
        keys = record.__table__.columns.keys()

        return getattr(record, keys[index.column()])

    def data_size(self, index):

        return self.rest_col_size if index.column() else self.first_col_size

    def headerData(self, section, orientation, role=Qt.DisplayRole):

        if role == Qt.DisplayRole:

            if section:
                return "BZNHeader"

    def parent(self, index):
        node = index.internalPointer()
        parentNode = node.parent()

        return QModelIndex() if parentNode == self.rootNode else\
            self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent=QModelIndex()):

        parentNode = parent.internalPointer() if parent.isValid() else\
            self.rootNode

        child = parentNode.child(row)

        if child:
            record = child.record()
            keys = record.__table__.columns.keys()

            return self.createIndex(row, column, child)\
                if column < len(keys) else QModelIndex()

        else:

            return QModelIndex()

    @BaseModel.records.setter
    def records(self, records):

        self._records = records

        for record in self._records:

            node = Node(record, self.rootNode)

            for childrecord in getattr(record, self.childnodes_attr):

                Node(childrecord, node)
