import sys
import unittest
from mchoof.core.application import HoofApp
from testapp.models import TestTableModel


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.app = HoofApp(sys.argv)
        self.app.initSettings()
        self.model = TestTableModel()

    def test_model(self):

        pass


if __name__ == '__main__':

    unittest.main()
