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
from urllib import urlencode
from eWRT.config import YAHOO_APP_ID

YAHOO_TERM_EXTRACTION_URI = 'http://search.yahooapis.com/ContentAnalysisService/V1/termExtraction'

class YahooTermExtractor(object):
    """ interfaces with yahoo's search service 
        * Term extraction: extract terms from yahoo search
          http://developer.yahoo.com/search/content/V1/termExtraction.html
    """
    __slots__ = ('r', )

    def __init__(self):
        self.r = Retrieve( YahooTermExtractor.__name__ )

    def extractTerms(self, content):
        """ extract terms from yahoo search, see http://developer.yahoo.com/search/content/V1/termExtraction.html """ 

        params = urlencode( {'appid': YAHOO_APP_ID,
                             'context': content,
                             'output': 'json'
        })
        result = eval ( self.r.open(YAHOO_TERM_EXTRACTION_URI, params).read() )
        return result['ResultSet']['Result']


class TestYahooTermExtractor(object):
    """ tests the yahoo search API """

    def __init__(self):
        self.y = YahooTermExtractor()

    def testExtractTerms(self):
        """ tests the yahoo term extraction interface """
        text = ''' 
            appid       string (required)       The application ID. See Application IDs for more information.
            context     string (required)     The context to extract terms from (UTF-8 encoded).
            query     string     An optional query to help with the extraction process.
            output     string: xml (default), json, php     The format for the output. If json is requested, the results will be returned in JSON format. If php is requested, the results will be returned in Serialized PHP format.
            callback     string     The name of the callback function to wrap around the JSON data. The following characters are allowed: A-Z a-z 0-9 . [] and _. If output=json has not been requested, this parameter has no effect. More information on the callback can be found in the Yahoo! Developer Network JSON Documentation. ''' 

        keywords = self.y.extractTerms(text)
        assert 'json' in keywords
        assert 'yahoo developer network' in keywords
        assert 'the' not in keywords
        assert 'for' not in keywords

