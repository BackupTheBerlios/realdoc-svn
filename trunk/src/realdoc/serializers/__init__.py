# Copyright 2006  Peter Gebauer
# (see LICENSE.txt for licensing information)
"""
Serializers turn Doc-trees into strings.
"""

class SerializationException(Exception):
    """
    Raised when a doc tree (an object within that tree) can't be
    serialized.
    """

    def __init__(self, msg, docObject):
        Exception.__init__(self, msg)
        self.docObject = docObject


class Serializer(object):
    """
    Used to serialize a doc tree.
    """

    def serialize(self, docObjects):
        """
        Should be able to take a tuple/list of Doc objects or
        a single doc object to be serialized.
        If a tuple or list, generate some sort of index/cover data for
        all DocPackage and DocModule instances.
        """
        raise NotImplementedError()
