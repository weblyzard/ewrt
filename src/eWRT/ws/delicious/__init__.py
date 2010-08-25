#!/usr/bin/env python

""" uses the del.icio.us API to access information about del.icio.us URLs """

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

import re
from eWRT.access.http import Retrieve
from eWRT.ws.TagInfoService import TagInfoService
from urllib import quote
import urllib2
from time import sleep
from hashlib import md5

from nose.plugins.attrib import attr
#from eWRT.config import DELICIOUS_USER, DELICIOUS_PASS

class Delicious(TagInfoService):
    """ retrieves data using the del.icio.us API """
    
    DELICIOUS_SERVICE_URL = "http://del.icio.us/url/%s"
    DELICIOUS_TAG_URL = "http://delicious.com/tag/%s"
    RE_COUNT = re.compile("<p>(\d+) Bookmarks</p></div>")

    NEXT_EXP = re.compile('\?page=(\S+)\" class=\"pn next\">Next')
    MAX_PAGES = 0 # set to zero if pages should not be iterated
    

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
        assert( isinstance(tags, tuple) or isinstance(tags, list) )
        url = Delicious._parse_tag_url(tags)
        try:
            content = Delicious._get_content(url)
            return Delicious._parse_counts(content)
        except urllib2.HTTPError:
            return 0

    @staticmethod
    def getRelatedTags( tags, retrieveTagInfo=False, pageNum=0 ):
        """ returns related tags for the given ones.
            @param  tags             list of tags
            @param  retrieveTagInfo  determines whether we will retrieve the tagInfo for the related tags
            @returns                 list of related tags 
        """

        assert( isinstance(tags, tuple) or isinstance(tags, list) )
        tag_url = Delicious._parse_tag_url( tags )

        if not pageNum == 0:
            tag_url = '%s?page=%s' % (tag_url, pageNum)

        content = Delicious._get_content( tag_url )

        m = Delicious.NEXT_EXP.search(content)

        related_tags = (Delicious._getNGramRelatedTags( content ) if '+' in tag_url else Delicious._getMonogramRelatedTags( content ))
        related_tags_with_count = [ (tag, Delicious.getTagInfo( (tag,) ) if retrieveTagInfo else None) for tag in related_tags ]

        # also find the tags in the next pages       
        if m and int(pageNum) < Delicious.MAX_PAGES:
            related_tags_with_count.extend( Delicious.getRelatedTags(tags, pageNum=m.group(1)) )

        return related_tags_with_count

    @staticmethod
    def _getMonogramRelatedTags( content ):
        """ Returns the related tags for the given monogram.
            @param content of the tag's page
            @return a list of related tags

            @remark
            this method parses the delicious "Related Tags" box.
        """
        return re.findall('<span class="m" title="(\w*?)">', content, re.IGNORECASE|re.DOTALL)

    @staticmethod
    def _getNGramRelatedTags( content ):
        """ Returns the related tags for the given n-gram.
            @param content of the tags' page
            @return a list of related tags

            @remark
            this method retrieves all other tags from the page and sorts
            them by the number of occurrences.
        """
        return re.findall('<span class="(?:tag-chain-item-span|tagItem)">(\w*?)</span>', content, re.IGNORECASE|re.DOTALL)
 
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
        tags = [quote(tag.replace(" ", "+"), safe="+") for tag in tags ]        
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
        return Delicious._parse_counts( Delicious._get_content(request) )
    
    @staticmethod
    def _get_content( url ):
        """ returns the content from delicious """
        assert( url.startswith("http") )

        f = Retrieve(Delicious.__name__).open(url)
        content = f.read()
        f.close()
        sleep(1)
        return content

class TestDelicious(object):

    RELATED_TAGS_DELICIOUS_PAGE = './test/delicious_climate_related_tags.html'
    
    def testTagSplitting(self):
        """ verifies the correct handling of tags containing spaces
            i.e. (t1, t2, t3) == (t1, "t2 t3") """
        d = Delicious._parse_tag_url
        print d( ("debian linux") )
        assert d( ("debian", "linux" )) == d( ("debian linux", ) )
        assert d( ("t1", "t2", "t3") ) == d( ("t1", "t2 t3") )

    def testNGramRelatedTags(self):
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
    def testCriticalTagNames(self):
        """ tests tag names which contain slashes, quotes, etc """
        assert Delicious.getTagInfo( ("consequence/frequency matrix", ) ) != None
        assert Delicious.getTagInfo( ("it's", )) != None





if __name__ == '__main__':

#    url = sys.argv[1].strip()
#    print Delicious.getUrlInfo( url ), "counts"
#    print Delicious.getTagInfo( ("debian", "linux") ), "counts"
#    print Delicious.getRelatedTag( ("debian", "linux") ), "counts"
    print Delicious.getTagInfo( ("debian", "linux") ), "counts"
    print Delicious.getRelatedTags(('debian', 'linux'))
