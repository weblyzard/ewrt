from eWRTlibs.tango.tango import tango
import oauth

from eWRT.access.http import Retrieve
from eWRT.ws.TagInfoService import TagInfoService
from eWRT.ws.twitter import Twitter
import json
import re
import unittest

import warnings

warnings.warn("Class TwitterTrends is deprecated, use eWRT.ws.twitter instead ", category=DeprecationWarning)

class TwitterTrends(TagInfoService):

    TWITTER_SEARCH_URL = 'http://search.twitter.com/search.json?q=&tag=%s&lang=all&rpp=100'

    def __init__(self):
        """ init connects to Twitter """
        Twitter.__init__()

    def getDailyTrends(self):
        """ getDailyTrends fetches the daily trends of twitter
             @return trends """
        return Twitter.getDailyTrends() 

    @staticmethod
    def getRelatedTags( tags ):
        """ fetches the related tags for the given tags
            @param list of tags
            @return dictionary of related tags with count
        """
        return Twitter.getRelatedTags( tags)

class TwitterTest( unittest.TestCase ):

    TWITTER_TEST_TAGS = ['linux', ('linux', 'debian')]

    def test_url_info(self):
        for tag in self.TWITTER_TEST_TAGS:
            print '%s has %s counts '% (tag, TwitterTrends.getRelatedTags(tag))

if __name__ == '__main__':
   TwitterTrends.getRelatedTags('linxu') 
