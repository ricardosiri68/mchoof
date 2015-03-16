from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide.QtGui import QPixmap
from mchoof.core import db_session
from mchoof.core.models import exceptions
from mchoof.core.models.query_methods import QueryMethod
from mchoof.core.config.table_model import TableModelConfig


session = db_session.get_session()


class TableModel(QAbstractTableModel):

    records = []
    session = session
    model_config = None
    filters_list = {}
    bool_decoration = {
        False: QPixmap(':/crud/bullet-red'),
        True: QPixmap(':/crud/bullet-green')
    }

    def __init__(self, parent=None):

        super(TableModel, self).__init__(parent)

        self.headers = self.schema.__table__.columns.keys()
        self.aligments = len(self.headers) * [Qt.AlignLeft]
        self.backgrounds = len(self.headers) * [None]
        self.foregrounds = len(self.headers) * [None]

        if self.model_config:
            TableModelConfig(self)

        self.objects = self.session.query(self.schema)

    def columnCount(self, index=None):

        return len(self.schema.__table__.columns)

    def rowCount(self, index=None):

        return len(self.records)

    def data(self, index, role=Qt.DisplayRole):

        if role in self.data_methods:
            return self.data_methods[role](self, index)

    def data_display(self, index):

        keys = self.schema.__table__.columns.keys()
        data = getattr(self.records[index.row()], keys[index.column()])

        if isinstance(data, (str, unicode, int, float, long)):
            return data

    def data_edit(self, index):

        return self.data_display(index)

    def data_textalign(self, index):

        return self.aligments[index.column()]

    def data_background(self, index):

        return self.backgrounds[index.column()]

    def data_foreground(self, index):
        return self.foregrounds[index.column()]

    def data_decoration(self, index):

        keys = self.schema.__table__.columns.keys()
        data = getattr(self.records[index.row()], keys[index.column()])

        if isinstance(data, bool):
            return self.bool_decoration[data]

    data_methods = {
        Qt.DisplayRole: data_display,
        Qt.EditRole: data_edit,
        Qt.TextAlignmentRole: data_textalign,
        Qt.BackgroundRole: data_background,
        Qt.ForegroundRole: data_foreground,
        Qt.DecorationRole: data_decoration
    }

    def setData(self, index, value, role=Qt.EditRole):
        try:

            setattr(
                self.records[index.row()],
                self.get_field_by_index(index.column()),
                value
            )

            self.dataChanged.emit(index, index)
            return True

        except AttributeError or IndexError:

            raise exceptions.ModelSetDataError(self, index, value)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        else:
            super(TableModel, self).headerData(section, orientation, role)

    def refresh(self):

        getattr(
            self,
            self.current_query['method']
        )(
            *self.current_query['args'],
            **self.current_query['kwargs']
        )

    def get_field_index(self, fieldname):

        try:
            return self.schema.__table__.columns.keys().index(fieldname)

        except ValueError:
            raise exceptions.FieldDoesntExist(self.schema, fieldname)

    def get_field_by_index(self, index):

        return self.schema.__table__.columns.keys()[index]

    def get_index_by_object(self, obj):
        return self.index(self.records.index(obj), 0)

    def add(self, row, **kwargs):

        index = self.index(row, 0)
        self.beginInsertRows(index.parent(), index.row(), index.row())

        newobject = self.schema(**kwargs)
        self.session.add(newobject)
        self.records.insert(index.row(), newobject)

        self.endInsertRows()

        return newobject

    def save(self, index, **kwargs):

        try:
            schema_obj = self.records[index]
        except IndexError:
            raise exceptions.ModelIndexError(self, index)

        for field, value in kwargs.items():

            if not field in self.schema.__table__.columns.keys():
                raise exceptions.FieldDoesntExist(self.schema, field)

            setattr(schema_obj, field, value)

        self.dataChanged.emit(QModelIndex(), QModelIndex())

    def removeRow(self, row, index=QModelIndex()):

        self.session.delete(self.records.pop(index.row()))
        return True

    def delete(self, index):

        self.beginRemoveRows(index.parent(), index.row(), index.row())
        self.session.delete(self.records.pop(index.row()))
        self.endRemoveRows()

    def commit(self, refresh=True):

        self.session.commit()

        if refresh:
            self.refresh()

    @QueryMethod.all
    def query(self):

        return self.objects
