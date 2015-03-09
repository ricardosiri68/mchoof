from PySide.QtCore import QModelIndex


class QueryMethod:

    @staticmethod
    def all(meth):

        def query_wrapper(*args, **kwargs):
            model = QueryMethod.before_wrapper(meth, args, kwargs)
            model.records = model.current_query['query'].all()
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


