from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex
from mchoof.core import db_session
from mchoof.core.models import exceptions


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
        elif role == Qt.EditRole:
            return self.data_edit(index)

    def data_display(self, index):

        keys = self.schema.__table__.columns.keys()
        return getattr(self.records[index.row()], keys[index.column()])

    def data_edit(self, index):
        return self.data_display(index)

    def refresh(self):

        self.current_query['method'](
            *self.current_query['args'],
            **self.current_query['kwargs']
        )

    def get_field_index(self, fieldname):

        try:
            return self.schema.__table__.columns.keys().index(fieldname)

        except ValueError:
            raise exceptions.FieldDoesntExist(self.schema, fieldname)

    @QueryMethod.all
    def query(self):

        return self.objects
