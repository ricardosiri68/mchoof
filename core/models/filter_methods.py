from PySide.QtCore import QModelIndex


class FilterMethod:

    @staticmethod
    def group(meth):

        def filter_wrapper(*args, **kwargs):
            model = FilterMethod.before_wrapper(meth, args, kwargs)

            if model.filters_list:
                model.records = model\
                    .objects\
                    .filter(*model.filters_list.values())\
                    .all()
            else:
                model.refresh()

            FilterMethod.after_wrapper(model)

            return model.records
        return filter_wrapper

    @staticmethod
    def before_wrapper(meth, args, kwargs):
        model = args[0]
        filter = meth(*args, **kwargs)

        if not filter is None:
            model.filters_list[meth.func_name] = filter
            model.reset()
        elif meth.func_name in model.filters_list:
            del model.filters_list[meth.func_name]

        return model

    @staticmethod
    def after_wrapper(model):
        model.dataChanged.emit(QModelIndex(), QModelIndex())
