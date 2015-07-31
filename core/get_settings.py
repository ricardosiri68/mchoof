app_settings = __import__('main_app.settings')


def get_database_url():

    return app_settings.settings.DATABASE_URL


def get_serial_port():

    return app_settings.settings.SERIAL_PORT
