from main_app import AlchemyBase
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class ParentTodo(AlchemyBase):

    __tablename__ = 'parent_todo'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)

    todos = relationship('Todo', backref='parent')


class Todo(AlchemyBase):

    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    task = Column(String(200), nullable=False)
    parent_id = Column(Integer, ForeignKey('parent_todo.id'))
    done = Column(Boolean, default=False)
