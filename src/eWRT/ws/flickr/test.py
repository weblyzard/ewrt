#!/usr/bin/env python

""" unittests covering the del.icio.us functions provided by eWRT """

# (C)opyrights 2009 by Heinz Lang <heinz.lang@wu.ac.at> 
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


from __init__ import Flickr
import unittest

FLICKR_TEST_TAGS = [("berlin",), ("vienna",), ("vienna", "prater")]
FLICKR_TEST_RELATED_TAGS = ["berlin dom", "vienna"]

class FlickrTest( unittest.TestCase ):


    def test_tag_info(self):
        print '### Testing tag_info ###'
        for tags in FLICKR_TEST_TAGS:
            print '%s has %s counts ' % (tags, Flickr.getTagInfo( tags ))

    
    def test_related_tags(self):
        print '### Testing related_tags ###'
        for tags in FLICKR_TEST_RELATED_TAGS:
            print '%s has related tags: %s' % (tags, Flickr.getRelatedTags( tags ))

if __name__ == '__main__':
    unittest.main()

