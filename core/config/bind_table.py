from PySide.QtCore import SIGNAL
from . import exceptions


class ModelBindTableParser:

    def __init__(self, parser_parent):
        self.parser_parent = parser_parent
        self.parent = parser_parent.parent

    def bindTables(self, model, childnodes):
        for element in childnodes:

            if element.nodeName == 'table':

                self.bindTable(model, element)

    def bindTable(self, model, element):

        name = element.getAttribute('name')

        if not name:
            raise exceptions.ModelBindingNameError(element)

        try:
            table = getattr(self.parent, name)

        except AttributeError:

            raise exceptions.ModelBindingViewAttributeError(
                self.parent,
                name,
                element
            )

        table.setModel(model)

        self.configTableFields(table, element.childNodes)

    def configTableFields(self, table, fields_elements):
        for field_element in fields_elements:
            if field_element.nodeName == 'field':
                self.configTableField(table, field_element)

    def configTableField(self, table, field_element):
        model = table.model()
        name = field_element.getAttribute('name')
        hidden = field_element.hasAttribute('hidden')
        width = field_element.getAttribute('width')

        if not name:
            raise exceptions.ModelBindingNameError(field_element)

        try:
            field_index = model.get_field_index(name)
        except:
            raise exceptions.ModelBindingTableFieldnameError(
                self.parent,
                model,
                name,
                field_element
            )

        table.setColumnHidden(field_index, hidden)

        if width:

            if width != "auto":

                try:
                    width = int(width)
                except ValueError:
                    raise exceptions.ModelBindingTableWidthFieldError(
                        self.parent,
                        name,
                        field_element
                    )

                table.setColumnWidth(field_index, width)

            else:

                horizontal_header = table.horizontalHeader()
                horizontal_header.setResizeMode(
                    field_index,
                    horizontal_header.Stretch
                )
