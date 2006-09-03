# Copyright 2006  Peter Gebauer
# (see LICENSE.txt for licensing information)
"""
The FileFactory in this module can create Doc-trees from files containing
Python source code.

It can also be used to create Doc-trees from packages and directories
containing packages.
"""

import sys, os, re, locale
import parser

from realdoc import *
from realdoc.factories import *
from realdoc.factories.ast import ASTFactory
from realdoc.factories.ast.patterns import ClassPattern, DefPattern, DocstringPattern

class FileFactory(ASTFactory):
    """
    Create Doc-trees from a directory containing packages, a package
    directory or a Python source code file.
    """

    def __init__(self, directory, encoding = None, **kwargs):
        """
        Valid keyword arguments:
        excludes            List of regexp objects.
        encoding
        """
        ASTFactory.__init__(self,
                            encoding,
                            (ClassPattern(),
                             DefPattern(),
                             DocstringPattern())
                            )
        self.directory = directory
        self.excludes = kwargs.get("excludes", [])

    def _getTuple(self, data):
        return parser.suite(data).totuple()

    def _getModule(self, filename, packages = []):
        filename = os.path.normpath(filename)
        if (os.path.isfile(filename)
            and filename.endswith(".py")
            and not filename.endswith("__init__.py")):
            moduleName = os.path.basename(filename).split(".")[0]
            packages.append(moduleName)
            dm = DocModule(".".join(packages))
            data = self._getTuple(file(filename).read())
            try:
                dm.children += self._getObjects(data[1:], ".".join(packages))
            except UnicodeDecodeError, ude:
                raise InvalidDecodingException(filename, ude)
            return dm
        return None

    def _getModules(self, directory, packages = []):
        directory = os.path.normpath(directory)
        if os.path.isdir(directory):
            ret = []
            for entry in ("%s%s%s"%(directory, os.sep, f)
                          for f in os.listdir(directory)):
                if os.path.isfile(entry):
                    dm = self._getModule(entry, list(packages))
                    if dm:
                        ret.append(dm)
        return ret

    def _getPackage(self, directory, packages = []):
        directory = os.path.normpath(directory)
        if os.path.isdir(directory):
            initFile = os.path.normpath("%s%s__init__.py"%(directory, os.sep))
            if os.path.isfile(initFile):
                packages.append(directory.split(os.sep)[-1])
                dp = DocPackage(u".".join(packages))
                dp.children += self._getPackages(directory, packages)
                dp.children += self._getModules(directory, packages)
                data = self._getTuple(file(initFile).read())
                try:
                    dp.children += self._getObjects(data[1:],
                                                   u".".join(packages))
                except UnicodeDecodeError, ude:
                    raise InvalidDecodingException(initFile, ude)
                return dp
        return None

    def _getPackages(self, directory, packages = []):
        directory = os.path.normpath(directory)
        ret = []
        if os.path.isdir(directory):            
            for entry in ("%s%s%s"%(directory, os.sep, f)
                          for f in os.listdir(directory)):
                if (os.path.isfile(entry)
                    and entry.endswith("__init__.py")
                    and not packages):
                    dp = self._getPackage(directory, list(packages))
                    if dp:
                        ret.append(dp)
                elif os.path.isdir(entry):
                    dp = self._getPackage(entry, list(packages))
                    if dp:
                        ret.append(dp)
        elif os.path.isfile(directory) and not packages:
            dm = self._getModule(directory, [])
            if dm:
                ret.append(dm)
        return ret

    def getPackages(self):
        return self._getPackages(self.directory)
