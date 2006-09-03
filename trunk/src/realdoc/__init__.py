# Copyright 2006  Peter Gebauer
# (see LICENSE.txt for licensing information)
"""
The main RealDoc package contains all base-types used by all
factories, serializers, generators, etc.
"""

class Doc(object):
    """
    Any doc object in the tree.
    """

    def dump(self, indent = ""):
        print u"%s%s"%(indent, self)


class DocContainer(Doc):
    """
    A doc object that can contain other doc objects.
    """

    def __init__(self, children = None):
        Doc.__init__(self)
        if children:
            self.children = children
        else:
            self.children = []

    def addChild(self, child):
        self.children.append(child)
        return child

    def removeChild(self, child):
        try:
            i = self.children.index(child)
        except ValueError:
            return -1
        self.children.remove(child)
        return i

    def getDocStrings(self):
        return [child for child in self.children
                if isinstance(child, DocString)]

    def __iter__(self):
        return iter(self.children)

    def __str__(self):
        return u"<%s (%d)>"%(
            self.__class__.__name__,
            len(self.children))

    def dump(self, indent = u""):
        Doc.dump(self, indent)
        for child in self.children:
            child.dump(u"    %s"%indent)


class DocString(Doc):
    """
    Representing the docstring.
    """

    def __init__(self, s):
        Doc.__init__(self)
        self.stringData = unicode(s)

    def dump(self, indent):
        print u"\n".join((u"%s%s"%(indent, l.strip())
                         for l in self.stringData.split(u"\n")))

    def __str__(self):
        lowest = -1
        for d in self.stringData.split(u"\n"):
            if len(d) - len(d.strip()) < lowest or lowest < 0:
                lowest = len(d) - len(d.strip())
        ret = []
        for d in (s.replace(u"\"\"\"", u"")
                  for s in self.stringData.split(u"\n")):
            if d or ret:
                ret.append(d[lowest:].rstrip())
        return u"\n".join(ret)


class DocAncestor(Doc):
    """
    The ancestors of a class. Basically a Doc-compatible string.
    """

    def __init__(self, name):
        Doc.__init__(self)
        self.name = name
        
    def __str__(self):
        return self.name


class DocPath(DocContainer):
    """
    A doc object with a path.
    """

    def __init__(self, path, children = None):
        DocContainer.__init__(self, children)
        self.path = path

    def getClasses(self):
        return [child for child in self.children
                if isinstance(child, DocClass)]

    def getDefs(self):
        return [child for child in self.children
                if isinstance(child, DocDef)]

    def __str__(self):
        return u"<%s '%s' (%d)>"%(
            self.__class__.__name__,
            self.path,
            len(self.children))


class DocPackage(DocPath):
    """
    Represents a package.
    """

    def __init__(self, path, children = None):
        DocPath.__init__(self, path, children)

    def getPackages(self):
        return [child for child in self.children
                if isinstance(child, DocPackage)]

    def getModules(self):
        return [child for child in self.children
                if isinstance(child, DocModule)]

class DocModule(DocPath):
    """
    Represents a module.
    """

    def __init__(self, path, children = None):
        DocPath.__init__(self, path, children)


class DocClass(DocPath):
    """
    Represents a class.
    """

    def __init__(self, path, children = None):
        DocPath.__init__(self, path, children)

    def getAncestors(self):
        return [child for child in self.children
                if isinstance(child, DocAncestor)]

    def __str__(self):
        ancestors = self.getAncestors()
        ancs = ancestors and u"(%s)"%", ".join((u"%s"%a
                                                for a in ancestors)) or ""
        return u"<%s '%s%s' (%d)>"%(
            self.__class__.__name__,
            self.path,
            ancs,
            len(self.children))


class DocDef(DocPath):
    """
    Represents a def-statement.
    """

    def __init__(self, path, children = None):
        DocPath.__init__(self, path, children)

    def getArguments(self):
        return [child for child in self.children
                if isinstance(child, DocArgument)]

    def __str__(self):
        return u"<%s '%s(%s)' (%d)>"%(
            self.__class__.__name__,
            self.path,
            ", ".join(("%s"%a for a in self.getArguments())),
            len(self.children))

    def dump(self, indent = ""):
        print u"%s%s"%(indent, self)
        for child in (c for c in self.children
                      if not isinstance(c, DocArgument)):
            if hasattr(child, "dump"):
                child.dump(u"    %s"%indent)
            else:
                print u"%s%s"%(indent, child)


class DocArgument(DocPath):
    """
    Any argument for a def-statement.
    """

    def __init__(self, name, default = None):
        DocPath.__init__(self, name, [])
        self.default = default
        
    def __str__(self):
        if self.default:
            return u"%s = %s"%(self.path, self.default)
        return u"%s"%self.path
