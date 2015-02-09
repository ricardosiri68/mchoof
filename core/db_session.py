import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app_settings = __import__(os.environ.get('MCHOOF_SETTINGS'))


def get_session():

    engine = create_engine(app_settings.settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()
