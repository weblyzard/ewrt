#!/usr/bin/env python

from eWRT.access.http import Retrieve
from eWRT.ws.TagInfoService import TagInfoService
import re

class Twitter(TagInfoService):

    TWITTER_SEARCH_URL = 'http://search.twitter.com/search.json?q=&tag=%s&lang=all&rpp=100'
    RE_FIND_TAGS = re.compile('#(\w+)', re.IGNORECASE|re.DOTALL)

    @staticmethod
    def getRelatedTags( tags ):
        """ fetches the related tags for the given tags
            @param list of tags
            @return dictionary of related tags with count
        """

        if type(tags).__name__ == 'str':
            url = Twitter.TWITTER_SEARCH_URL % tags
        else:   
            url = Twitter.TWITTER_SEARCH_URL % "+".join(tags)

        f = Retrieve(Twitter.__name__).open(url)

        # convert json into dict and remove null values with ""
        search_results = eval(re.sub('null', '""', f.read()))
        found_tags = []
        related_tags = {}

        for result in search_results['results']:
            found_tags.extend(Twitter.RE_FIND_TAGS.findall( result['text']))

        for tag in found_tags:
            related_tags[tag.lower()] = related_tags.get(tag.lower(), 0) + 1

        # todo: sort

        return related_tags
    
    @staticmethod
    def getDailyTrends():
        raise NotImplementedError


class TwitterTest( object ):

    TWITTER_TEST_TAGS = [ 'linux', ('linux', 'debian') ]

    def testUrlInfo(self):
        for tag in self.TWITTER_TEST_TAGS:
            relTags = Twitter.getRelatedTags(tag)
            print 'related to %s are %s.'% (tag, relTags )

