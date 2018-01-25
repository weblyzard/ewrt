#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Nov 29, 2017

.. codeauthor: max goebel <mcgoebel@gmail.com>
'''
import unittest
import logging
import os

from datetime import datetime, timedelta

from eWRT.ws.youtube import convert_date, YouTube_v3
from eWRT.config import YOUTUBE_API_KEY

                    
logger = logging.getLogger('eWRT.ws.youtube')
                                  
class YouTubeTest(unittest.TestCase):
        
    def setUp(self):
        api_key = os.getenv('YOUTUBE_API_KEY') or YOUTUBE_API_KEY
        if not api_key or len(api_key)==0:
            raise unittest.SkipTest('Skipping YouTubeTest: missing API key')
        self.search_terms = ["Linus Torvalds","Ubuntu"]
        self.youtube = YouTube_v3(api_key=api_key)
        logger.addHandler(logging.StreamHandler())

    def test_search_v3(self):
        search_terms = 'FIFA'
        since_date = None
        max_results = 10
         
        if not since_date:
            since_date = datetime.now() - timedelta(days=1)
        if isinstance(since_date, datetime):
            since_date = since_date.isoformat("T") + "Z"
             
        items_per_page = min([max_results, self.youtube.MAX_RESULTS_PER_QUERY])
             
        for r in self.youtube.search(search_terms=search_terms, 
#                                     location=location,
                                     max_results=max_results,
                                     since_date=since_date):
            print('=================================================')
            print(r)
            
        kwargs = {'q':search_terms,
                  'part':'id,snippet',
                  'type':'video',
                  'publishedAfter':since_date,
                  'maxResults':items_per_page,
                  'order':'date'}
         
#         if region_code:
#             kwargs['regionCode'] = region_code
#         if language:
#             kwargs['relevanceLanguage'] = language
             
        response = self.youtube.search().list(**kwargs).execute()
        total_results = response['pageInfo']['totalResults']
             
        result = []
        items_count = 0
        for search_result in response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                try:
                    items_count += 1
                    result.append( self._build_youtube_item(search_result,
                                                   max_comment_count=10, 
                                                   get_details=True))
                except Exception as e:
                    print(e)
                                   
        assert len(result)
        
#     def test_query_time(self):
#         test_cases = ((1000, 'today'), 
#                       (5000, 'this_week'), 
#                       (12000, 'this_month'), 
#                       (datetime.now() - timedelta(hours=12), 'today'),
#                       (datetime.now() - timedelta(days=4), 'this_week'),
#                       (datetime.now() - timedelta(days=15), 'this_month'),)
#          
#         for max_age, exp_result in test_cases: 
#             result = YouTube.get_query_time(max_age)
#             assert exp_result == result, 'max_age %s, result %s, exp %s' % (max_age, 
#                                                                             result, 
#                                                                             exp_result)
    def test_search(self):   
        required_keys = ('location', 'content', 'id', 'url', 'title',
                         'last_modified', 'published', 'user_name', 
                         'yt_source', 'rights', 'summary', 'keywords', 
                         'related_url', 'statistics_viewcount', 
                         'statistics_favoritecount', 'rating_average', 
                         'rating_max', 'rating_min', 'rating_numraters', 
                         'picture', 'duration', ''
                        )
              
        for r in self.youtube.search(self.search_terms, None):
 
            assert len(required_keys) == len(r.keys())
            assert isinstance(r['last_modified'], datetime)
            for rk in required_keys: 
                if not rk in r.keys():
                    print('k ', sorted(r.keys()))
                    print('rk', sorted(required_keys))
                    assert False, 'key %s missing' % rk
     
    def test_convert_date(self):
        date_str = '2012-11-24T02:48:24.000Z'
        assert convert_date(date_str) == datetime(2012, 11, 24, 2, 48, 24)
 
    def test_comments_result(self):
        search_terms = ((('Linux',), 5), (('Climate Change',), 3), 
                        (('Microsoft',), 2))
         
        for search_term, max_results in search_terms:
            print('querying youtube for %s' % search_term)
            result = [item for item in self.youtube.search(search_term, max_results)]
            print('\t got %s documents, max_results was %s' % (len(result),
                                                               max_results)) 
            self.assertEqual( len(result), max_results)
             
            num_comments = max([ len(r['comments']) for r in result ])
            print("Maximum number of comments for search term '%s': %d" % (search_term[0], num_comments))
            print('-------------------------')
 
    def test_comments(self):
        comments = self.youtube._get_video_comments(video_id="yI4g8Ti6eTM")
        assert len(comments)

if __name__ == "__main__":
    unittest.main()
