from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_session_class(database_url):

    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return Session()
