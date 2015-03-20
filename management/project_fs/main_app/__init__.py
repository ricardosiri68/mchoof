from sqlalchemy.ext.declarative import declarative_base
from settings import DATABASE_URL

if DATABASE_URL:
    AlchemyBase = declarative_base()
