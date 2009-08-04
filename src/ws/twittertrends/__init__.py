from eWRTlibs.tango.tango import tango
import oauth

## @package TwitterTrends
class TwitterTrends(object):

    # init connects to Twitter
    def __init__(self):
        self.twitter = tango.setup();

    # getDailyTrends fetches the daily trends of twitter
    # @return trends
    def getDailyTrends(self):
        return self.twitter.getDailyTrends() 
