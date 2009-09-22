#!/usr/bin/env python

# (C)opyrights 2008-2009 by Albert Weichselbraun <albert@weichselbraun.net>
#                           Heinz-Peter Lang <heinz@langatium.net>
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

import sys
import re
from eWRT.access.http import Retrieve
from eWRT.ws.TagInfoService import TagInfoService
from urlparse import urlsplit
from eWRT.config import TECHNORATI_API_KEY
import xml.sax

import unittest

class Technorati(TagInfoService):
    """ retrieves data using the del.icio.us API """
    TECHNORATI_URL = 'http://api.technorati.com/tag?key='+TECHNORATI_API_KEY+'&tag=%s' 
    TECHNORATI_URL = 'http://technorati.com/r/tag/%s?authority=n&language=n'
    #RE_TAG_COUNT = re.compile('<postsmatched>(\d+)</postsmatched>')
    RE_TAG_COUNT = re.compile('<span class="count">\((\S+)\)</span>')

    __slots__ = ()

    @staticmethod
    def getTagInfo( tags ):
        """ @param   tags   A list of tags to retrieve information for
            @returns        the number of bookmarks using the given tags
        """
        url = Technorati._parseURL(tags)
        content = Technorati.get_content(url)

        return Technorati._parse_tag_counts(content)

    @staticmethod
    def test ():
        print Technorati.TECHNORATI_URL

    @staticmethod
    def getRelatedTags( tags, withCounts = True ):
        """ @param tags - list of tags
            @param booelan withCounts to print counts for tags
            @return list of related tags 
        """
        url = Technorati._parseURL(tags)

        content = Technorati.get_content(url)
        tag_container = re.findall('<div id="related-tags".*?<ul>(.*?)</ul>.*?</div>', content, re.IGNORECASE|re.DOTALL)
        related_tags_with_count = []

        if len(tag_container) > 0:

            related_tags = re.findall('<a.*?">(.*?)</a>', tag_container[0], re.IGNORECASE | re.DOTALL)

            if withCounts:
                for tag in related_tags:
                    tag = re.sub(' ', '-', tag)
                    related_tags_with_count.append((tag, Technorati._getRelatedTagCount(tags, tag)))
                
                return related_tags_with_count

            else:
                return related_tags
        


    # 
    # helper functions
    #
    @staticmethod
    def _parse_tag_counts( content ):
        """ parses flickrs html content and returns the number of counts for the tags """
        m = Technorati.RE_TAG_COUNT.search( content )
        if m:
            return re.sub(',', '', m.group(1))
        else:
            return 0

    @staticmethod
    def _getRelatedTagCount( tags, filter ):
        """ returns the related tag count
            @param tags - list of tags
            @param filtered tag
            @return count of related tag """

        url = Technorati._parseURL(tags, filter)
        content = Technorati.get_content(url)
        return Technorati._parse_tag_counts(content)

    @staticmethod
    def _parseURL( tags, filter=''):
        """ parses the URL """

        if type(tags).__name__ == 'str':
            url = Technorati.TECHNORATI_URL % tags
        else:   
            url = Technorati.TECHNORATI_URL % "+".join(tags)

        if filter == '':
            return url
        else:
            return '%s&filter=%s' % ( url, filter )


    @staticmethod
    def get_content( url ):
        """ returns the content from Technorati """
        print url
        assert( url.startswith("http") )
        f = Retrieve(Technorati.__name__).open(url)
        content = f.read()
        f.close()
        return content
