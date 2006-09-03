# Copyright 2006  Peter Gebauer
# (see LICENSE.txt for licensing information)
"""
Generators that can create output to a filesystem.
"""

import os
from realdoc.generators import Generator

class FileGenerator(Generator):
    """
    Creates an output file for every python file.

    It supports packages (i.e directories) and is recursive.
    """

    def __init__(self,
                 factory,
                 serializer,
                 outputDir,
                 quiet = False):
        Generator.__init__(self)
        self.outputDir = outputDir
        self.quiet = quiet
        self.factory = factory 
        self.serializer = serializer

    def generateModule(self, m):
        adir = self.outputDir
        if not os.path.isdir(adir):
            os.mkdir(adir)
        for d in m.path.split(".")[:-1]:
            adir = os.path.normpath("%s/%s"%(adir, d))
            if not os.path.isdir(adir):
                os.mkdir(adir)
        filename = "%s/%s.xml"%(adir, m.path.split(".")[-1])
        f = file(filename, "w")
        f.write(self.serializer.serialize(m))
        f.close()
        if not self.quiet:
            print "wrote doc for module  '%s': %s"%(m.path, filename)

    def generatePackage(self, package):
        adir = self.outputDir
        if not os.path.isdir(adir):
            os.mkdir(adir)
        for d in package.path.split("."):
            adir = os.path.normpath("%s/%s"%(adir, d))
            if not os.path.isdir(adir):
                os.mkdir(adir)
        filename = "%s/__init__.xml"%adir
        f = file(filename, "w")
        f.write(self.serializer.serialize(package))
        f.close()
        if not self.quiet:
            print "wrote doc for package '%s': %s"%(package.path,
                                                    filename)
        for p in package.getPackages():
            self.generatePackage(p)
        for p in package.getModules():
            self.generateModule(p)

    def generate(self, docObjects = None):
        if not docObjects:
            docObjects = self.factory.getPackages()
        Generator.generate(self, docObjects)
        if not os.path.isdir(self.outputDir):
            os.mkdir(self.outputDir)
        filename = "%s/index.xml"%self.outputDir
        f = file(filename, "w")
        f.write(self.serializer.serialize(docObjects))
        f.close()
        if not self.quiet:
            print "wrote index '%s'"%filename
        
