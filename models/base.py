from datetime import date
from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex, QDate,\
    QDateTime
from PySide.QtGui import QPixmap
from mchoof.core import db_session
from mchoof.models import exceptions
from mchoof.models.query_methods import QueryMethod
from mchoof.config.table_model import TableModelConfig


session = db_session.get_session()


class BaseModel(object):

    current_query = {}
    session = session
    model_config = None

    def __init__(self):

        self._related_fields = {}
        self.__records = []

        self.data_methods = {
            Qt.DisplayRole: self.data_display,
            Qt.EditRole: self.data_edit,
            Qt.TextAlignmentRole: self.data_textalign,
            Qt.BackgroundRole: self.data_background,
            Qt.ForegroundRole: self.data_foreground,
            Qt.DecorationRole: self.data_decoration
        }

    def data(self, index, role=Qt.DisplayRole):

        if role in self.data_methods:

            return self.data_methods[role](index)

    def data_display(self, index):

        pass

    def data_edit(self, index):

        pass

    def data_textalign(self, index):

        pass

    def data_background(self, index):

        pass

    def data_foreground(self, index):

        pass

    def data_decoration(self, index):

        pass

    def refresh(self):

        if self.current_query:

            getattr(
                self,
                self.current_query['method']
            )(
                *self.current_query['args'],
                **self.current_query['kwargs']
            )

    def commit(self, refresh=True):

        self.session.commit()

        if refresh:

            self.refresh()

    @property
    def records(self):
        return self.__records

    @records.setter
    def records(self, records):
        self.__records = records

    @property
    def filters_list(self):

        return self._filters_list

    @filters_list.setter
    def filters_list(self, filters_list):

        self._filters_list = filters_list

    @QueryMethod.all
    def query(self):

        return self.objects


class TableModel(QAbstractTableModel, BaseModel):

    bool_decoration = {
        False: QPixmap(':/crud/bullet-red'),
        True: QPixmap(':/crud/bullet-green')
    }

    def __init__(self, parent=None):

        QAbstractTableModel.__init__(self, parent)
        BaseModel.__init__(self)

        self.__appends = []
        self.headers = self.field_keys
        self.aligments = len(self.headers) * [
            int(Qt.AlignVCenter | Qt.AlignLeft)
        ]

        self.backgrounds = len(self.headers) * [None]
        self.foregrounds = len(self.headers) * [None]

        if self.model_config:
            TableModelConfig(self)

        self.objects = self.session.query(self.schema)

    def columnCount(self, index=None):

        return len(self.field_keys)

    def rowCount(self, index=None):

        return len(self.records)

    def data(self, index, role=Qt.DisplayRole):

        return BaseModel.data(self, index, role)

    def data_display(self, index):

        keys = self.field_keys
        data = getattr(self.records[index.row()], keys[index.column()])

        if isinstance(data, bool):
            return 'Si' if data else 'No'

        elif isinstance(data, long) and index.column() in self.related_fields:

            attribute, field = self.related_fields[index.column()]
            record_attribute = getattr(self.records[index.row()], attribute)

            return getattr(record_attribute, field)

        elif isinstance(data, date):

            return '{:%d/%m/%Y}'.format(data)

        else:

            return data

    def data_edit(self, index):

        keys = self.field_keys

        data = getattr(self.records[index.row()], keys[index.column()])

        if isinstance(data, date):

            return QDate(data.year, data.month, data.day)

        else:
            return data

    def data_textalign(self, index):

        return self.aligments[index.column()]

    def data_background(self, index):

        return self.backgrounds[index.column()]

    def data_foreground(self, index):
        return self.foregrounds[index.column()]

    def data_decoration(self, index):

        keys = self.field_keys
        data = getattr(self.records[index.row()], keys[index.column()])

        if isinstance(data, bool):
            return self.bool_decoration[data]

    def setData(self, index, value, role=Qt.EditRole):

        record = self.records[index.row()]

        try:

            field_name = self.get_field_by_index(index.column())

            if isinstance(value, QDateTime):
                schema_field = getattr(record, field_name)

                if isinstance(schema_field, date):
                    value = value.toPython()

            setattr(
                record,
                field_name,
                value
            )

            if index.column() in self.related_fields:

                attribute = self.related_fields[index.column()][0]

                relation_attr = getattr(record, attribute)

                new_relation_attr = self.session\
                    .query(relation_attr.__class__)\
                    .filter_by(id=value).one()

                setattr(record, attribute, new_relation_attr)

            self.dataChanged.emit(index, index)

            return True

        except AttributeError or IndexError, e:

            print e

            raise exceptions.ModelSetDataError(self, index, value)

    def headerData(self, section, orientation, role=Qt.DisplayRole):

        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        else:
            super(TableModel, self).headerData(section, orientation, role)

    def get_field_index(self, fieldname):

        try:
            return self.field_keys.index(fieldname)

        except ValueError:

            raise exceptions.FieldDoesntExist(self.schema, fieldname)

    def get_field_by_index(self, index):

        return self.field_keys[index]

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

    def save(self, row, **kwargs):

        try:

            schema_obj = self.records[row]

        except IndexError:

            raise exceptions.ModelIndexError(self, row)

        for field, value in kwargs.items():

            if not field in self.field_keys:

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

    @property
    def related_fields(self):

        return self._related_fields

    @related_fields.setter
    def related_fields(self, related_fields):

        self._related_fields = related_fields

    @property
    def field_keys(self):

        return self.schema.__table__.columns.keys() + self.appends

    @property
    def appends(self):

        return self.__appends
