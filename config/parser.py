import os
from xml.dom.minidom import parse


class ConfParser:

    def __init__(self, filename):
        self.__filename = filename
        self.__document = parse(filename)

    def document(self):
        return self.__document

    def rootNode(self):
        return self.__document.childNodes[0]

    def filename(self):
        return self.__filename
