import sys
import unittest
from PySide.QtCore import Qt
from PySide.QtGui import QBrush, QColor
from mchoof.core.application import HoofApp
from mchoof.config.table_model import TableModelConfig
from testapp.schema import ParentTodo


app = HoofApp(sys.argv)
app.initSettings()


class TestConfig(unittest.TestCase):

    def setUp(self):

        from testapp.models import TestModel
        self.model = TestModel()

    def test_add(self):

        self.model.add(
            0,
            task='test task',
            parent=ParentTodo(name='test parent')
        )

        self.assertEqual(len(self.model.records), 1)

    def test_remove(self):

        self.model.add(
            0,
            task='test task',
            parent=ParentTodo(name='test parent')
        )

        self.model.removeRow(0)

        self.assertEqual(len(self.model.records), 0)

    def test_data_task(self):

        self.model.add(
            0,
            task='test task',
            parent=ParentTodo(name='test parent')
        )

        task = self.model.data(
            self.model.index(0, 1)
        )

        self.assertEqual('test task', task)


class TestTodoModelField(unittest.TestCase):

    def setUp(self):

        from testapp.models import TestModel

        self.model = TestModel()
        self.model.model_config = 'id-hidden-model-conf.xml'

        TableModelConfig(self.model)

        self.model.add(
            0,
            task='test task',
            parent=ParentTodo(name='test parent')
        )

    def test_header_task(self):

        header = self.model.headerData(1, Qt.Horizontal)

        self.assertEqual('Tarea', header)

    def test_background_task(self):

        control = QBrush(QColor(255, 255, 255, 255))
        background = self.model.data(self.model.index(0, 1), Qt.BackgroundRole)

        self.assertEqual(control, background)

    def test_foreground_task(self):

        control = QBrush(QColor(204, 204, 204, 255))
        foreground = self.model.data(self.model.index(0, 1), Qt.ForegroundRole)

        self.assertEqual(control, foreground)


if __name__ == '__main__':

    unittest.main()
