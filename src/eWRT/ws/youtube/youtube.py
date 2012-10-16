#!/usr/bin/env python
# coding: UTF-8
'''
Created on 25.09.2012

@author: Norman Süsstrunk, Heinz-Peter Lang
'''
import unittest
import logging
from operator import attrgetter
from datetime import datetime, timedelta

from gdata.youtube.service import YouTubeService, YouTubeVideoQuery

from eWRT.ws.WebDataSource import WebDataSource

MAX_RESULTS_PER_QUERY = 50 

logger = logging.getLogger('eWRT.ws.youtube')

# TODO: store the comments
# TODO: query.location --> radius available?

class YouTube(WebDataSource):
    '''
    searches youtube video library
    '''
    
    YT_ATOM_RESULT_TO_DICT_MAPPING = {
        'media.title.text': 'title',
        'published.text':'published',
        'media.description.text': 'content',
        'media.keywords.text':'keywords',
        'media.duration.seconds':'duration', 
        'rating.average': 'average rating', 
        'statistics.view_count': 'statistics_viewcount', 
        'statistics.favorite_count': 'statistics_favoritecount', 
        'rating.average': 'rating_average',
        'rating.max': 'rating_max',
        'rating.min': 'rating_min',
        'rating.num_raters': 'rating_numraters', 
        'summary': 'summary', 
        'rights': 'rights', 
        'updated.text': 'last_modified', 
        'source': 'yt_source'
    }
    
    def __init__(self):
        self.youtube_service = YouTubeService()
        
    def search(self, search_terms, location=None, 
               max_results=MAX_RESULTS_PER_QUERY, max_age=None):
        """ searches for youtube videos
        @param search_terms: list of search terms
        @param location: tuple latitude, longitue, e.g. 37.42307,-122.08427
        @param max_results:
        @param max_age: datetime of the oldest entry  
        """
        
        # all youtube search parameter are here: 
        # https://developers.google.com/youtube/2.0/reference?hl=de#Custom_parameters
        query = YouTubeVideoQuery()
        query.vq = ', '.join(search_terms)
        query.orderby = 'published'
        query.racy = 'include'
        query.time = self.get_query_time(max_age)
        if location:
            query.location = location
        if max_results > MAX_RESULTS_PER_QUERY:
            query.max_results = MAX_RESULTS_PER_QUERY
        else: 
            query.max_results = max_results
                        
        return self.search_youtube(query, max_results)
    
    @classmethod
    def get_query_time(cls, max_age):
        ''' converts a datetime or int (age in minutes) to the youtube specific
        query parameter (e.g. this_month, today ...)
        @param max_age: int or datetime object
        @return: youtube specific query_time 
        '''
        if not max_age:
            return 'all_time'
        
        if isinstance(max_age, datetime):
            # convert datetime to minutes
            max_age = (datetime.now() - max_age).total_seconds() / 60  

        if max_age <= 1440:
            query_time = 'today'
        elif max_age > 1440 and max_age <= 10080:
            query_time = 'this_week'
        else: 
            query_time = 'this_month'
            
        return query_time
    
    
    def search_youtube(self, query, max_results=MAX_RESULTS_PER_QUERY):
        ''' executes the youtube query and facilitates paging of the resultset
        @param query: YouTubeVideoQuery
        @param max_results: 
        @return: list of dictionaries 
        '''
        feed = self.youtube_service.YouTubeQuery(query)
        result = []
        
        for entry in feed.entry: 
            try: 
                yt_dict = self.convert_feed_entry(entry)
                result.append(yt_dict)
            except Exception, e: 
                logger.exception('Exception converting entry: %s' % e)
        
        # max_results = total_results
        if max_results > int(feed.total_results.text):
            max_results = int(feed.total_results.text)
        
        # set a new start_index, items_per_page to get the other entries
        if max_results > MAX_RESULTS_PER_QUERY:
            new_start_idx = int(feed.start_index.text) + int(feed.items_per_page.text)
            new_end_idx = new_start_idx + int(feed.items_per_page.text)
            
            if new_end_idx > max_results:
                new_end_idx = max_results + 1
            
            query.start_index = new_start_idx
            query.max_results = new_end_idx - new_start_idx

            if int(query.max_results) > 0:
                logger.debug('new query: start_index %s, max_results %s' % (query.start_index, 
                                                                            query.max_results))
                result.extend(self.search_youtube(query, max_results))
            
        return result

    def convert_feed_entry(self, entry):
        ''' converts the feed entry to a dictionary (never change the mapping
        names, as later analyzer steps requires consistent keys)
        @param entry: Youtube feed entry
        @return: dictionary   
        '''
        yt_dict = {'user_name': entry.author[0].name.text, 
                   'user_url': entry.author[0].uri.text}
        
        for attr, key in self.YT_ATOM_RESULT_TO_DICT_MAPPING.items(): 
            try: 
                yt_dict[key] = attrgetter(attr)(entry)
            except AttributeError, e:
                logger.warn('AttributeError: %s' % e)
                yt_dict[key] = None
                
        yt_dict['id'] = entry.id.text.split('/')[-1]
        yt_dict['url'] = "http://www.youtube.com/watch?v=%s" % yt_dict['id']         
        
        yt_dict['location'] = None
        if entry.geo: 
            yt_dict['location'] = entry.geo.location()
        
        yt_dict['related_url'] = None
        for link in entry.link:
            if link.href.endswith('related'):
                yt_dict['related_url'] = link.href
        
        if yt_dict['duration']: 
            duration = int(yt_dict['duration'])
            yt_dict['duration'] = '%d:%02d' % (duration / 60, duration % 60)
        
        yt_dict['picture'] = None
        for thumbnail in entry.media.thumbnail:
            yt_dict['picture'] = thumbnail.url
            break

        if not yt_dict['keywords']: 
            yt_dict['keywords'] = []

        for category in entry.category:
            if 'http://gdata.youtube.com/schemas' not in category.term:
                yt_dict['keywords'].append(category.term)

        return yt_dict
                                     

