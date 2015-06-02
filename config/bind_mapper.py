from ..views.mappers import MhDataMapper
from .exceptions.view_exceptions import ViewAttributeError
from .exceptions.model_binding_exceptions import (
    ModelBindingNameError,
    ModelBindingMapperAttributeError,
    ModelBindingViewAttributeError,
    ModelBindingMappingFieldError,
    ModelBindingMapperSelectorViewError,
    ModelBindingMappingCommiterError
)


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

            raise ModelBindingNameError(element)

        if hasattr(self. parent, name):

            raise ModelBindingMapperAttributeError(
                self.parent,
                name,
                element
            )

        mapper = MhDataMapper(self.parent)

        setattr(self.parent, name, mapper)
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
        delegate = mapping.getAttribute('delegate')

        if not inputname:

            raise ModelBindingMapperAttributeError(
                self.parent,
                'input',
                mapping
            )

        if not fieldname:

            raise ModelBindingMapperAttributeError(
                self.parent,
                'field',
                mapping
            )

        if not hasattr(self.parent, inputname):

            raise ModelBindingViewAttributeError(
                self.parent,
                inputname,
                mapping
            )

        try:

            field_index = model.get_field_index(fieldname)

        except:

            raise ModelBindingMappingFieldError(
                mapper,
                fieldname,
                mapping
            )

        widget = getattr(self.parent, inputname)

        if not delegate:
            mapper.addMapping(widget, field_index)

        else:
            mapper.addDelegatedMapping(widget, field_index, delegate)

    def configMapper(self, mapper, element):

        selectorview = element.getAttribute('selectorview')
        manualsubmit = element.hasAttribute('manualsubmit')

        commiter = element.getAttribute('commiter')
        accept = element.getAttribute('accept')
        reject = element.getAttribute('reject')
        done = element.getAttribute('done')

        if element.hasAttribute('selectorview'):
            self.bindSelectorView(mapper, selectorview, element)

        if element.hasAttribute('commiter') and (accept or reject or done):
            self.bindCommiter(mapper, commiter, accept, reject, done, element)

        if manualsubmit:
            mapper.setSubmitPolicy(mapper.ManualSubmit)

    def bindSelectorView(self, mapper, selectorview, element):

        if not selectorview:
            raise ModelBindingMapperSelectorViewError(element)

        if not hasattr(self.parent, selectorview):
            raise ModelBindingViewAttributeError(
                self.parent,
                selectorview,
                element
            )

        selectorview = getattr(self.parent, selectorview)
        mapper.setSelectorView(selectorview)

    def bindCommiter(self, mapper, commiter, accept, reject, done, element):

        if not hasattr(self.parent, commiter):

            raise ViewAttributeError(self.parent, commiter, element)

        commiter_attr = getattr(self.parent, commiter)

        if commiter_attr.__class__.__name__ != 'QDialogButtonBox':

            raise ModelBindingMappingCommiterError(
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

                raise ViewAttributeError(
                    self.parent,
                    value,
                    element
                )
