from . import exceptions
import sys
import os
import shutil


class Command:

    def __init__(self, project_path):

        self.project_path = project_path

        try:
            command = self.commands[sys.argv[1]]
        except KeyError:
            raise exceptions.CommandNameError(sys.argv[1])

        command(self, *sys.argv[2:])

    def start_project(self, *args):

        if not args:
            raise exceptions.CommandArgumentError('startproject', 1, 0)

        project_name, = args
        StartProject(self.project_path, project_name)

    def start_app(self, *args):

        if not args:
            raise exceptions.CommandArgumentError('startapp', 1, 0)

        app_name, = args
        StartApp(self.project_path, app_name)

    def alembic_env(self, *args):

        alembic_path, = args if args else ('alembic',)
        AlembicEnv(self.project_path, alembic_path)

    commands = {
        'startproject': start_project,
        'startapp': start_app,
        'alembicenv': alembic_env
    }


class StartProject:

    main_files = (
        'resource.qrc', 'resource_rc.py', 'main.py', 'setup.py'
    )

    main_app_files = (
        'settings.py', 'local_settings.py', 'views.py', '__init__.py',
        os.path.join('conf', 'menubar.xml')
    )

    resource_files = 'style.css',
    resource_icons = [
        'add.png', 'bg.png', 'bullet-green.png', 'bullet-red.png',
        'checked.png', 'config.png', 'delete.png', 'down-arrow-hover.png',
        'down-arrow-pressed.png', 'down-arrow.png', 'edit.png', 'icon.png',
        'save.png', 'seach.png', 'unchecked.png', 'up-arrow-hover.png',
        'up-arrow-pressed.png', 'up-arrow.png'
    ]
    templates_files = 'mainFrame.ui', 'mainWindow.ui'
    database_dirs = 'migrations', 'initdata', 'extra', 'dumpschema'

    def __init__(self, path, name):

        self.__path = path  # ruta donde se iniciara el proyecto
        self.__name = name  # nombre del proyecto

        # MAKE DIRS
        self.make_main_dir()
        self.make_templates_dir()
        self.make_resources_dir()

        # COPY DIRS
        self.copy_main_files()
        self.make_main_app()
        self.copy_resource_files()
        self.copy_templates_files()

    def make_main_app(self):

        main_app_fs = os.path.join(self.get_project_fs_dir(), 'main_app')
        startapp = StartApp(self.__main_path, 'main_app')
        app_path = startapp.app_path()

        for app_file in self.main_app_files:
            shutil.copy2(
                os.path.join(main_app_fs, app_file),
                os.path.join(app_path, app_file)
            )

    def make_main_dir(self):

        # ruta del proyecto
        self.__main_path = os.path.join(self.__path, self.__name)
        if os.path.isdir(self.__main_path):
            raise exceptions.ProjectAlreadyExistError(self.__name, self.__path)

        os.mkdir(self.__main_path)

    def get_project_fs_dir(self):

        module_dir = os.path.dirname(__file__)
        return os.path.join(module_dir, 'project_fs')

    def copy_main_files(self):

        project_fs = self.get_project_fs_dir()

        for main_file in self.main_files:
            shutil.copy2(
                os.path.join(project_fs, main_file),
                os.path.join(self.__main_path, main_file)
            )

    def copy_resource_files(self):

        resources_fs = os.path.join(self.get_project_fs_dir(), 'resources')
        project_resource = os.path.join(self.__main_path, 'resources')

        resources_icons_fs = os.path.join(resources_fs, 'icons')
        project_icons = os.path.join(project_resource, 'icons')

        for resource_file in self.resource_files:
            shutil.copy2(
                os.path.join(resources_fs, resource_file),
                os.path.join(project_resource, resource_file)
            )

        for resource_icon in self.resource_icons:
            shutil.copy2(
                os.path.join(resources_icons_fs, resource_icon),
                os.path.join(project_icons, resource_icon)
            )

    def copy_templates_files(self):

        templates_fs = os.path.join(
            self.get_project_fs_dir(),
            'templates',
            'main_app'
        )
        project_templates = os.path.join(self.__templates_path, 'main_app')
        os.mkdir(project_templates)

        for template_file in self.templates_files:
            shutil.copy2(
                os.path.join(templates_fs, template_file),
                os.path.join(project_templates, template_file)
            )

    def make_templates_dir(self):

        self.__templates_path = os.path.join(self.__main_path, 'templates')
        os.mkdir(self.__templates_path)

    def make_resources_dir(self):

        resources_path = os.path.join(self.__main_path, 'resources')
        resources_icons = os.path.join(resources_path, 'icons')
        os.mkdir(resources_path)
        os.mkdir(resources_icons)


class StartApp:

    app_fs_dir = 'app_fs'
    app_files = '__init__.py', 'schema.py', 'models.py', 'views.py'

    def __init__(self, path, name):

        self.__name = name
        self.__path = path
        self.__app_path = os.path.join(path, name)
        self.make_app_dir()
        self.__copy_files()

    def make_app_dir(self):

        view_conf_path = os.path.join(self.__app_path, 'conf')

        if os.path.isdir(self.__app_path):
            raise exceptions.AppPackageAlreadyExistError(
                self.__name,
                self.__path
            )

        os.mkdir(self.__app_path)
        os.mkdir(view_conf_path)

    def app_path(self):

        return self.__app_path

    def get_app_fs_dir(self):

        module_dir = os.path.dirname(__file__)
        return os.path.join(module_dir, self.app_fs_dir)

    def __copy_files(self):

        app_fs = self.get_app_fs_dir()

        for app_file in self.app_files:
            shutil.copy2(
                os.path.join(app_fs, app_file),
                os.path.join(self.__app_path, app_file)
            )


class AlembicEnv:

    env_files = ('env.py', )
    alembic_fs = 'alembic_fs'

    def __init__(self, project_path, alembic_path):

        self.alembic_path = os.path.join(project_path, alembic_path)

        if not os.path.isdir(self.alembic_path):
            raise exceptions.WrongPathForGenerateAlembicEnvError(
                self.alembic_path
            )

        self.copy_env()

    def copy_env(self):

        alembic_fs = self.get_alembic_fs_dir()

        for env_file in self.env_files:
            shutil.copy2(
                os.path.join(alembic_fs, env_file),
                os.path.join(self.alembic_path, env_file)
            )

    def get_alembic_fs_dir(self):

        module_dir = os.path.dirname(__file__)
        return os.path.join(module_dir, self.alembic_fs)
