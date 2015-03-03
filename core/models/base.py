from PySide.QtCore import QAbstractTableModel, Qt
from mchoof.core import db_session
from mchoof.core.models import exceptions
from mchoof.core.models.query_methods import QueryMethod
from mchoof.core.config.table_model import TableModelConfig


session = db_session.get_session()


class TableModel(QAbstractTableModel):

    records = []
    session = session
    model_config = None

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
        return getattr(self.records[index.row()], keys[index.column()])

    def data_edit(self, index):

        return self.data_display(index)

    def data_textalign(self, index):

        return self.aligments[index.column()]

    def data_background(self, index):

        return self.backgrounds[index.column()]

    def data_foreground(self, index):
        return self.foregrounds[index.column()]

    data_methods = {
        Qt.DisplayRole: data_display,
        Qt.EditRole: data_edit,
        Qt.TextAlignmentRole: data_textalign,
        Qt.BackgroundRole: data_background,
        Qt.ForegroundRole: data_foreground
    }

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

    def add(self, **kwargs):

        self.session.add(self.schema(**kwargs))

    def commit(self):

        self.session.commit()
        self.refresh()

    @QueryMethod.all
    def query(self):

        return self.objects
