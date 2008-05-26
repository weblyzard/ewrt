#!/usr/bin/env python

""" descriptor.py
    this module assigns descriptors to terms based on wikipedia queries """

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

from access.http import Retrieve
from urllib import quote

WIKIPEDIA_SEARCH_QUERY = 'http://%s.wikipedia.org/w/index.php?title=Special%%3ASearch&search=%s&ns0=1&fulltext=Search'

class Descriptor(object):
    """ returns the descriptor of an object based on a wikipedia
        query """

    
    @staticmethod
    def getDescriptor(synonym, lang='en'):
        """ returns the descriptor for the given synonym in the diven language """
        assert( len(lang)==2 )
        result = Descriptor.getWikipediaSearchResults(synonym, lang)
        return result[0]


    @staticmethod
    def getWikipediaSearchResults(term, lang):
        """ returns a list of wikipedia search results for the given term """
        search_query = WIKIPEDIA_SEARCH_QUERY % (lang, quote(term) )
        f=Retrieve( Descriptor.__name__ ).open(search_query)
        results = Descriptor._parse_wikipedia_search_results( f.read() )
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


if __name__ == '__main__':
    
    from unittest import TestCase, main

    class TestDescriptor(TestCase):
        """ tests the http class """
        TEST_TERMS = { 'Pope Benedict XVI': ('pope benedict', 'ratzinger', 'joseph ratzinger'),
                       'Wolfgang Amadeus Mozart': ('amadeus', 'wolfgang amadeus'), 
                     }

        def testDescriptor(self):
            """ tries to retrieve the following url's from the list """

            for descriptor, synonyms in self.TEST_TERMS.iteritems():
                for synonym in synonyms:
                    self.assertEqual( descriptor, Descriptor.getDescriptor(synonym) )


    main()

