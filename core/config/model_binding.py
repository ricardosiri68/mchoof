import os
from PySide.QtCore import SIGNAL
from PySide.QtGui import QDataWidgetMapper
from .parser import ConfParser
from . import exceptions


class ModelBindingParser(ConfParser):

    def __init__(self, parent):
        conf_path = os.path.join(
            parent.__class__.__module__.split('.')[0],
            'conf',
            parent.models_binding_conf
        )
        self.parent = parent
        ConfParser.__init__(self, conf_path)
        self.bindModels()

    def bindModels(self):
        for binding in self.rootNode().childNodes:
            if binding.nodeName == 'model':
                self.bindModel(binding)

    def bindModel(self, binding):
        name = binding.getAttribute('name')

        if not name:
            raise exceptions.ModelBindingNameError(binding)

        try:
            model = getattr(self.parent, name, binding)
        except AttributeError:
            raise exceptions.ModelBindingViewAttributeError(
                self.parent,
                name,
                binding
            )

        if binding.hasAttribute('autoload'):

            querymethodname = binding.getAttribute('autoload')
            querymethodname = querymethodname if querymethodname else 'query'

            try:
                querymethod = getattr(model, querymethodname)
            except AttributeError:
                raise exceptions.ModelQuerymethodError(
                    self.parent,
                    model,
                    querymethod,
                    binding
                )

            querymethod()

        self.bindTables(model, binding.childNodes)
        self.bindMappers(model, binding.childNodes)

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

    def bindMappers(self, model, childnodes):
        for element in childnodes:
            if element.nodeName == 'mapper':
                self.bindMapper(model, element)

    def bindMapper(self, model, element):
        name = element.getAttribute('name')

        if not name:
            raise exceptions.ModelBindingNameError(element)

        mapper_name = 'mapper%s' % name.capitalize()

        if hasattr(self. parent, mapper_name):
            raise exceptions.ModelBindingMapperAttributeError(
                self.parent,
                name,
                element
            )

        setattr(self.parent, mapper_name, QDataWidgetMapper(self.parent))
        mapper = getattr(self.parent, mapper_name)
        mapper.setModel(model)

        self.mapFields(mapper, element.childNodes)
        self.configMapper(mapper, element)

    def mapFields(self, mapper, elements):
        model = mapper.model()

        for element in elements:

            if element.nodeName == 'map':

                self.mapField(mapper, model, element)

    def mapField(self, mapper, model, mapping):
        inputname = mapping.getAttribute('input')
        fieldname = mapping.getAttribute('field')

        if not inputname:

            raise exceptions.ModelBindingMapperAttributeError(
                self.parent,
                'input',
                mapping
            )

        if not fieldname:

            raise exceptions.ModelBindingMapperAttributeError(
                self.parent,
                'field',
                mapping
            )

        if not hasattr(self.parent, inputname):

            raise exceptions.ModelBindingViewAttributeError(
                self.parent,
                inputname,
                mapping
            )

        try:

            field_index = model.get_field_index(fieldname)

        except:

            raise exceptions.ModelBindingMappingFieldError(
                mapper,
                fieldname,
                mapping
            )

        widget = getattr(self.parent, inputname)
        mapper.addMapping(widget, field_index)

    def configMapper(self, mapper, element):

        if element.hasAttribute('selectorview'):
            selectorview = element.getAttribute('selectorview')

            if not selectorview:
                raise exceptions.ModelBindingMapperSelectorViewError(element)

            if not hasattr(self.parent, selectorview):
                raise exceptions.ModelBindingViewAttributeError(
                    self.parent,
                    selectorview
                )

            selectorview = getattr(self.parent, selectorview)
            selectorview.selectionModel().connect(
                SIGNAL("currentChanged(QModelIndex, QModelIndex)"),
                self.parent.connectMapper(mapper)
            )
