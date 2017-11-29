#!/usr/bin/env python

""" unittests covering the del.icio.us functions provided by eWRT """

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

import unittest

from nose.plugins.attrib import attr

from eWRT.ws.delicious import Delicious


DELICIOUS_TEST_URLS = ( 'http://www.iaeste.at', 'http://www.wu-wien.ac.at', 'http://www.heise.de', 
                        'http://www.kurier.at', 'http://news.bbc.co.uk', )

DELICIOUS_TEST_TAGS = [("linux",), ("information",), ("information", "retrieval"),("linux", "debian"),("algore",)]

RELATED_TAGS_DELICIOUS_PAGE = './data/delicious_climate_related_tags.html'
    
class TestDelicious(unittest.TestCase):

    def test_url_info(self):
        for url in DELICIOUS_TEST_URLS:
            print '%s has %s counts '% (url, Delicious.delicious_info_retrieve(url))

    def test_tag_info(self):
        print '### Testing tag_info ###'
        for tags in DELICIOUS_TEST_TAGS:
            print '%s has %s counts ' % (tags, Delicious.getTagInfo( tags ))

    
    def test_related_tags(self):
        print '### Testing related_tags ###'
        for tags in DELICIOUS_TEST_TAGS:
            print '%s has related tags: %s' % (tags, Delicious.getRelatedTags( tags ))
    
    def test_tag_splitting(self):
        """ verifies the correct handling of tags containing spaces
            i.e. (t1, t2, t3) == (t1, "t2 t3") """
        d = Delicious._parse_tag_url
        print d( ("debian linux") )
        assert d( ("debian", "linux" )) == d( ("debian linux", ) )
        assert d( ("t1", "t2", "t3") ) == d( ("t1", "t2 t3") )

    def test_ngram_related_tags(self):
        """ tests support for related tags for n-grams """
        assert len( Delicious().getRelatedTags( ("climate", "change") ) ) > 0

        content = open( TestDelicious.RELATED_TAGS_DELICIOUS_PAGE ).read()
        related_tags = Delicious._getNGramRelatedTags( content )

        assert 'global' in related_tags
        assert 'evidence' in related_tags
        assert 'vegetarian' in related_tags
        assert 'sustainability' in related_tags

        assert 'linux' not in related_tags

    @attr("remote")
    def test_critical_tag_names(self):
        """ tests tag names which contain slashes, quotes, etc """
        assert Delicious.getTagInfo( ("consequence/frequency matrix", ) ) != None
        assert Delicious.getTagInfo( ("it's", )) != None

if __name__ == '__main__':
    unittest.main()
