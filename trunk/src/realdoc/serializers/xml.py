# Copyright 2006  Peter Gebauer
# (see LICENSE.txt for licensing information)
"""
Creates regular realdoc XML from a doc-tree.

The DTD for this XML can be found in share/realdoc.dtd
"""
import locale
from realdoc import *
from realdoc.serializers import *

def escape(s, attr = False):
    """
    Escapes <, > and optionally \" if attr = True.
    """
    s = s.replace(u"<", u"&lt;").replace(u">", u"&gt;u").replace(u"&", u"&amp;")
    if attr:
        s = s.replace("\"", "&quot;")
    return s


class XMLSerializer(Serializer):
    """
    Creates realdoc XML (share/realdoc.dtd) from a doc-tree.
    """

    def __init__(self, meta, encoding = None):
        Serializer.__init__(self)
        self.meta = meta
        if encoding:
            self.encoding = encoding
        else:
            self.encoding = locale.getpreferredencoding()

    def _serializeMeta(self):
        ret = []
        for k, v in self.meta.items():
            if v:
                ret.append(u"<meta name=\"%s\">"%escape(k, True))
                ret += (u"    %s"%escape(s.strip()) for s in v.split(u"\n"))
                ret.append(u"</meta>")
            else:
                ret.append(u"<meta name=\"%s\"/>"%escape(k, True))
        return u"\n".join(ret)

    def _serializeDocStrings(self, doc, lines = None):
        ret = []
        docs = doc.getDocStrings()
        if docs:
            ret.append(u"<doc>")
            rr = []
            for d in (u"%s"%s for s in docs):
                rr.append(escape(d).replace(u" ", u"&#160;"))
            splitty = ("".join(rr)).split("\n")
            if lines:
                ret.append("&lt;br/&gt;".join(splitty[:lines]))
            else:
                ret.append("&lt;br/&gt;".join(splitty))
            ret.append(u"</doc>")
        return u"\n".join(ret)
    
    def _serializeClass(self, doc):
        ret = [u"<class name=\"%s\" path=\"%s\">"%(doc.path.split(u".")[-1],
                                                  doc.path)]
        ret += (u"    %s"%s
                for s in self._serializeDocStrings(doc).split("\n"))
        for child in doc.getAncestors():
            ret.append(u"    <ancestor>%s</ancestor>"%child)
        for child in doc.getClasses():
            ret += (u"    %s"%s
                    for s in self._serializeClass(child).split(u"\n"))
        for child in doc.getDefs():
            ret += (u"    %s"%s
                    for s in self._serializeDef(child).split(u"\n"))
        ret.append(u"</class>")
        return u"\n".join(ret)

    def _serializeDef(self, doc):
        ret = [u"<def name=\"%s\" path=\"%s\">"%(doc.path.split(u".")[-1],
                                                doc.path)]
        ret += (u"    %s"%s
                for s in self._serializeDocStrings(doc).split("\n"))
        for child in doc.getArguments():
            name = child.path.split(".")[-1]
            if name.startswith("**"):
                type_ = "dict"
                name = name[2:]
            elif name.startswith("*"):
                type_ = "list"
                name = name[1:]
            else:
                type_ = "normal"
            if child.default:
                ret.append(u"    <arg type=\"%s\" default=\"%s\">%s</arg>"%(
                    type_, escape(child.default, True), name))
            else:
                ret.append(u"    <arg type=\"%s\">%s</arg>"%
                           (type_, name))
        for child in doc.getClasses():
            ret += (u"    %s"%s
                    for s in self._serializeClass(child).split(u"\n"))
        for child in doc.getDefs():
            ret += (u"    %s"%s
                    for s in self._serializeDef(child).split(u"\n"))
        ret.append(u"</def>")
        return u"\n".join(ret)

    def _serializeModule(self, doc):
        ret = [u"<module name=\"%s\" path=\"%s\">"%(doc.path.split(u".")[-1],
                                                doc.path)]
        ret += (u"    %s"%s
                for s in self._serializeDocStrings(doc).split("\n"))
        for child in doc.getClasses():
            ret += (u"    %s"%s
                    for s in self._serializeClass(child).split(u"\n"))
        for child in doc.getDefs():
            ret += (u"    %s"%s
                    for s in self._serializeDef(child).split(u"\n"))
        ret.append(u"</module>")
        return u"\n".join(ret)

    def _serializePackage(self, doc):
        ret = [u"<package name=\"%s\" path=\"%s\">"%(doc.path.split(u".")[-1],
                                                doc.path)]
        ret += (u"    %s"%s
                for s in self._serializeDocStrings(doc).split("\n"))
        for child in doc.getPackages():
            ret.append(u"    <subpackage path=\"%s\">"%child.path)
            ret += (u"        %s"%s
                    for s in self._serializeDocStrings(child).split("\n"))
            ret.append(u"    </subpackage>")
        for child in doc.getModules():
            ret.append(u"    <submodule path=\"%s\">"%child.path)
            ret += (u"        %s"%s
                    for s in self._serializeDocStrings(child).split("\n"))
            ret.append(u"    </submodule>")
        for child in doc.getClasses():
            ret += (u"    %s"%s
                    for s in self._serializeClass(child).split(u"\n"))
        for child in doc.getDefs():
            ret += (u"    %s"%s
                    for s in self._serializeDef(child).split(u"\n"))
        ret.append(u"</package>")
        return u"\n".join(ret)

    def _getContentList(self, doc):
        ret = []
        if isinstance(doc, Doc):
            if isinstance(doc, DocPackage):
                ret += (u"    %s"%s
                        for s in self._serializePackage(doc).split(u"\n"))
            elif isinstance(doc, DocModule):
                ret += (u"    %s"%s
                        for s in self._serializeModule(doc).split(u"\n"))
        elif isinstance(doc, (tuple, list)):
            for d in doc:
                if isinstance(d, DocPackage):
                    cl = "package"
                elif isinstance(d, DocModule):
                    cl = "module"
                else:
                    cl = None
                if cl:
                    ret.append(
                        u"    <index type=\"%s\" name=\"%s\" path=\"%s\">"
                        %(cl, d.path.split(u".")[-1], d.path))
                    docs = self._serializeDocStrings(d, 1).split(u"\n")
                    for l in (u"%s"%s for s in docs):
                        ret.append(u"        %s"%l)
                    ret.append(u"    </index>")
                    if isinstance(d, DocPackage):
                        newList = d.getModules() + d.getPackages()
                        ret += (u"%s"%s
                                for s in self._getContentList(newList))
        return ret
        
    def serialize(self, doc):
        ret = [u"<?xml version=\"1.0\" encoding=\"%s\"?>"%self.encoding,
               u"<!DOCTYPE realdoc SYSTEM \"/home/peter/projects/realdoc/share/realdoc.dtd\">"]
        ret.append(u"<realdoc version=\"alpha\">")
        ret += (u"    %s"%s
                for s in self._serializeMeta().split(u"\n"))        
        ret += self._getContentList(doc)
        ret.append(u"</realdoc>")
        try:
            return (u"\n".join(ret)).encode(self.encoding)
        except UnicodeEncodeError, uee:
            raise SerializationException("invalid data for encoding '%s'"
                                         %self.encoding,
                                         doc)
                                             
