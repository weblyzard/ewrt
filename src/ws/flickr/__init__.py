#!/usr/bin/env python

""" uses flickr """

# (C)opyrights 2008 by Albert Weichselbraun <albert@weichselbraun.net>
# (C)opyrights 2009 by Heinz Lang <heinz@langatium.net>
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

class Flickr(TagInfoService):
    """ retrieves data using the del.icio.us API """
    FLICKR_TAG_URL = "http://www.flickr.com/search/?w=all&q=%s&m=tags" 
    RE_TAG_COUNT = re.compile('var page_pagination_count = (\d+);')
    # RE_TAG_COUNT = re.compile('<div class="Results">\((\d+) results\)</div>')

    @staticmethod
    def getTagInfo( tags ):
        """ @param   tags   A list of tags to retrieve information for
            @returns        the number of bookmarks using the given tags
        """

        url = Flickr.FLICKR_TAG_URL % "+".join(tags)        
        print url
        content = Flickr.get_content(url)
        return Flickr._parse_tag_counts(content)

    # 
    # helper functions
    #
    @staticmethod
    def _parse_tag_counts( content ):
        """ parses flickrs html content and returns the number of counts for the tags """
        m=Flickr.RE_TAG_COUNT.search( content )
        if m:
            return m.group(1)
        else:
            return 0

    @staticmethod
    def get_content( url ):
        """ returns the content from Flickr """
        assert( url.startswith("http") )

        f = Retrieve(Flickr.__name__).open(url)
        content = f.read()
        f.close()
        return content

if __name__ == '__main__':
    print Flickr.getTagInfo( ("peugeot 206", "206") ), "counts"

