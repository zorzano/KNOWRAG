class KGIoTDriver(object):

    def close(self):
        # Empty method, to be fulfiiled by inheritors
        raise NotImplementedError()

    def nukeBase(self):
        raise NotImplementedError()

    def readNode(self, type, attributes):
        raise NotImplementedError()

    def readNodeAndLinked(self, type, attributes):
        raise NotImplementedError()

    def mergeNode(self, type, attributes):
        raise NotImplementedError()

    def mergeLink(self, typeLink, attributesLink, typeA, attributesA, typeB, attributesB):
        raise NotImplementedError()
