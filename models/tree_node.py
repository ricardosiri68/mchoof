class Node(object):

    def __init__(self, record=None, parent=None):

        self.__parent = parent
        self.__record = record
        self.__childnodes = []

        if parent is not None:
            parent.addChild(self)

    def addChild(self, childnode):

        self.__childnodes.append(childnode)

    def parent(self):

        return self.__parent

    def childnodes(self):

        return self.__childnodes

    def clearChilds(self):

        self.__childnodes = []

    def row(self):

        return self.parent().childnodes().index(self)

    def record(self):

        return self.__record

    def child(self, row):

        try:

            return self.__childnodes[row]

        except IndexError:

            pass

    def childCount(self):

        return len(self.__childnodes)

    def log(self, tablevel=-1):

        tablevel += 1
        output = tablevel * '\t'

        output += '%s\n' % self.__record

        for childnode in self.__childnodes:
            output += childnode.log(tablevel)

        tablevel -= 1

        return output
