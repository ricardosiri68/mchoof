import os
from PySide.QtCore import Qt
from PySide.QtGui import QBrush, QColor
from mchoof.core import utils
from .parser import ConfParser
from . import exceptions


class TableModelConfig(ConfParser):

    model_element = None
    aligments_mapping = {
        'left': Qt.AlignLeft,
        'right': Qt.AlignRight,
        'center': Qt.AlignHCenter,
        'justify': Qt.AlignJustify
    }

    def __init__(self, model):

        conf_path = os.path.join(
            model.__class__.__module__.split('.')[0],
            'conf',
            model.model_config
        )

        self.fieldnames = model.schema.__table__.columns.keys()
        self.model = model

        ConfParser.__init__(self, conf_path)

        for model_element in self.rootNode().childNodes:

            if model_element.nodeName == 'model':

                name = model_element.getAttribute('name')

                if not name:
                    raise exceptions.ModelConfigNameError(
                        self.parent,
                        model_element
                    )

                if name == self.model.__class__.__name__:
                    self.model_element = model_element

        if not self.model_element:
            raise exceptions.ModelConfNotFound(self.model)

        self.configFields()

    def configFields(self):
        for childnode in self.model_element.childNodes:
            if childnode.nodeName == 'field':
                self.configField(childnode)

    def configField(self, field_element):
        name = field_element.getAttribute('name')
        header = field_element.getAttribute('header')
        align = field_element.getAttribute('align')
        background = field_element.getAttribute('background')
        foreground = field_element.getAttribute('foreground')
        relatedfield = field_element.getAttribute('relatedfield')

        if not name:
            raise exceptions.ModelConfigFieldnameError(
                self.model,
                field_element
            )

        if not name in self.fieldnames:
            raise exceptions.ModelConfigNotHasFieldError(
                self.model,
                name,
                field_element
            )

        if not header and field_element.hasAttribute('header'):
            raise exceptions.ModelConfigHeaderError(self.model, field_element)

        index_column = self.fieldnames.index(name)

        if field_element.hasAttribute('background'):
            try:
                colortuple = utils.hex_to_rgb(background)
            except ValueError:
                raise exceptions.ModelConfigHexColorError(
                    self.model,
                    'background',
                    background,
                    field_element
                )
            self.model.backgrounds[index_column] = QBrush(QColor(*colortuple))

        if field_element.hasAttribute('foreground'):
            try:
                colortuple = utils.hex_to_rgb(foreground)
            except ValueError:
                raise exceptions.ModelConfigHexColorError(
                    self.model,
                    'foreground',
                    foreground,
                    field_element
                )
            self.model.foregrounds[index_column] = QBrush(QColor(*colortuple))

        self.model.headers[index_column] = header

        if field_element.hasAttribute('align'):

            if not align:
                raise exceptions.ModelConfigAlingError(
                    self.model,
                    field_element
                )

            if not align in self.aligments_mapping.keys():
                raise exceptions.ModelConfigAlignValueError(
                    self.model,
                    field_element
                )

            self.model.aligments[index_column] = int(
                Qt.AlignVCenter | self.aligments_mapping[align]
            )

        if relatedfield:
            self.setRelatedField(self.model, index_column, relatedfield)

    def setRelatedField(self, model, index_column, relatedfield):

        self.model.related_fields[index_column] = relatedfield.split(':')
