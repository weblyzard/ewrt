#!/usr/bin/env python

""" yahoo! - uses yahoo's boss search service """

# (C)opyrights 2008-2009 by Albert Weichselbraun <albert@weichselbraun.net>
#                           Heinz Peter Lang <hplang@langatium.net>
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
from urllib import urlencode, quote
from eWRT.ws.TagInfoService import TagInfoService
from eWRT.config import YAHOO_APP_ID, YAHOO_SEARCH_URL

class Yahoo(TagInfoService):
    """ interfaces with yahoo's search service """

    __slots__ = ('r', )

    YAHOO_TERM_EXTRACTION_URI = 'http://search.yahooapis.com/ContentAnalysisService/V1/termExtraction'

    def __init__(self):
        self.r = Retrieve( Yahoo.__name__ )

    def query(self, terms, count=0):
        """ returns search results for the given terms
            @param[in] terms ... a list of search terms
            @param[in] count ... number of results to return (0 if we are
                                 interested on the search meta data only).
            @returns the search results
        """
        assert ( isinstance(terms, tuple) or isinstance(terms, list) )
        params = urlencode( {'appid': YAHOO_APP_ID,
                             'count': count,
                             'format': 'json'
        })
        url = YAHOO_SEARCH_URL % "%2B".join(map( quote, terms) ) +"?"+ params
        result = eval( self.r.open(url).read() )

        return result['ysearchresponse']
    
    def getTagInfo(self, tag):
        """ @Override """
        return int( self.query(tag)['totalhits'] )

    def extractTerms(self, content):
        """ extract terms from yahoo search, see http://developer.yahoo.com/search/content/V1/termExtraction.html """ 

        params = urlencode( {'appid': YAHOO_APP_ID,
                             'context': content,
                             'output': 'json'
        })
        result = eval ( self.r.open(self.YAHOO_TERM_EXTRACTION_URI, params).read() )
        return result['ResultSet']['Result']


class TestYahoo(object):
    """ tests the yahoo search API """

    SEARCH_QUERIES = {
        'energy': ( ('energy', 'coal'), ('energy', 'sustainable') ),
        'latex' : ( ('latex', 'bibtex'), ('latex', 'knutz') )
    }

    def __init__(self):
        self.y = Yahoo()

    def testSearchCounts(self):
        for query, refinedQueries in self.SEARCH_QUERIES.iteritems():
            qCount = int(self.y.query( (query, ) )['totalhits'])

            for q in refinedQueries:
                print query, q, "**",qCount, int(self.y.query( q )['totalhits'])
                assert qCount > int(self.y.query( q )['totalhits'])
    
    def testTagInfo(self):
        """ tests the tag info service """
        assert self.y.getTagInfo( ('weblyzard',)) > 10
        assert self.y.getTagInfo( ('a_query_which_should_not_appear_at_all', )) == 0




if __name__ == '__main__':
    y = Yahoo()
    print y.query( ("energy",) )
    print y.query( ("energy", "coal") )
    print y.query( ("d'alembert", "law") )

    text = ''' 
        appid       string (required)       The application ID. See Application IDs for more information.
        context     string (required)     The context to extract terms from (UTF-8 encoded).
        query     string     An optional query to help with the extraction process.
        output     string: xml (default), json, php     The format for the output. If json is requested, the results will be returned in JSON format. If php is requested, the results will be returned in Serialized PHP format.
        callback     string     The name of the callback function to wrap around the JSON data. The following characters are allowed: A-Z a-z 0-9 . [] and _. If output=json has not been requested, this parameter has no effect. More information on the callback can be found in the Yahoo! Developer Network JSON Documentation. ''' 

    print y.extractTerms(text)
