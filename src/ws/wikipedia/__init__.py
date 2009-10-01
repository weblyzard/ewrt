#!/usr/bin/env python

""" @package eWRT.ws.wikipedia
    provides access to wikipedia using the wikipedia api
    http://en.wikipedia.org/w/api.php 
"""

# (C)opyrights 2008 by Albert Weichselbraun <albert@weichselbraun.net>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__version__ = "$Header$"

from eWRT.access.http import Retrieve
from urllib import urlencode
from xml.dom.minidom import parseString

WIKIPEDIA_API_QUERY = 'http://%s.wikipedia.org/w/api.php'

class WikiPedia(object):
    """ returns an WikiPedia Object  """

    def __init__(self):
        self.r = Retrieve( WikiPedia.__name__ )
    
    def getWikiPage(self, pageName, lang='en'):
        """ returns the given wikipedia page considering different spellings 
            @param[in] pageName
            @param[in] language (determines which wikipedia to query)
            @returns the page's wikipedia text
        """
        assert( len(lang)==2 )

        for pn in self._getPageNameAlterations( pageName ):
            pageContent = self._retrievePage( pn, lang )
            if pageContent:
                return pageContent

        return None

    @staticmethod
    def _getPageNameAlterations(pageName):
        """ @returns a list of differnt names for the given page """

        alt = [ pageName, ]
        if not ' ' in pageName:
            alt

        words = pageName.split(" ")
        alt.append( "%s %s" % (words[0].capitalize(), " ".join( map(str.lower, words[1:] ) )) )
        return alt

    def _retrievePage(self, pageName, lang):
        """ retrieves the given Wiki page
            @param[in] pageName
            @param[in] language (determines which wikipedia to query)
            @returns the page's wikipedia text
        """
        param = urlencode( {'action': 'query',
                            'format':'json', 
                            'export':'',
                            'redirects':'true',
                            'titles':pageName 
        })
        data = self.r.open( WIKIPEDIA_API_QUERY % lang, param ).read()
        jsonData = eval( data  )['query']
        if '-1' in jsonData['pages']:
            return None

        xmlData = jsonData['export']['*'].replace("\/","/")
        return parseString( xmlData  ).getElementsByTagName('text')[0].firstChild.data



class CleanupWikiText(object):
    """ cleans wiki text """

    @staticmethod
    def removeLanguageReferences(text):
        cleaned = []
        for line in text.split("\n"):
            if line.startswith("<!--") and "Other languages" in line:
               break
            cleaned.append(line)

        return "\n".join(cleaned)
        


class TestWikiPedia(object):
    """ tests the WikiPedia Class """
    TEST_QUERIES= { 
                ('Energy', 'en'):  ('fossil', 'renewable'),
                ('Energie', 'de'): ('kinetisch', 'Verbrauch', "Atom"),
                 }

    def testRetrievePage(self):
        """ tries to retrieve the following url's from the list """

        w = WikiPedia()
        for (keyword, lang), searchTerms in self.TEST_QUERIES.iteritems():
            wikiPediaText = w.getWikiPage(keyword, lang=lang)
            for term in searchTerms:
                print keyword, term
                assert term in wikiPediaText


def test( term1, term2):
    w = WikiPedia()
    text1 = w.getWikiPage(term1, 'en')
    text2 = w.getWikiPage(term2, 'en')
    return term1 in text2 or term2 in text1

if __name__ == '__main__':
    w=WikiPedia()
    # text = w.getWikiPage("Energy", "en")
    # text = w.getWikiPage("Greenhouse Gas", "en")

    
    print w._getPageNameAlterations("Greenhouse Gas Emissions")
    #print test('Greenhouse Gsa Emissions', 'Emissions')
    print test('Oil', 'Fossil Fuels')

    # print CleanupWikiText.removeLanguageReferences( text )

