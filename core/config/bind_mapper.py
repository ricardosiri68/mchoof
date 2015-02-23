from PySide.QtCore import SIGNAL
from PySide.QtGui import QDataWidgetMapper
from . import exceptions


class ModelBindMapperParser:

    def __init__(self, parser_parent):
        self.parser_parent = parser_parent
        self.parent = self.parser_parent.parent

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
                    selectorview,
                    element
                )

            selectorview = getattr(self.parent, selectorview)

            selectorview.selectionModel().connect(
                SIGNAL("currentChanged(QModelIndex, QModelIndex)"),
                self.parent.connectMapper(mapper)
            )