class YouTubeTest(unittest.TestCase):
        
    def setUp(self):
        self.search_terms = ["Linus Torvalds","Ubuntu"]
        self.youtube = YouTube()
    
    def test_query_time(self):
        test_cases = ((1000, 'today'), 
                      (5000, 'this_week'), 
                      (12000, 'this_month'), 
                      (datetime.now() - timedelta(hours=12), 'today'),
                      (datetime.now() - timedelta(days=4), 'this_week'),
                      (datetime.now() - timedelta(days=15), 'this_month'),)
        
        for max_age, exp_result in test_cases: 
            result = YouTube.get_query_time(max_age)
            assert exp_result == result, 'max_age %s, result %s, exp %s' % (max_age, 
                                                                            result, 
                                                                            exp_result)
        
    
    def test_search(self):   
        
        required_keys = ('location', 'content', 'id', 'url', 'title',
                         'last_modified', 'published', 'user_name', 
                         'yt_source', 'rights', 'summary', 'keywords', 
                         'related_url', 'statistics_viewcount', 
                         'statistics_favoritecount', 'rating_average', 
                         'rating_max', 'rating_min', 'rating_numraters', 
                         'picture', 'duration', 'user_url'
                        )
             
        for r in self.youtube.search(self.search_terms, None):

            assert len(required_keys) == len(r.keys())
            
            for rk in required_keys: 
                if not rk in r.keys():
                    print 'k ', sorted(r.keys())
                    print 'rk', sorted(required_keys)
                    assert False, 'key %s missing' % rk

    def test_max_result(self):
        
        search_terms = (('Linux', 43), ('Apple', 51), ('Microsoft', 99))
        
        for search_term, max_results in search_terms:
            print 'querying youtube for %s' % search_term
            result = self.youtube.search(search_term, None, max_results)
            print '\t got %s documents, max_results was %s' % (len(result),
                                                               max_results) 
            assert len(result) == max_results
            print '-------------------------'
        
if __name__ == "__main__":
    unittest.main()
        
