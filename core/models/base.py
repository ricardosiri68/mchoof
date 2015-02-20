from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex
from mchoof.core import db_session


session = db_session.get_session()


class QueryMethod:

    @staticmethod
    def all(meth):

        def query_wrapper(*args, **kwargs):
            model = QueryMethod.before_wrapper(meth, args, kwargs)
            model.records = meth(*args, **kwargs).all()
            QueryMethod.after_wrapper(model)

            return model.records

        return query_wrapper

    @staticmethod
    def first(meth):

        def query_wrapper(*args, **kwargs):
            model = QueryMethod.before_wrapper(meth, args, kwargs)
            result = meth(*args, **kwargs).first()
            model.records = [result]
            QueryMethod.after_wrapper(model)

            return result

        return query_wrapper

    @staticmethod
    def one(meth):

        def query_wrapper(*args, **kwargs):
            model = QueryMethod.before_wrapper(meth, args, kwargs)
            result = meth(*args, **kwargs).one()
            model.records = [result]
            QueryMethod.after_wrapper(model)

            return result

        return query_wrapper

    @staticmethod
    def scalar(meth):

        def query_wrapper(*args, **kwargs):
            model = QueryMethod.before_wrapper(meth, args, kwargs)
            result = meth(*args, **kwargs).scalar()
            model.records = [result]
            QueryMethod.after_wrapper(model)

            return result

        return query_wrapper

    @staticmethod
    def before_wrapper(meth, args, kwargs):
        model = args[0]
        model.reset()

        model.current_query = {
            'method': meth,
            'args': args,
            'kwargs': kwargs
        }

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

    def refresh(self):
        self.current_query['method'](
            *self.current_query['args'],
            **self.current_query['kwargs']
        )

    @QueryMethod.all
    def query(self):
        return self.objects
