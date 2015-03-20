class FieldDoesntExist(Exception):

    def __init__(self, schema, fieldname):
        message = 'The Schema {class_name} don\'t has the field {fieldname}'\
            .format(
                class_name=schema.__class__.__name__,
                fieldname=fieldname
            )
        super(FieldDoesntExist, self).__init__(message)


class ModelIndexError(Exception):

    def __init__(self, model, index):
        message = 'The row index {index} doesn\'t exist on {model_classname}\
            records'.format(
            index=index,
            model_classname=model.__class__.__name__
        )
        super(ModelIndexError, self).__init__(message)


class ModelSetDataError(Exception):

    def __init__(self, model, index, value):

        message = 'The model {model_classnaame} can\'t set the value {value}\
        on the index {row}:{column}'.format(
            model_classname=model.__class__.__name__,
            value=value,
            row=index.row(),
            column=index.column()
        )
        super(ModelSetDataError, self).__init__(message)
