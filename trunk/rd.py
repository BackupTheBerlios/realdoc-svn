#!/usr/bin/python
# -*- encoding: ISO-8859-1 -*-
#
# Copyright 2006  Peter Gebauer
# (see LICENSE.txt for licensing information)

import sys
sys.path.append("src")
from optparse import OptionParser
from realdoc.generators.file import FileGenerator
from realdoc.factories.file import FileFactory
from realdoc.serializers.xml import XMLSerializer


parser = OptionParser(usage="rd [options] [-o output dir] [input dir or file]")
parser.add_option("-o", "--outputdir", dest="outputDir", default=".",
                  help="ouput files to DIRECTORY")
parser.add_option("-d", "--decode", dest="decode", default=None,
                  help="select source input codec")
parser.add_option("-e", "--encode", dest="encode", default=None,
                  help="select file output codec")
parser.add_option("-q", "--quiet",
                  action="store_true", dest="quiet", default=False,
                  help="don't print status messages to stdout")
parser.add_option("-t", "--title", dest="title", default=None,
                  help="title for the documentation")
parser.add_option("-c", "--copyright", dest="copyright", default=None,
                  help="title for the documentation")
parser.add_option("-x", "--xslt",
                  action="store_true", dest="xslt", default=False,
                  help="process XML using XSLT stylesheet")
parser.add_option("-s", "--stylesheet", dest="stylesheet",
                  default="/usr/local/share/realdoc/realdoc-xhtml.xsl",
                  help="use this XSLT stylesheet instead of default")
parser.add_option("--suffix", dest="suffix", default=".html",
                  help="suffix the ending of the XSLT processed filenames")

(options, args) = parser.parse_args()

if not args:
    print "Copyright 2006  Peter Gebauer"
    print "(see LICENSE.txt for licensing information)"
    print
    parser.print_help()
    raise Exception("you must explicitly specify a starting directory or file!")

fg = FileGenerator(FileFactory(args[0], options.decode),                   
                   XMLSerializer({"title": options.title,
                                  "copyright": options.copyright},
                                 options.encode),
                   options.outputDir,
                   options.quiet
                   )
fg.generate()

if options.xslt:
    from realdoc.xslt import XSLTProcessor
    xp = XSLTProcessor(options.outputDir, options.encode, options.quiet)
    xp.process(options.stylesheet, options.suffix)
