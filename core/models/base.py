from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex
from mchoof.core import db_session
from mchoof.core.models import exceptions
from mchoof.core.config.table_model import TableModelConfig


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
            'method': meth.func_name,
            'args': args[1:],
            'kwargs': kwargs
        }

        return model

    @staticmethod
    def after_wrapper(model_instance):
        model_instance.dataChanged.emit(QModelIndex(), QModelIndex())


class TableModel(QAbstractTableModel):

    records = []
    session = session
    model_config = None

    def __init__(self, parent=None):

        super(TableModel, self).__init__(parent)

        self.headers = self.schema.__table__.columns.keys()
        self.aligments = [Qt.AlignLeft for k in self.headers]

        if self.model_config:
            TableModelConfig(self)

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

        elif role == Qt.TextAlignmentRole:
            return self.data_textalign(index)

    def data_display(self, index):

        keys = self.schema.__table__.columns.keys()
        return getattr(self.records[index.row()], keys[index.column()])

    def data_edit(self, index):

        return self.data_display(index)

    def data_textalign(self, index):

        return self.aligments[index.column()]

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

    @QueryMethod.all
    def query(self):

        return self.objects

    def add(self, **kwargs):

        self.session.add(self.schema(**kwargs))

    def commit(self):

        self.session.commit()
        self.refresh()
