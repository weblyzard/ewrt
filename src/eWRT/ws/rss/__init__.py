#!/usr/bin/env python

"""
@package eWRT.ws.rss
@author: Albert Weichselbraun <albert@weblyzard.com>

Retrieves RSS Feeds and the corresponding Web page.
"""

from datetime import datetime
from time import mktime
import feedparser
from eWRT.access.http import Retrieve
from unittest import main

HTTP_FETCH_DELAY = 0

def parse(url, last_modified=None):
    """ 
    Parses the given RSS Feed an returns all articles and the content of
    the page referenced in the <link> tag.
    
    @param url: the url of the rss feed
    @param last_modified: a datetime object that specifies the last time the
                          feed has been queried the last time (only newer 
                          entries are returned).  
    """
    feed = feedparser.parse(url, modified=last_modified)
    retrieve = Retrieve("rss", HTTP_FETCH_DELAY)
    
    result = []
    for item in feed['items']:
        if datetime.fromtimestamp(
                mktime(item['updated_parsed'])) > last_modified:
            item['content'] = retrieve.open(item['link']).read()
            result.append(item)

    return result



def parse_test():
    """ Test the rss module. """
    TEST_URL = "http://kurier.at/rss/channel_startseite_rss.xml"
    last_modified = datetime(2012,8,3,21,50,00)
    for a in parse(TEST_URL, last_modified):
        print a['link'], a['date']
        print len(a['content'])