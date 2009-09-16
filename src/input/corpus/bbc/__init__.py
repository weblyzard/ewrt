
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

from eWRT.config import BBC_CORPUS_PRINT
from eWRT.conv.html import HtmlToText
import os

class BBCGetCorpus(object):
    """ An iterator over all documents """

    def __init__(self, filePattern="*"):
        """ @param[in] filePattern Pattern of files to consider (e.g. 7[3456789]*.stm)
        """
        self.files = glob( os.path.join(BBC_CORPUS_PRINT, filePattern) )

    def __iter__(self):
        return self

    def next(self):
        if self.files:
            htmlTxt = open( self.files.pop() ).read()
            return HtmlToText.getText( htmlTxt )
        else:
            raise StopIteration

