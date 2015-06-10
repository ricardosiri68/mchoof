from main_app import AlchemyBase
from sqlalchemy import Column, Integer, String


class Todo(AlchemyBase):

    __tablename__ = 'test_table'

    id = Column(Integer, primary_key=True)
    task = Column(String,)
