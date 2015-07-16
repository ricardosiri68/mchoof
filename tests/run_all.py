import unittest
from colour_runner import runner

from model_config import TestTableModelConfErrors, TestTableModelConf
from table_model_integration_tests import TestConfig, TestTodoModelField


if __name__ == '__main__':

    unittest.main(testRunner=runner.ColourTextTestRunner, verbosity=2)
