from PySide.QtCore import QModelIndex
from .tree_node import Node


class QueryMethod:

    @staticmethod
    def all(meth):

        def query_wrapper(*args, **kwargs):
            model = QueryMethod.before_wrapper(meth, args, kwargs)

            model.records = model.current_query['query'].all()

            if 'TreeModel' in [mro.__name__ for mro in model.__class__.__mro__]:

                model.records = model.current_query['query'].all()

                for record in model.records:

                    node = Node(record, model.rootNode)

                    for childrecord in getattr(record, model.childnodes_attr):

                        Node(childrecord, node)

            QueryMethod.after_wrapper(model)

            return model.records

        return query_wrapper

    @staticmethod
    def first(meth):

        def query_wrapper(*args, **kwargs):
            model = QueryMethod.before_wrapper(meth, args, kwargs)
            result = model.current_query['query'].first()
            model.records = [result]
            QueryMethod.after_wrapper(model)

            return result

        return query_wrapper

    @staticmethod
    def one(meth):

        def query_wrapper(*args, **kwargs):
            model = QueryMethod.before_wrapper(meth, args, kwargs)
            result = model.current_query['query'].one()
            model.records = [result]
            QueryMethod.after_wrapper(model)

            return result

        return query_wrapper

    @staticmethod
    def scalar(meth):

        def query_wrapper(*args, **kwargs):
            model = QueryMethod.before_wrapper(meth, args, kwargs)
            result = model.current_query['query'].scalar()
            model.records = [result]
            QueryMethod.after_wrapper(model)

            return result

        return query_wrapper

    @staticmethod
    def before_wrapper(meth, args, kwargs):
        model = args[0]
        model.reset()

        model.current_query = {
            'query': meth(*args, **kwargs),
            'method': meth.func_name,
            'args': args[1:],
            'kwargs': kwargs
        }

        return model

    @staticmethod
    def after_wrapper(model_instance):
        model_instance.dataChanged.emit(QModelIndex(), QModelIndex())


