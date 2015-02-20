from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex
from mchoof.core import db_session


session = db_session.get_session()


def query_method(meth):

    def query_wrapper(*args, **kwargs):
        model = args[0]
        model.reset()
        model.records = meth(*args, **kwargs)
        model.dataChanged.emit(QModelIndex(), QModelIndex())

    return query_wrapper


class TableModel(QAbstractTableModel):

    records = []
    session = session

    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)
        self.objects = self.session.query(self.schema)

    def columnCount(self, index=None):
        return len(self.schema.__table__.columns)

    def rowCount(self, index=None):
        return len(self.records)

    def data(self, index, role=Qt.DisplayRole):

        if role == Qt.DisplayRole:
            return self.data_display(index)

    def data_display(self, index):
        keys = self.schema.__table__.columns.keys()
        return getattr(self.records[index.row()], keys[index.column()])

    @query_method
    def query(self):
        return self.objects.all()
