from mchoof.models.base import TableModel
from .schema import Todo, ParentTodo


class ParentModel(TableModel):

    schema = ParentTodo


class TestModel(TableModel):

    schema = Todo
