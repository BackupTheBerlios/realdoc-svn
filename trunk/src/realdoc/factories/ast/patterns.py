# Copyright 2006  Peter Gebauer
# (see LICENSE.txt for licensing information)
"""
Contains patterns used to match AST data.
"""
from realdoc.factories.ast import ASTFactory, extract, Pattern
from realdoc import *

      
class DocstringPattern(Pattern):
    """
    Match a docstring.
    """

    def __init__(self):
        Pattern.__init__(self, (266, (267, (268, (269, (320, (298, (299, (300, (301, (303, (304, (305, (306, (307, (308, (309, (310, (311, (3, str))))))))))))))))), (4, str))))

    def getObject(self, data):
        return DocString(extract(data, *(1,) * 19).decode(self.encoding))


class ClassPattern(Pattern):
    """
    Match class definitions.
    """

    def __init__(self, path = None):
        Pattern.__init__(self, (266, (291, (323, (1, "class"), (1, str)))))
        self.path = path

    def getObject(self, data):
        name = extract(data, 1, 1, 2, 1).decode(self.encoding)
        subdata = extract(data, 1, 1)[4:]
        astf = ASTFactory(self.encoding, (AncestorsPattern(),))
        ancestors = astf._getObjects(subdata[0])
        doc = DocClass(self.path and u"%s.%s"%(self.path, name) or name,
                       ancestors)
        astf.patterns = (ClassPattern(), DefPattern(), DocstringPattern())
        doc.children += astf._getObjects(subdata, doc.path)
        return doc


class DefPattern(Pattern):
    """
    Match def-statements.
    """

    def __init__(self, path = None):
        Pattern.__init__(self, (266, (291, (261, (1, "def"), (1, str)))))
        self.path = path

    def getObject(self, data):
        name = extract(data, 1, 1, 2, 1).decode(self.encoding)
        # extract(data, 1, 1)[3:][0]
        doc = DocDef(self.path and u"%s.%s"%(self.path, name) or name)
        astf = ASTFactory(self.encoding,
                          (ArgsPattern(),
                           ClassPattern(),
                           DefPattern(),
                           DocstringPattern()))
        doc.children += astf._getObjects(extract(data, 1, 1)[3:], doc.path)
        return doc


class AncestorsPattern(Pattern):
    """
    Match ancestors in a class definition.
    """

    def __init__(self):
        Pattern.__init__(self, (298, (299, (300, (301, (303, (304, (305, (306, (307, (308, (309, (310, (311, (1, str)))))))))))))))

    def getObject(self, data):
        return DocAncestor(extract(data, *(1,) * 14).decode(self.encoding))


class ArgsPattern(Pattern):
    """
    Match arguments for a def statement.
    """

    def __init__(self):
        Pattern.__init__(self, (262, (7, '('), (263,)))

    def getObject(self, data):
        args = []
        data = data[1:][1:][0][1:]
        for i in xrange(len(data) - 2):
            if data[i][0] == 264:
                astf = ASTFactory(self.encoding,
                                  (ArgDefaultPattern(),
                                   ))
                defaults = astf._getObjects(data[i + 2], self.path)
                if defaults:
                    default = defaults[0]
                else:
                    default = None
                args.append(DocArgument(data[i][1][1].decode(self.encoding),
                                        default))
            elif (i < len(data) - 1
                  and data[i][0] == 16
                  and data[i + 1][0] == 1):
                args.append(DocArgument(
                    u"*%s"%data[i + 1][1].decode(self.encoding)))
            elif (i < len(data) - 1
                  and data[i][0] == 36
                  and data[i + 1][0] == 1):
                args.append(DocArgument(
                    u"**%s"%data[i + 1][1].decode(self.encoding)))
        return args


class ArgDefaultPattern(Pattern):
    """
    Match default values for arguments.
    """

    def __init__(self):
        Pattern.__init__(self, (299, (300, (301, (303, (304, (305, (306, (307, (308, (309, (310, (311, )))))))))))))

    def getObject(self, data):
        dd = extract(data, *(1,) * 13)
        if dd == u"{":
            subdata = extract(data, *(1, ) * 11)[2][1:]
            ret = []
            for i in xrange(len(subdata) - 2):
                if subdata[i + 1][1] == u":":
                    if ret:
                        ret.append(u", ")
                    else:
                        ret.append(u"{")
                    ret.append(extract(subdata[i], *(1, ) * 14))
                    ret.append(u": ")
                    astf = ASTFactory(self.encoding,
                                      (ArgDefaultPattern(),
                                       ))
                    sub = astf._getObjects(subdata[i + 2], self.path)
                    ret.append(u", ".join(sub))
                    ret.append(u"}")
            return u"".join(ret)
        elif dd == u"[" or dd == u"(":
            subdata = extract(data, *(1, ) * 11)[2][1:]
            astf = ASTFactory(self.encoding,
                              (ArgDefaultPattern(),
                               ))
            sub = []
            for d in subdata:
                sub += astf._getObjects(d, self.path)
            return u"[%s]"%u", ".join(sub)
        return dd
        
