#!/usr/bin/env python
# coding: UTF-8
'''
Created on 25.09.2012

@author: Norman Süsstrunk
'''
import unittest

import gdata.youtube.service

from eWRT.lib.apihelber import info
from eWRT.ws.WebDataSource import WebDataSource

class YouTube(WebDataSource):
    '''
    searches youtube video library
    '''
    def __init__(self):
        self.youtube_service = gdata.youtube.service.YouTubeService()
        self.feed = None
        
    def search(self, search_terms, max_doc=100, max_age='this week', location='None'):
        """search"""
        search_query_youtube = self.concat_list_to_yt_term_sq(search_terms)
        query = gdata.youtube.service.YouTubeVideoQuery()
        query.vq = search_query_youtube
        query.orderby = 'viewCount'
        query.racy = 'include'
        self.feed = self.youtube_service.YouTubeQuery(query)
        #sprint info(self.feed.entry)
    
    def concat_list_to_yt_term_sq(self, term_list):
        return ", ".join(term_list)
    
    def print_video_feed(self):
        for entry in self.feed.entry:
            self.print_entry_details(entry)
    
    def print_entry_details(self, entry):
        print 'Video title: %s' % entry.media.title.text
        print 'Video published on: %s ' % entry.published.text
        print 'Video description: %s' % entry.media.description.text
        '''print 'Video category: %s' % entry.media.category[[0]].text'''
        print 'Video tags: %s' % entry.media.keywords.text
        print 'Video watch page: %s' % entry.media.player.url
        print 'Video flash player URL: %s' % entry.GetSwfUrl()
        print 'Video duration: %s' % entry.media.duration.seconds
        
        # non entry.media attributes
        # print 'Video geo location: %s' % entry.geo.location()
        # print 'Video view count: %s' % entry.statistics.view_count
        # print 'Video rating: %s' % entry.rating.average
        
        # show alternate formats
        for alternate_format in entry.media.content:
            if 'isDefault' not in alternate_format.extension_attributes:
                print 'Alternate format: %s | url: %s ' % (alternate_format.type, alternate_format.url)
        
        # show thumbnails
        for thumbnail in entry.media.thumbnail:
            print 'Thumbnail url: %s' % thumbnail.url                                     

class YouTubeTest(unittest.TestCase):
        
    def setUp(self):
        self.search_terms = ["Linus Torvalds","Ubuntu"]
        self.youtube = YouTube()
    
    def test_concat_list_to_yt_term_sq(self):
        search_term_query = self.youtube.concat_list_to_yt_term_sq(self.search_terms)
        self.assertEqual("Linus Torvalds, Ubuntu", search_term_query)
         
    def test_search(self):
        self.youtube.search(self.search_terms, None, None, None)
        self.assertGreaterEqual(len(self.youtube.feed.entry), 0 )

if __name__ == "__main__":
    unittest.main()
        
