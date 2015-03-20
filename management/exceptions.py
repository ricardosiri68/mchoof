class CommandNameError(Exception):

    def __init__(self, command_name):
        message = "The command {command_name} doesn't exsist".format(
            command_name=command_name
        )
        super(CommandNameError, self).__init__(message)


class CommandArgumentError(Exception):

    def __init__(self, command_name, cant, given):
        message = '{command_name} takes {cant} arguments ({given} given)'.\
            format(
                command_name=command_name,
                cant=cant,
                given=given
            )
        super(CommandArgumentError, self).__init__(message)


class ProjectAlreadyExistError(Exception):

    def __init__(self, project_name, path):
        message = 'The {project_name} dir already exist on {path}'.format(
            project_name=project_name,
            path=path
        )
        super(ProjectAlreadyExistError, self).__init__(message)


class AppPackageAlreadyExistError(Exception):

    def __init__(self, app_name, project_path):
        message = 'The {app_name} dir already exist on {project_path}'.format(
            app_name=app_name,
            project_path=project_path
        )
        super(AppPackageAlreadyExistError, self).__init__(message)


class WrongPathForGenerateAlembicEnvError(Exception):

    def __init__(self, path):
        message = 'the path {path} is not a directory or doesn\'t exist'\
            .format(path=path)
        super(WrongPathForGenerateAlembicEnvError, self).__init__(message)
