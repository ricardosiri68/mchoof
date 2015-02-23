class FieldDoesntExist(Exception):

    def __init__(self, schema, fieldname):
        message = 'The Schema {class_name} don\'t has the field {fieldname}'\
            .format(
                class_name=schema.__class__.__name__,
                fieldname=fieldname
            )
        super(NotFieldDoesntExist, self).__init__(message)
