#!/usr/bin/env python

""" __init__.py
    retrieves WikiPedia articles """

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

from future import standard_library
standard_library.install_aliases()
from builtins import object
__version__ = "$Header$"

from urllib.parse import quote
from urllib.error import HTTPError

from eWRT.access.http import Retrieve


WIKIPEDIA_SEARCH_QUERY = 'http://%s.wikipedia.org/wiki/%s'

class WikiPedia(object):
    """ returns a wikipedia article """

    def __init__(self):
        self.r = Retrieve( WikiPedia.__name__ )
    
    def getDescriptor(self, synonym, lang='en'):
        """ returns the descriptor for the given synonym in the diven language """
        assert( len(lang)==2 )
        try:
            result = self.getWikipediaSearchResults(synonym, lang)
            return result[0]
        except (HTTPError, IndexError):
            return None


    def getWikipediaSearchResults(self, term, lang):
        """ returns a list of wikipedia search results for the given term 
            or None if nothing was found 
        """
        search_query = WIKIPEDIA_SEARCH_QUERY % (lang, quote(term) )
        f=self.r.open(search_query)
        results = WikiPedia._parse_wikipedia_search_results( f.read() )
        f.close()

        return results

    @staticmethod
    def _parse_wikipedia_search_results( text ):
        result = []
        for line in text.split("\n"):
            # only consider lines containing search results
            if not "class='searchresult'" in line: continue

            (prefix, tmp) = line.split("title=\"", 1)
            (descriptor, suffix ) = tmp.split("\"", 1)

            result.append(descriptor)

        return result
