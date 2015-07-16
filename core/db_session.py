import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app_settings = __import__('main_app.settings')


def get_session():

    if app_settings.settings.DATABASE_URL:
        engine = create_engine(app_settings.settings.DATABASE_URL)
        Session = sessionmaker(bind=engine, autoflush=False)
        return Session()
