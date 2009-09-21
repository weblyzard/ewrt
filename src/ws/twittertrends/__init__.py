from eWRTlibs.tango.tango import tango
import oauth

from eWRT.access.http import Retrieve
from eWRT.ws.TagInfoService import TagInfoService
import json

## @package TwitterTrends
class Twitter(TagInfoService):

    TWITTER_SEARCH_URL = 'http://search.twitter.com/search.json?q=&tag=%s&lang=all'

    # init connects to Twitter
    def __init__(self):
        self.twitter = tango.setup();

    # getDailyTrends fetches the daily trends of twitter
    # @return trends
    def getDailyTrends(self):
        return self.twitter.getDailyTrends() 

    @staticmethod
    def getRelatedTags( tags ):
        url = Twitter.TWITTER_SEARCH_URL % "+".join(tags)
        f = Retrieve(Twitter.__name__).open(url)
        search_result = f.read()
        result = json.loads(search_result) 

        # todo: continue here: extract tags

        print result

if __name__ == '__main__':
    Twitter.getRelatedTags(('debian', 'linux'))
