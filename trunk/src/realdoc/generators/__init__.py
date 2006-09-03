# Copyright 2006  Peter Gebauer
# (see LICENSE.txt for licensing information)
"""
Default generators package.

Generators generate the result from the serializers.
"""
from realdoc import DocPackage, DocModule

class Generator(object):
    """
    Base generator class.
    """
    def generatePackage(self, package):
        raise NotImplementedError()
    
    def generateModule(self, m):
        raise NotImplementedError()

    def generate(self, docObjects = None):
        if not docObjects:
            docObjects = self.factory.getPackages()
        for docObject in docObjects:
            if isinstance(docObject, DocPackage):
                self.generatePackage(docObject)
            elif isinstance(docObject, DocModule):
                self.generateModule(docObject)
