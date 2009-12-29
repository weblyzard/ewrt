#!/usr/bin/env python

""" 
    @package DetectLanguage.reuters
    a generic method to retrieve text from the reuters corpus
"""

# -----------------------------------------------------------------------
# - (C)opyright 2009 by Albert Weichselbraun <albert@weichselbraun.net>
# -                    webLyzard technology gmbh <awe@weblyzard.com>
# -----------------------------------------------------------------------

__revision__ = "$Revision: 545 $"
__author__   = "Albert Weichselbraun"


from xml.sax import handler, parseString
from glob import glob
from eWRT.config import REUTERS_DATA_DIR
from zipfile import ZipFile
import os

class ReutersParser(handler.ContentHandler):

    RELEVANT_ELEMENTS = ('title', 'text')

    def __init__(self):
        self.clear()

    def startElement(self, name, attrs):
        if name.lower() in self.RELEVANT_ELEMENTS:
            self.isRelevantText = True

    def endElement(self, name):
        if name.lower() in self.RELEVANT_ELEMENTS:
            self.isRelevantText = False

    def characters(self, content):
        if self.isRelevantText:
            if content.strip():
                self.text.append(content.strip())

    def getText(self):
        return "\n".join(self.text)

    def clear(self):
        self.isRelevantText = False
        self.text = []
        
class Reuters(object):

    @staticmethod
    def getText(s):
        """ returns the relevant strings from the given reuters article
            @param[in] s      string containing the article
            @returns the text in the file from the headline and text fields
        """
        # parser = make_parser()
        rps = ReutersParser()
        parseString(s, rps)
        return rps.getText()

class ReutersGetCorpus(object):
    """ An iterator for all documents in the given language """

    def __init__(self, lang):
        self.files = glob( os.path.join( REUTERS_DATA_DIR, lang, "*.xml") )

    def __iter__(self):
        return self

    def next(self):
        if self.files:
            xmlTxt = open( self.files.pop() ).read()
            return Reuters.getText( xmlTxt )
        else:
            raise StopIteration

class ReutersGetZipCorpus(object):
    """ An iterator over all documents in a zipped reuters corpus """

    def __init__(self, baseDir, lang):
        self.zipFiles = glob( os.path.join( baseDir, lang, "*.zip") )
        self.zip, self.files = self.openNextZipFile()

    def __iter__(self):
        return self

    def next(self):
        if not self.files:
            self.zip, self.files = self.openNextZipFile()

        fname = self.files.pop()
        return fname, Reuters.getText( self.zip.read( fname ))

    def openNextZipFile(self):
        if not self.zipFiles:
            raise StopIteration

        fname = self.zipFiles.pop()
        zip = ZipFile(fname)
        
        return zip, zip.namelist()


if __name__ == '__main__':
    import sys
    for nr,t in enumerate(ReutersGetZipCorpus( "./eval", "it") ):
        print t
        sys.exit(0)

    for nr,t in enumerate(ReutersGetCorpus("de")):
        print nr
