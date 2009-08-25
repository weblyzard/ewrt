#!/usr/bin/env python

""" uses the del.icio.us API to access information about del.icio.us URLs """

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

import sys
import re
from eWRT.access.http import Retrieve
from eWRT.ws.TagInfoService import TagInfoService
from urlparse import urlsplit
from md5 import md5
from eWRT.config import DELICIOUS_USER, DELICIOUS_PASS

class Delicious(TagInfoService):
    """ retrieves data using the del.icio.us API """
    
    DELICIOUS_SERVICE_URL = "http://del.icio.us/url/%s"
    DELICIOUS_TAG_URL = "http://delicious.com/tag/%s"
    RE_COUNT = re.compile("this url has been saved by (\d+) people")
    RE_TAG_COUNT = re.compile("<p>(\d+) Bookmarks</p></div>")

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

        url = Delicious.DELICIOUS_TAG_URL % "+".join(tags)        
        content = Delicious.get_content(url)
        return Delicious._parse_tag_counts(content)

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
    def _parse_tag_counts( content ):
        """ parses del.icio.us's html content and returns the number of counts for the tags """
        m=Delicious.RE_TAG_COUNT.search( content )
        if m:
            return m.group(1)
        else:
            return 0

    @staticmethod
    def _normalize_url(url):
        """ prepares a url for the usage by delicious"""
        if not url.endswith("/"):
            url += "/"
        return url

    # heinz: todo remove or adopt???
    @staticmethod
    def delicious_info_retrieve( url ):
        assert( url.startswith("http") )

        md5_url = md5( Delicious._normalize_url(url)).hexdigest()
        request = Delicious.DELICIOUS_SERVICE_URL % md5_url

        f = Retrieve(Delicious.__name__).open(request)
        content = f.read()
        f.close()

        return Delicious._parse_counts(content)
    
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
    print Delicious.delicious_get_content( url )
    print Delicious.getUrlInfo( url ), "counts"
    print Delicious.getTagInfo( ("debian", "linux") ), "counts"

