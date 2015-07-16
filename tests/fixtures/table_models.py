from PySide.QtCore import Qt


class MockRelatedField:

    def __init__(self):

        self.name = 'name_test'


class MockSchema:

    def __init__(self):

        self.id = 1
        self.task = ''
        self.parent_id = 1

        self.parent = MockRelatedField()


class BadTestModel:

    schema = MockSchema

    def __init__(self):

        self.headers = self.field_keys = ['id', 'task', 'parent_id', 'done']
        self.aligments = len(self.headers) * [
            int(Qt.AlignVCenter | Qt.AlignLeft)
        ]

        self.backgrounds = len(self.headers) * [None]
        self.foregrounds = len(self.headers) * [None]
        self.related_fields = {}


class GoodTestModel:

    schema = MockSchema

    def __init__(self):

        self.headers = self.field_keys = ['id', 'task', 'parent_id', 'done']
        self.aligments = len(self.headers) * [
            int(Qt.AlignVCenter | Qt.AlignLeft)
        ]

        self.backgrounds = len(self.headers) * [None]
        self.foregrounds = len(self.headers) * [None]
        self.related_fields = {}
