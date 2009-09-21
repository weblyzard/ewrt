#!/usr/bin/env python

""" uses the del.icio.us API to access information about del.icio.us URLs """

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

import sys
import re
from eWRT.access.http import Retrieve
from eWRT.ws.TagInfoService import TagInfoService
from urlparse import urlsplit
from HTMLParser import HTMLParser

try:
    from hashlib import md5
except ImportError:
    from md5 import md5
from eWRT.config import DELICIOUS_USER, DELICIOUS_PASS

class Delicious(TagInfoService):
    """ retrieves data using the del.icio.us API """
    
    DELICIOUS_SERVICE_URL = "http://del.icio.us/url/%s"
    DELICIOUS_TAG_URL = "http://delicious.com/tag/%s"
    RE_COUNT = re.compile("<p>(\d+) Bookmarks</p></div>")

    __slots__ = ()

    @staticmethod
    def getUrlInfo( url ):
        """ @param   url 
            @returns the number of bookmarks for the given url """
        return Delicious.delicious_info_retrieve( url )

    @staticmethod
    def getTagInfo( tags ):
        """ @param   tags   A list of tags to retrieve information for
            @returns        the number of bookmarks using the given tags
        """

        url = Delicious._parse_tag_url(tags)
        content = Delicious.get_content(url)
        return Delicious._parse_counts(content)

    @staticmethod
    def getRelatedTags( tags ):
        """ returns a the count of related tags 
            @param list/tuple of tags 
            @returns list of related tags with a count of their occurence """

        content = Delicious.get_content(Delicious._parse_tag_url(tags))

        related_tags = re.findall('class="m relatedTag" title="">(\w*?)<em>', content, re.IGNORECASE|re.DOTALL)
        related_tags_with_count = []

        for tag in related_tags:
            related_tags_with_count.append((tag, Delicious.getTagInfo(tag)))
            
        return related_tags_with_count

    # 
    # helper functions
    #
    @staticmethod
    def _parse_counts( content ):
        """ parses del.icio.us's html content and returns the number of counts """
        m=Delicious.RE_COUNT.search( content )
        if m:
            return m.group(1)
        else:
            return 0

    @staticmethod
    def _parse_tag_url( tags ):
        """ parses the tag url, removes white spaces in the tags ...
            @param tuple/list of tags 
            @returns delicious tag url
        """        
        if len([ tag for tag in tags if ' ' in tag ]):
            raise ValueError('Tags must not contain white spaces!')
        else:
            return Delicious.DELICIOUS_TAG_URL % "+".join(tags)        

    @staticmethod
    def _normalize_url(url):
        """ prepares a url for the usage by delicious"""
        if not url.endswith("/"):
                url += "/"
        return url

    @staticmethod
    def delicious_info_retrieve( url ):
        assert( url.startswith("http") )

        md5_url = md5( Delicious._normalize_url(url)).hexdigest()
        request = Delicious.DELICIOUS_SERVICE_URL % md5_url
        return Delicious._parse_counts( Delicious.get_content(request) )
    
    @staticmethod
    def get_content( url ):
        """ returns the content from delicious """
        assert( url.startswith("http") )

        f = Retrieve(Delicious.__name__).open(url)
        content = f.read()
        f.close()
        return content


if __name__ == '__main__':

    url = sys.argv[1].strip()
    print Delicious.getUrlInfo( url ), "counts"
    print Delicious.getTagInfo( ("debian", "linux") ), "counts"
    print Delicious.getRelatedTag( ("debian", "linux") ), "counts"
