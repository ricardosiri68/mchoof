import os
from PySide.QtCore import SIGNAL
from .parser import ConfParser
from . import exceptions


class SignalConfParser(ConfParser):

    def __init__(self, parent):
        conf_path = os.path.join(
            parent.__class__.__module__.split('.')[0],
            'conf',
            parent.signals_conf
        )
        self.parent = parent
        ConfParser.__init__(self, conf_path)
        self.bindSignals(self.rootNode().childNodes)

    def bindSignals(self, childnodes):
        for childnode in childnodes:

            if childnode.nodeName == 'signal':
                self.bindSignal(self.parent, childnode)

            elif childnode.nodeName == 'attr_signal':
                self.bindAttrSignal(childnode)

    def bindSignal(self, qobject, signal_element):
        name = signal_element.getAttribute('name')
        target = signal_element.getAttribute('target')
        attr = signal_element.getAttribute('attr')

        if not name:
            raise exceptions.SignalNameError(self.parent, signal_element)

        if not target:
            raise exceptions.SignalTargetError(self.parent, signal_element)

        must_be_an_attr = (
            qobject is self.parent or
            signal_element.hasAttribute('attr')
        )
        if not attr and must_be_an_attr:
            raise exceptions.SignalAttributeSenderNonValueError(
                self.parent,
                qobject,
                signal_element
            )

        if attr:
            if not hasattr(qobject, attr):
                raise exceptions.SignalQObjectNonHasAttrError(
                    self.parent,
                    qobject,
                    attr,
                    signal_element
                )
            else:

                qobject = getattr(qobject, attr)

                if callable(qobject):
                    qobject = qobject()

        if not hasattr(self.parent, target):
            raise exceptions.SignalInvalidTargetError(
                self.parent,
                target,
                signal_element
            )

        qobject.connect(
            SIGNAL(str(name)),
            getattr(self.parent, target)
        )

    def bindAttrSignal(self, attr_element):
        name = attr_element.getAttribute('name')

        if not name:
            raise exceptions.SignalAttributeSenderNameError(
                self.parent,
                attr_element
            )

        if not hasattr(self.parent, name):
            raise exceptions.SignalQObjectNonHasAttrError(
                self.parent,
                self.parent,
                name,
                attr_element
            )

        qobject = getattr(self.parent, name)

        for childnode in attr_element.childNodes:
            if childnode.nodeName == 'signal':
                self.bindSignal(qobject, childnode)
