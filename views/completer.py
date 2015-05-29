from PySide.QtCore import SIGNAL
from PySide.QtGui import QItemDelegate, QLineEdit


class MhColumnCompleterDelegate(QItemDelegate):

    def __init__(self, completer, parent=None):

        super(MhColumnCompleterDelegate, self).__init__(parent)

        self.__completer = completer

        self.__completer.connect(
            SIGNAL('activated(QModelIndex)'),
            self.sendIndex
        )

    def createEditor(self, widget, style, index):

        super(MhColumnCompleterDelegate, self).createEditor(
            widget,
            style,
            index
        )

        self.__current_index = index

        lineedit = QLineEdit(self.parent())
        lineedit.setCompleter(self.__completer)

        return lineedit

    def sendIndex(self, index):

        widget = self.parent()

        if index.isValid():

            delegated_object = self.completer.model().records[index.row()]

            widget.model().setData(self.__current_index, delegated_object)

    @property
    def completer(self):

        return self.__completer
