from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex
from mchoof.core import db_session


session = db_session.get_session()


class QueryMethod:

    @staticmethod
    def all(meth):

        def query_wrapper(*args, **kwargs):
            model = QueryMethod.before_wrapper(meth, args, kwargs)
            model.records = model.current_query.all()
            QueryMethod.after_wrapper(model)

        return query_wrapper

    @staticmethod
    def first(meth):

        def query_wrapper(*args, **kwargs):
            model = QueryMethod.before_wrapper(meth, args, kwargs)
            model.records = model.current_query.first()
            QueryMethod.after_wrapper(model)

        return query_wrapper

    @staticmethod
    def one(meth):

        def query_wrapper(*args, **kwargs):
            model = QueryMethod.before_wrapper(meth, args, kwargs)
            model.records = model.current_query.one()
            QueryMethod.after_wrapper(model)

        return query_wrapper

    @staticmethod
    def scalar(meth):

        def query_wrapper(*args, **kwargs):
            model = QueryMethod.before_wrapper(meth, args, kwargs)
            model.records = model.current_query.scalar()
            QueryMethod.after_wrapper(model)

        return query_wrapper

    @staticmethod
    def before_wrapper(meth, args, kwargs):
        model = args[0]
        model.reset()
        model.current_query = meth(*args, **kwargs)
        return model

    @staticmethod
    def after_wrapper(model_instance):
        model_instance.dataChanged.emit(QModelIndex(), QModelIndex())


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

    @QueryMethod.all
    def query(self):
        return self.objects
