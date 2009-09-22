from eWRTlibs.tango.tango import tango
import oauth

from eWRT.access.http import Retrieve
from eWRT.ws.TagInfoService import TagInfoService
import json
import re
import unittest

class Twitter(TagInfoService):

    TWITTER_SEARCH_URL = 'http://search.twitter.com/search.json?q=&tag=%s&lang=all&rpp=100'

    def __init__(self):
        """ init connects to Twitter """
        self.twitter = tango.setup();

    def getDailyTrends(self):
        """ getDailyTrends fetches the daily trends of twitter
             @return trends """
        return self.twitter.getDailyTrends() 

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
            found_tags.extend(re.findall('#(\w+)', result['text'], re.IGNORECASE|re.DOTALL))

        for tag in found_tags:
            related_tags[tag.lower()] = related_tags.get(tag.lower(), 0) + 1

        return related_tags


class TwitterTest( unittest.TestCase ):

    TWITTER_TEST_TAGS = ['linux', ('linux', 'debian')]

    def test_url_info(self):
        for tag in self.TWITTER_TEST_TAGS:
            print '%s has %s counts '% (tag, Twitter.getRelatedTags(tag))

if __name__ == '__main__':
    print Twitter.getRelatedTags('linux')
    #unittest.main()
