from PySide.QtCore import SIGNAL
from PySide.QtGui import QDataWidgetMapper


class MhDataMapper(QDataWidgetMapper):

    selector_view = None

    def setSelectorView(self, selectorview):

        self.selector_view = selectorview

        selectorview.selectionModel().connect(
            SIGNAL("currentChanged(QModelIndex, QModelIndex)"),
            self.currentModelIndexChanged
        )

    def currentModelIndexChanged(self, current, previus):
        self.setCurrentModelIndex(current)

    def setModelIndex(self, index):

        if self.selector_view:
            selectionModel = self.selector_view.selectionModel()
            selectionModel.setCurrentIndex(
                index,
                selectionModel.ClearAndSelect
            )

            if self.selector_view.__class__.__name__ == 'QTableView':
                self.selector_view.selectRow(index.row())

        self.setCurrentModelIndex(index)

    def setModel(self, model):

        super(MhDataMapper, self).setModel(model)

        model.connect(
            SIGNAL('rowsInserted(QModelIndex, int, int)'),
            self.rowInserted
        )

        model.connect(
            SIGNAL('rowsRemoved(QModelIndex, int, int)'),
            self.rowRemoved
        )

    def rowInserted(self, parent, start, end):
        index = self.model().index(start, 0)
        self.setModelIndex(index)

    def rowRemoved(self, parent, start, end):
        index = self.model().sibling(start, 0, parent)
        self.setModelIndex(index)