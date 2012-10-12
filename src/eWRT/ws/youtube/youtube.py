#!/usr/bin/env python
# coding: UTF-8
'''
Created on 25.09.2012

@author: Norman Süsstrunk
'''
import unittest

import gdata.youtube.service

#from eWRT.lib.apihelber import info
from eWRT.ws.WebDataSource import WebDataSource
from operator import attrgetter

class YouTube(WebDataSource):
    '''
    searches youtube video library
    '''
    
    YT_ATOM_RESULT_TO_DICT_MAPPING = {
                                       'media.title.text': 'title',
                                       'published.text':'published text',
                                       'media.description.text': 'description',
                                       'media.keywords.text':'keywords',
                                       'media.player.url':'player ulr',
                                       'media.duration.seconds':'duration', 
                                       'statistics.view_count': 'view count', 
                                       'rating.average': 'average rating'
    }
    
    def __init__(self):
        self.youtube_service = gdata.youtube.service.YouTubeService()
        
    def search(self, search_terms, location, max_results=50, time='all_time' ):
        """
        searches for youtube videos
        
        all youtube search parameter are here: 
        https://developers.google.com/youtube/2.0/reference?hl=de#Custom_parameters
        
        possible time values: 
            today (1 day), 
            this_week - default (7 days) 
            this_month (1 month)
            all_time (default in the yt api)
        
        Example for location value (latitude,longitude)
            location=37.42307,-122.08427
        
        """
        search_query_youtube = ", ".join(search_terms)
        query = gdata.youtube.service.YouTubeVideoQuery()
        query.vq = search_query_youtube
        query.orderby = 'viewCount'
        query.racy = 'include'
        query.time = time
        if location is not None:
            query.location = location
        query.max_results = max_results
        feed = self.youtube_service.YouTubeQuery(query)
        return self.convert_feed_to_result_dictionary(feed)
                
    @classmethod
    def convert_feed_to_result_dictionary(cls, feed):
        """ Converts youtube feed results to the eWRT dictionary
            format.
            @param feed: the youtube feed object
            @return: a list of dictionaries containing the query
                     results.
        """
        # result = [{key: attrgetter(attr)(entry) for attr, key in self.YT_ATOM_RESULT_TO_DICT_MAPPING.items()}  for entry in feed.entry ]
        result = []
        for entry in feed.entry: # iterate over all  
            youtube_result_dict = { key: attrgetter(attr)(entry) 
                  for attr, key in cls.YT_ATOM_RESULT_TO_DICT_MAPPING.items() }
                 
            youtube_result_dict['swf url'] = entry.GetSwfUrl()
            
            if entry.geo is not None: # can be none
                youtube_result_dict['geo location'] = entry.geo.location()
            
            # alternative media type
            youtube_result_dict['alternativ formats'] = [ 
                  'Alternate format: %s | url: %s '  
                  % (alternative_format.type, alternative_format.url) 
                  for alternative_format in entry.media.content 
                  if 'isDefault' not in alternative_format.extension_attributes ]
        
            # thumbnails
            youtube_result_dict['thumbnails'] = [ thumbnail.url for thumbnail in entry.media.thumbnail ]
                
            result.append(youtube_result_dict)
        return result
    
    def print_video_feed(self, feed):
        for entry in feed.entry:
            self.print_entry_details(entry)
    
    def print_entry_details(self, entry):
        print 'Video title: %s' % entry.media.title.text
        print 'Video published on: %s ' % entry.published.text
        print 'Video description: %s' % entry.media.description.text
        #'''print 'Video category: %s' % entry.media.category[[0]].text'''
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
    
    def test_search(self):
        print self.youtube.search(self.search_terms, None)
        # self.assertGreaterEqual(len(self.youtube.feed.entry), 0 )


if __name__ == "__main__":
    unittest.main()
        
