#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys


class ContentHandler(ContentHandler):

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.title = ""
        self.theContent = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title' or name == 'link':
                self.inContent = True

    def endElement(self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.title = (self.theContent).encode('utf-8')
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                print '<p><a href="' + (self.theContent).encode('utf-8') \
                    + '">' + self.title + '</a></p>'
                self.inContent = False
                self.title = ""
                self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# -----main-----

if len(sys.argv) < 2:
    print "Usage: python " + sys.argv[0] + " <document>"
    print
    sys.exit(1)

# Load parser and driver
theParser = make_parser()
theHandler = ContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!
try:
    xmlFile = open(sys.argv[1], "r")
except IOError:
    print "File " + sys.argv[1] + " does not exists"
    sys.exit(1)
print "<html><body>"
theParser.parse(xmlFile)
print "</body></html>"
print
