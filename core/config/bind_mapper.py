from ..views.mappers import MhDataMapper
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

        if hasattr(self. parent, name):

            raise exceptions.ModelBindingMapperAttributeError(
                self.parent,
                name,
                element
            )

        setattr(self.parent, name, MhDataMapper(self.parent))
        mapper = getattr(self.parent, name)
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

        selectorview = element.getAttribute('selectorview')
        autosubmit = element.hasAttribute('autosubmit')

        commiter = element.getAttribute('commiter')
        accept = element.getAttribute('accept')
        reject = element.getAttribute('reject')
        done = element.getAttribute('done')

        if element.hasAttribute('selectorview'):
            self.bindSelectorView(mapper, selectorview, element)

        if element.hasAttribute('commiter') and (accept or reject or done):
            self.bindCommiter(mapper, commiter, accept, reject, done, element)

        if autosubmit:
            mapper.setSubmitPolicy(mapper.AutoSubmit)

    def bindSelectorView(self, mapper, selectorview, element):

        if not selectorview:
            raise exceptions.ModelBindingMapperSelectorViewError(element)

        if not hasattr(self.parent, selectorview):
            raise exceptions.ModelBindingViewAttributeError(
                self.parent,
                selectorview,
                element
            )

        selectorview = getattr(self.parent, selectorview)
        mapper.setSelectorView(selectorview)

    def bindCommiter(self, mapper, commiter, accept, reject, done, element):

        if not hasattr(self.parent, commiter):

            raise exceptions.ViewAttributeError(self.parent, commiter, element)

        commiter_attr = getattr(self.parent, commiter)

        if commiter_attr.__class__.__name__ != 'QDialogButtonBox':

            raise exceptions.ModelBindingMappingCommiterError(
                self.parent,
                commiter,
                element
            )

        actions = {
            'accepted': accept,
            'rejected': reject,
            'clicked': done,
        }

        for key, value in actions.items():

            if not value:
                break

            if hasattr(self.parent, value):

                action = getattr(self.parent, value)
                getattr(commiter_attr, key).connect(action)

            else:

                raise exceptions.ViewAttributeError(
                    self.parent,
                    value,
                    element
                )
