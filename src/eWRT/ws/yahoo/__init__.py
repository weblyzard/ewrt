#!/usr/bin/env python

""" @package eWRT.ws.yahoo
    support for the yahoo! search 
    
    @remarks
    this module is based on yahoo's boss search service 
"""

# (C)opyrights 2008-2010 by Albert Weichselbraun <albert@weichselbraun.net>
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
from urllib import urlopen, urlencode, quote
from eWRT.ws.TagInfoService import TagInfoService
from eWRT.config import YAHOO_APP_ID, YAHOO_SEARCH_URL
from eWRT.input.conv.html import HtmlToText
from urllib2 import URLError
from nose.plugins.attrib import attr
from socket import setdefaulttimeout
setdefaulttimeout(60)


class Yahoo(TagInfoService):
    """ interfaces with yahoo's search service 
        * Search: Yahoo! BOSS
          (see http://developer.yahoo.com/search/boss)
    """
    __slots__ = ('r', )

    def __init__(self):
        self.r = Retrieve( Yahoo.__name__, sleep_time=0 )

    def query(self, terms, count=0, queryParams={} ):
        """ returns search results for the given terms
            @param[in] terms       ... a list of search terms
            @param[in] count       ... number of results to return (0 if we are
                                       interested on the search meta data only).
            @param[in] queryParams ... a dictionary of query parameters to add to
                                          the request
            @returns the search results
        """
        assert ( isinstance(terms, tuple) or isinstance(terms, list) )
        queryParams.update( {'appid': YAHOO_APP_ID,
                             'count': count,
                             'format': 'json'
        } )
        params = urlencode( queryParams )
        url = YAHOO_SEARCH_URL % "%2B".join(map( quote, terms) ) +"?"+ params
        print url
        try:
            result = eval( self.r.open(url).read().replace("\\/", "/" ))
            return result['ysearchresponse']
        except URLError:
            return ""

    @staticmethod
    def getSearchResults(query_result):
        """ returns a list of all search results returned by the given
            query result.
            @param[in] query_result     Result of the query
        """
        return [ YahooSearchResult(r) for r in query_result['resultset_web'] ] \
           if 'resultset_web' in query_result else []


    def getTagInfo(self, tag):
        """ @Override """
        return int( self.query(tag)['totalhits'] )


class YahooSearchResult(object):
    """ Perfom manipulations on yahoo search results """

    __slots__ = ('search_result')

    def __init__(self, search_result):
        """ @param[in] search_result ... search result to query """
        self.search_result = search_result

    def getKeywords(self):
        """ @returns the keywords for the given search_result """
        return self.search_result['keywords']['terms']

    def getPageContent(self):
        """ @returns the content of the found web page """
        return urlopen( self.search_result['url'] ).read()

    def getPageText(self):
        """ @returns the text of the found web page """
        try:
            return HtmlToText.getText( self.getPageContent() )
        except:
            return ""

class TestYahoo(object):
    """ tests the yahoo search API """

    SEARCH_QUERIES = {
        'energy': ( ('energy', 'coal'), ('energy', 'sustainable') ),
        'latex' : ( ('latex', 'bibtex'), ('latex', 'knutz') )
    }

    def __init__(self):
        self.y = Yahoo()

    @attr("remote")
    def testSearchCounts(self):
        for query, refinedQueries in self.SEARCH_QUERIES.iteritems():
            qCount = int(self.y.query( (query, ) )['totalhits'])

            for q in refinedQueries:
                print query, q, "**",qCount, int(self.y.query( q )['totalhits'])
                assert qCount > int(self.y.query( q )['totalhits'])
    
    @attr("remote")
    def testTagInfo(self):
        """ tests the tag info service """
        assert self.y.getTagInfo( ('weblyzard',)) > 10
        assert self.y.getTagInfo( ('a_query_which_should_not_appear_at_all', )) == 0

    @attr("remote")
    def testYahooSearchResult(self):
        """ tests the Yahoo Search Result objects """
        for resultSite in Yahoo.getSearchResults(self.y.query( ("linux", "firefox", ),  \
                            count=1, queryParams={'view':'keyterms', 'abstract': 'long'} )):

            print resultSite.search_result['keyterms']['terms']
            assert len( resultSite.getPageText() ) > len(resultSite.search_result['abstract'])
            assert 'http' in resultSite.search_result['url']

    @attr("remote")
    def testBorderlineYahooSearchResult(self):
        """ tests borderline cases such as empty search results """
        assert len( Yahoo.getSearchResults(self.y.query( ('ksdaf', 'sadfj93', 'kd9', ), count=10, queryParams={'view':'keyterms', 'abstract': 'long'}) ) ) == 0

    @attr("remote")
    def testMultiProcessingRetrieve(self):
        """ tests the multi processing capabilities of this module """
        from multiprocessing import Pool
        p = Pool(4)

        TEST_URLS = ['http://www.derstandard.at', 
                     'http://www.dilbert.com',
                     'http://www.wetter.at',
                     'http://www.wu.ac.at',
                     'http://www.ai.wu.ac.at',
                     'http://www.tuwien.ac.at',
                     'http://www.boku.ac.at',
                     'http://www.univie.ac.at',
                    ]
        # f=open("/tmp/aw", "w")
        for res in p.map( p_fetchWebPage, TEST_URLS ):
            # f.write(res)
            # f.write("\n-----\n\n\n")
            assert len(res) > 20
        # f.close()

    @attr("remote")
    def testFailingUrls(self):
        """ tests the module with URLs known to fail(!) """
        TEST_URLS = ['http://www.mfsa.com.mt/insguide/english/glossarysearch.jsp?letter=all',
                    ]
        for url in TEST_URLS:
            assert len( p_fetchWebPage(url).strip() ) > 0



def p_fetchWebPage(url):
    """ fetches the web page specified in the given yahoo result object
        @param[in] url the url to fetch

        @remarks
        helper function for the testMultiProcessing test
    """
    r = YahooSearchResult( {'url': url} )
    return r.getPageText()


if __name__ == '__main__':
    y = Yahoo()
    #print y.query( ("energy",) )
    #print y.query( ("energy", "coal") )
    #print y.query( ("d'alembert", "law") )
    r = y.query( ("linux", "python", ), count=5, queryParams={'view': 'keyterms', 'abstract': 'long'} )
    print "***", r
    for entry in r['resultset_web']:
        print entry.keys()
        print entry['keyterms']['terms']
        print entry['url']
        print entry['abstract']


