import os
from PySide.QtCore import Qt
from PySide.QtGui import QBrush, QColor
from mchoof.core import utils
from .parser import ConfParser
from .exceptions.model_config_exceptions import (
    ModelConfigNameError,
    ModelConfNotFound,
    ModelConfigFieldnameError,
    ModelConfigNotHasFieldError,
    ModelConfigHeaderError,
    ModelConfigAlignError,
    ModelConfigAlignValueError,
    ModelConfigHexColorError,
    ModelConfigRelatedFieldError,
    ModelConfigRelatedAttributeError,
)


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

        self.model = model

        ConfParser.__init__(self, conf_path)

        for model_element in self.rootNode().childNodes:

            if model_element.nodeName == 'model':

                name = model_element.getAttribute('name')

                if not name:
                    raise ModelConfigNameError(
                        self.model,
                        model_element
                    )

                if name == self.model.__class__.__name__:
                    self.model_element = model_element

        if not self.model_element:
            raise ModelConfNotFound(self.model)

        self.appendFields()
        self.configFields()

    def appendFields(self):

        for childnode in self.model_element.childNodes:

            if childnode.nodeName == 'append':

                self.appendField(childnode)

    def appendField(self, append_element):

        SchemaClass = self.model.schema

        name = append_element.getAttribute('name')

        if not name:

            raise ModelConfigNameError(
                self.model,
                append_element
            )

        # if not hasattr(SchemaClass, name):

        try:

            getattr(SchemaClass, name)

        except:

            raise ModelConfigFieldnameError(
                self.model,
                append_element
            )

        self.model.appends.append(name)

        self.configField(append_element)

    def configFields(self):

        for childnode in self.model_element.childNodes:
            if childnode.nodeName == 'field':
                self.configField(childnode)

    def configField(self, field_element):

        name = field_element.getAttribute('name')

        if not name:

            raise ModelConfigFieldnameError(
                self.model,
                field_element
            )

        if not name in self.model.field_keys:

            raise ModelConfigNotHasFieldError(
                self.model,
                name,
                field_element
            )

        index_column = self.model.field_keys.index(name)

        self.setHeader(field_element, index_column)
        self.setAlign(field_element, index_column)
        self.setBackground(field_element, index_column)
        self.setForeground(field_element, index_column)
        self.setRelatedField(field_element, index_column)

    def setHeader(self, field_element, index_column):

        header = field_element.getAttribute('header')

        if not header and field_element.hasAttribute('header'):

            raise ModelConfigHeaderError(self.model, field_element)

        elif header:

            if field_element.nodeName == 'append':

                self.model.headers.append(header)

            else:

                self.model.headers[index_column] = header

        if not header and field_element.nodeName == 'append':

            self.models.headers.append(field_element.getAttibute('name'))

    def setAlign(self, field_element, index_column):

        align = field_element.getAttribute('align')

        if field_element.hasAttribute('align'):

            if not align:
                raise ModelConfigAlignError(
                    self.model,
                    field_element
                )

            if not align in self.aligments_mapping.keys():
                raise ModelConfigAlignValueError(
                    self.model,
                    field_element
                )

            alignament = int(
                Qt.AlignVCenter | self.aligments_mapping[align]
            )

            if field_element.nodeName == 'append':

                self.model.aligments.append(alignament)

            else:

                self.model.aligments[index_column] = alignament

        if not align and field_element.nodeName == 'append':

            self.model.aligments.append(int(Qt.AlignVCenter | Qt.AlignLeft))

    def setBackground(self, field_element, index_column):

        background = field_element.getAttribute('background')

        if field_element.hasAttribute('background'):

            try:

                colortuple = utils.hex_to_rgb(background)

            except ValueError:

                raise ModelConfigHexColorError(
                    self.model,
                    'background',
                    background,
                    field_element
                )

            background_color = QBrush(QColor(*colortuple))

            if field_element.nodeName == 'append':

                print 'append background', background
                self.model.backgrounds.append(background_color)

            else:

                self.model.backgrounds[index_column] = background_color

        elif field_element.nodeName == 'append':

            self.model.backgrounds.append(None)

    def setForeground(self, field_element, index_column):

        foreground = field_element.getAttribute('foreground')

        if field_element.hasAttribute('foreground'):

            try:

                colortuple = utils.hex_to_rgb(foreground)

            except ValueError:

                raise ModelConfigHexColorError(
                    self.model,
                    'foreground',
                    foreground,
                    field_element
                )

            foreground_color = QBrush(QColor(*colortuple))

            if field_element.nodeName == 'append':

                self.model.foregrounds.append(foreground_color)

            else:

                self.model.foregrounds[index_column] = foreground_color

        elif field_element.nodeName == 'append':

            self.model.foregrounds.append(None)

    def setRelatedField(self, field_element, index_column):

        relatedfield = field_element.getAttribute('relatedfield')

        if not relatedfield:

            return

        schema = self.model.schema()

        try:

            related_attr, field_attr = relatedfield.split(':')

        except ValueError:

            raise ModelConfigRelatedFieldError(
                self.model,
                field_element
            )

        if not hasattr(schema, related_attr):

            raise ModelConfigRelatedAttributeError(
                self.model,
                related_attr,
                field_element
            )

        self.model.related_fields[index_column] = (
            related_attr,
            field_attr,
            field_element
        )

        del schema
