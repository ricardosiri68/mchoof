from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .get_settings import get_database_url


def get_session():

    database_url = get_database_url()

    if database_url:

        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine, autoflush=False)
        return Session()
