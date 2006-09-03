# Copyright 2006  Peter Gebauer
# (see LICENSE.txt for licensing information)
"""
This package contains the basics for making Doc-trees from AST data.
"""

import sys, os, re, locale
import symbol, token

from realdoc import *
from realdoc.factories import *

def extract(data, *indices):
    """
    extractItem(l, 0, 3, -1) is equivalent to l[0][3][-1].
    """
    counter = 0
    for i in indices:
        counter += 1
        try:
            data = data[i]
        except (TypeError, IndexError):
            return None
    return data


def getSize(data):
    if isinstance(data, (tuple, list)):
        size = 0
        for d in data:
            size += getSize(d)
        return size
    return 1


class Pattern(object):
    """
    AST patterns can be matched with other patterns or AST tuples.
    """

    def __init__(self, pattern, encoding = None):
        self.pattern = pattern
        self.encoding = encoding

    def getSize(self):
        return getSize(self.pattern)

    def _testEq(self, pattern, data):
        if (isinstance(pattern, (tuple, list))
            and isinstance(data, (tuple, list))):
            if len(pattern) <= len(data):
                for i in xrange(len(pattern)):
                    if not self._testEq(pattern[i], data[i]):
                        return False
                return True
        elif isinstance(pattern, type):
            if isinstance(data, pattern):
                return True
        elif (type(pattern) == type(data)
              and pattern == data):
            return True
        return False

    def getObject(self, data):
        return data

    def __eq__(self, comp):
        if (not hasattr(comp, "__iter__")
            and not hasattr(comp, "pattern")):
            raise TypeError("patterns can only be "
                            "compared with other patterns or sequences")
        if hasattr(comp, "pattern"):
            comp = comp.pattern
        return self._testEq(self.pattern, comp)
    

class ASTFactory(Factory):
    """
    Can create package and module content from AST's.
    """

    def __init__(self, encoding, patterns):
        Factory.__init__(self)
        if encoding:
            self.encoding = encoding
        else:
            self.encoding = locale.getpreferredencoding()
        self.patterns = patterns

    def _getObjects(self, ast, path = None):
        ret = []
        if isinstance(ast, (tuple, list)):
            for data in ast:
                if isinstance(data, (tuple, list)):
                    for pattern in self.patterns:
                        if pattern == data:
                            pattern.path = path
                            pattern.encoding = self.encoding
                            do = pattern.getObject(data)
                            if do:
                                if isinstance(do, (tuple, list)):
                                    ret += do
                                else:
                                    ret.append(do)
                            break
                        #else:
                        #    print pattern.__class__.__name__, pattern.pattern
                        #    print data
                        #    print
            ret += self._getObjects(data, path)
        return ret
