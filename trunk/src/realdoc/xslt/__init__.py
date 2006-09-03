# Copyright 2006  Peter Gebauer
# (see LICENSE.txt for licensing information)
"""
XSLT processing add-on.

This package provides transformation support using XSLT.
"""
import os
import libxml2, libxslt

class XSLTException(Exception):
    """
    Raise this for any problems regarding XSLT processing.
    """

    def __init__(self, stylesheet, xml = None):
        Exception.__init__(self, "problem applying stylesheet '%s' on file '%s'"%(stylesheet, xml))
        self.stylesheet = stylesheet
        self.xml = xml


class XSLTProcessor(object):
    """
    Iterate a RealDoc tree structure with XML-files and process them
    using specified stylesheet.
    """

    def __init__(self, directory, encoding, quiet = False):
        self.directory = os.path.normpath(directory)
        self.encoding = encoding
        self.quiet = quiet

    def _process(self, style, directory, suffix, index):
        for f in os.listdir(directory):
            fn = os.path.normpath("%s/%s"%(directory, f))
            if os.path.isfile(fn) and f.endswith(".xml"):
                doc = libxml2.parseFile(fn)
                result = style.applyStylesheet(doc, {"index":
                                                     "'%s'"%index})
                filename = os.path.normpath("%s/%s%s"
                                            %(directory,
                                              f[:f.rindex(".")],
                                              suffix))
                result.saveFileEnc(filename, self.encoding)
                doc.freeDoc()
                result.freeDoc()
                if not self.quiet:
                    print "processed '%s' to '%s'"%(fn, filename)
            elif os.path.isdir(fn):
                self._process(style, fn, suffix, "%s/.."%index)

    def process(self, stylesheet, suffix):
        styledoc = libxml2.parseFile(stylesheet)
        style = libxslt.parseStylesheetDoc(styledoc)
        self._process(style, self.directory, suffix, ".")
        style.freeStylesheet()
