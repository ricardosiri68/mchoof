from PySide.QtCore import SIGNAL
from PySide.QtGui import QDataWidgetMapper


class MhDataMapper(QDataWidgetMapper):

    selector_view = None

    def __init__(self, parent):

        super(MhDataMapper, self).__init__(parent)

        self.__delegations = {}
        self.__delegating = False

    def setSelectorView(self, selectorview):

        self.selector_view = selectorview

        if selectorview.__class__.__name__ in ('QTableView', 'QListView'):

            selectorview.selectionModel().connect(
                SIGNAL("currentChanged(QModelIndex, QModelIndex)"),
                self.currentModelIndexChanged
            )

        elif selectorview.__class__.__name__ == 'QComboBox':

            selectorview.connect(
                SIGNAL('currentIndexChanged(int)'),
                self.currentModelIndexRowChanged
            )

    def currentModelIndexChanged(self, current, previus):
        self.setCurrentModelIndex(current)

    def currentModelIndexRowChanged(self, current):
        self.setCurrentModelIndex(self.selector_view.model().index(current, 0))

    def setModelIndex(self, index):

        if self.selector_view:
            selectionModel = self.selector_view.selectionModel()
            selectionModel.setCurrentIndex(
                index,
                selectionModel.ClearAndSelect
            )

            if self.selector_view.__class__.__name__ == 'QTableView':

                self.selector_view.selectRow(index.row())

            else:

                self.selector_view.setCurrentIndex(index.row())

        self.setCurrentModelIndex(index)

    def setCurrentModelIndex(self, index):

        super(MhDataMapper, self).setCurrentModelIndex(index)

        if index.isValid():
            if self.__delegations:
                self.mapDelegations(index)

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
        index = self.model().index(start, 0, parent)
        self.setModelIndex(index)

    def rowRemoved(self, parent, start, end):
        index = self.model().sibling(start, 0, parent)
        self.setModelIndex(index)

    def addDelegatedMapping(self, widget, field_index, delegation):

        index_column = widget.model().get_field_index(delegation)

        self.__delegations[field_index] = (
            delegation,
            widget,
            index_column
        )

        widget.currentIndexChanged.connect(
            self.connectDelegatedData(widget, field_index, index_column)
        )

    def mapDelegations(self, index):

        for field_index, (delegation, widget, columnindex) in\
                self.__delegations.items():

            self.mapDelegation(index, field_index, delegation, widget)

    def mapDelegation(self, index, field_index, delegation, widget):

        model = self.model()
        index = model.index(index.row(), field_index)
        data = model.data_edit(index)

        delegated_object = widget\
            .model()\
            .objects\
            .filter_by(**{delegation: data})\
            .one()

        delegated_index = widget.model().get_index_by_object(delegated_object)

        self.delegating = True
        widget.setCurrentIndex(delegated_index.row())
        self.delegating = False

    def connectDelegatedData(self, widget, field_index, index_column):

        def setDelegatedData(index):

            if not self.delegating:

                model = widget.model()

                data = model.data_edit(model.index(index, index_column))

                row_index = self.currentIndex()

                self.model().setData(
                    self.model().index(row_index, field_index),
                    data
                )

        return setDelegatedData
