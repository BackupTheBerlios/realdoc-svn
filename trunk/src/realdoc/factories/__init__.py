# Copyright 2006  Peter Gebauer
# (see LICENSE.txt for licensing information)
"""
Default factory packages.

A factory is used to create Doc-object trees from various sources.
"""

class InvalidDataException(Exception):
    """
    Raised by factories when the data it receives is invalid for
    creating a proper Doc tree.
    """

    def __init__(self, msg, data):
        Exception.__init__(self, msg)
        self.data = data


class InvalidDecodingException(Exception):
    """
    Factory is having problem decoding the source material.
    """

    def __init__(self, source, ude):
        Exception.__init__(
            self,
            "source '%s' has invalid data for codec %s"
            %(source, ude.encoding))


class Factory(object):
    """
    Used to create a doc tree.
    """

    def getPackages(self):
        raise NotImplementedError()
