from PySide.QtCore import Qt
from PySide.QtGui import QCompleter
from . import exceptions


class ModelBindCompleterParser:

    def __init__(self, parser_parent):

        self.parser_parent = parser_parent
        self.parent = parser_parent.parent

    def bindCompleters(self, model, childnodes):

        for childnode in childnodes:

            if childnode.nodeName == 'completer':

                self.bindCompleter(model, childnode)

    def bindCompleter(self, model, completer_element):
        '''<completer
                name="uiApostadores"
                completionfield="nombre"
                onnew="addCompostador"
        />'''

        name = completer_element.getAttribute('name')
        completion_field = completer_element.getAttribute('completionfield')
        on_new = completer_element.getAttribute('onnew')

        if not name:

            raise exceptions.ModelBindingNameError(completer_element)

        if not completion_field:

            raise exceptions.NoCompletionFieldException(
                self.parent,
                completer_element
            )

        if completer_element.hasAttribute('onnew') and not on_new:

            raise exceptions.NoCompletionDataExeption(
                self.parent,
                completer_element
            )

        completer = QCompleter(self.parent)
        setattr(self.parent, name, completer)

        completer.setModel(model)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionColumn(model.get_field_index(completion_field))
