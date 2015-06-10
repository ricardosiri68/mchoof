import os
import unittest
from PySide.QtCore import Qt
from mchoof.config.table_model import TableModelConfig
from mchoof.config.exceptions import model_config_exceptions as excepts
from fixtures.table_models import BadTestModel, GoodTestModel


class TestTableModelConfErrors(unittest.TestCase):

    dir_prefix = 'bad-model-confs'

    def __dir_prefix(self, filename):

        return os.path.join(self.dir_prefix, filename)

    def setUp(self):

        self.model = BadTestModel()

    def test_wrong_config_path(self):
        '''ails when the model not has a valid config path'''

        self.model.model_config = self.__dir_prefix('wrong-conf-path.xml')
        self.assertRaises(
            IOError,
            TableModelConfig,
            self.model
        )

    def test_not_config(self):
        '''fails if the config is not'''

        self.model.model_config = self.__dir_prefix('no-config-model.xml')

        self.assertRaises(
            excepts.ModelConfNotFound,
            TableModelConfig,
            self.model
        )

    def test_not_name_on_config(self):
        '''the model element config has no name when is parsed'''

        self.model.model_config = self.__dir_prefix('no-name-conf-model.xml')

        self.assertRaises(
            excepts.ModelConfigNameError,
            TableModelConfig,
            self.model
        )

    def test_fieldname_error(self):
        '''the field element has no name'''

        self.model.model_config = self.__dir_prefix(
            'no-name-field-confmodel.xml'
        )

        self.assertRaises(
            excepts.ModelConfigFieldnameError,
            TableModelConfig,
            self.model
        )

    def test_wrong_fieldname_error(self):
        '''the field "name" atribute has a wrong value who doesn't exist on it
        schema'''

        self.model.model_config = self.__dir_prefix(
            'wrong-name-field-confmodel.xml'
        )

        self.assertRaises(
            excepts.ModelConfigNotHasFieldError,
            TableModelConfig,
            self.model
        )

    def test_empty_header_error(self):
        '''the header attribute is empty'''

        self.model.model_config = self.__dir_prefix('no-header-attr-field.xml')

        self.assertRaises(
            excepts.ModelConfigHeaderError,
            TableModelConfig,
            self.model
        )

    def test_wrong_background_error(self):
        '''the hexcolor of de background attribute'''

        self.model.model_config = self.__dir_prefix(
            'wrong-background-model.xml'
        )

        self.assertRaises(
            excepts.ModelConfigHexColorError,
            TableModelConfig,
            self.model
        )

    def test_wrong_foreground_error(self):
        '''the hexcolor of de foreground attribute'''

        self.model.model_config = self.__dir_prefix(
            'wrong-foreground-model.xml'
        )

        self.assertRaises(
            excepts.ModelConfigHexColorError,
            TableModelConfig,
            self.model
        )

    def test_wrong_align_error(self):
        '''must fails if is the value is not: align, right, center o justify'''

        self.model.model_config = self.__dir_prefix(
            'wrong-align-attr-field-model.xml'
        )

        self.assertRaises(
            excepts.ModelConfigAlignValueError,
            TableModelConfig,
            self.model
        )

    def test_empty_align_error(self):
        '''must be raise a empti align attr error'''

        self.model.model_config = self.__dir_prefix(
            'empty-align-attr-field-model.xml'
        )

        self.assertRaises(
            excepts.ModelConfigAlignError,
            TableModelConfig,
            self.model
        )

    def test_wrong_relatedfield_error(self):
        '''must be raise a wrong related field error'''

        self.model.model_config = self.__dir_prefix(
            'wrong-relatedfield-attr-model.xml'
        )

        self.assertRaises(
            excepts.ModelConfigRelatedFieldError,
            TableModelConfig,
            self.model
        )

    def test_wrong_relatedfield_attr_error(self):
        '''must be raise a wrong related field attr error'''

        self.model.model_config = self.__dir_prefix(
            'wrong-relatedfield-attr-2-model.xml'
        )

        self.assertRaises(
            excepts.ModelConfigRelatedAttributeError,
            TableModelConfig,
            self.model
        )


class TestTableModelConf(unittest.TestCase):

    dir_prefix = 'good-model-confs'

    def __dir_prefix(self, filename):

        return os.path.join(self.dir_prefix, filename)

    def setUp(self):

        self.model = GoodTestModel()

    def test_config_path(self):

        self.model.model_config = self.__dir_prefix('some-path-config.xml')

        table_model_config = TableModelConfig(self.model)

        self.assertEqual(
            'fixtures/conf/good-model-confs/some-path-config.xml',
            table_model_config.filename()
        )


if __name__ == '__main__':

    unittest.main()
