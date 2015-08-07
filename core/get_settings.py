import os
app = __import__('main_app.settings')


def get_database_url():

    return app.settings.DATABASE_URL


def get_serial_port():

    return app.settings.SERIAL_PORT


def get_printer_templates_dir():

    return os.path.join(
        app.settings.BASE_DIR,
        app.settings.PRINTER_TEMPLATE_DIR
    )
