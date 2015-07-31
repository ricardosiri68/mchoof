from PySide.QtCore import QAbstractItemModel, Qt, QModelIndex, QSize
from .base import BaseModel
from .tree_node import Node
from mchoof.config.tree_model import TreeModelConfig


class TreeModel(QAbstractItemModel, BaseModel):

    first_col_size = QSize(10, 20)
    rest_col_size = QSize(100, 20)

    __childnodes_attr = None
    __column_methods = []
    __headers = []

    def __init__(self, parent=None):

        QAbstractItemModel.__init__(self, parent)
        BaseModel.__init__(self)

        self.rootNode = Node()
        self.data_methods.update({
            Qt.SizeHintRole: self.data_size
        })

        if self.model_config:
            TreeModelConfig(self)

        self.objects = self.session.query(self.schema)

    def columnCount(self, parent):

        return len(self.__column_methods)

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

            return self.column_methods[index.column()](
                index,
                Qt.DisplayRole
            )

    def data_edit(self, index):

        node = index.internalPointer()
        record = node.record()
        keys = record.__table__.columns.keys()

        return getattr(record, keys[index.column()])

    def data_size(self, index):

        return self.rest_col_size if index.column() else self.first_col_size

    def headerData(self, section, orientation, role=Qt.DisplayRole):

        if role == Qt.DisplayRole and orientation == Qt.Horizontal:

            if section:
                return self.headers[section]

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

        self.__records = records
        self.rootNode.clearChilds()

        for record in self.__records:

            node = Node(record, self.rootNode)

            for childrecord in getattr(record, self.childnodes_attr):

                Node(childrecord, node)

    @property
    def column_methods(self):

        return self.__column_methods

    @property
    def headers(self):

        return self.__headers

    @property
    def childnodes_attr(self):

        return self.__childnodes_attr

    @childnodes_attr.setter
    def childnodes_attr(self, value):

        self.__childnodes_attr = value

    def add(self, row, **kwargs):

        index = self.index(row, 0)

        self.beginInsertRows(index.parent(), index.row(), index.row())

        newobject = self.schema(**kwargs)

        self.session.add(newobject)
        self.records.insert(index.row(), newobject)

        self.endInsertRows()

        return newobject

    def delete(self):

        pass
