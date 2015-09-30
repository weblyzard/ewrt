#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 25.09.2012

@author: Norman Süsstrunk, Heinz-Peter Lang, Albert Weichselbraun
'''
import unittest
import logging
from operator import attrgetter
from datetime import datetime, timedelta
from cPickle import dump

from gdata.youtube.service import YouTubeService, YouTubeVideoQuery

from eWRT.ws.WebDataSource import WebDataSource
from time import sleep
import dateutil.parser as dateparser
from types import NoneType

from apiclient.discovery import build
import urllib, json

def get_value(key, dictionary):
    if '.' in key and not key.isdigit():
        old_key, new_key = key.split('.', 1)
        if old_key in dictionary:
            return get_value(new_key, dictionary[old_key])
    else: 
        if key in dictionary:
            return dictionary[key]
    
    return None

# number of seconds to wait between comment request
# this is required to prevent the youtube api from
# blocking us.
YOUTUBE_SLEEP_TIME = 1       
MAX_RESULTS_PER_QUERY = 50 
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'

logger = logging.getLogger('eWRT.ws.youtube')
convert_date = lambda str_date: datetime.strptime(str_date, DATE_FORMAT)

# ToDO: comment rating, once it get's supported by the gdata API.
# TODO: query.location --> radius available?

FREEBASE_SEARCH_URL = 'https://www.googleapis.com/freebase/v1/search?%s'
YOUTUBE_SEARCH_URL = 'https://www.youtube.com/watch?v='

class YouTubeEntry(dict):
    
    DATE_FIELDS = ('published', 'last_modified')
     
    VIDEO_MAPPING = {
        'id':'video_id',
        'comments': None,
        'snippet.title': 'title',
        'snippet.publishedAt':'published',
        'snippet.description': 'content',
        'contentDetails.duration':'duration',
        'contentDetails.caption':'caption',
        'contentDetails.licensedContent':'licensed',
        'statistics.viewCount':'statistics_viewcount',
        'statistics.favoriteCount':'statistics_favoritecount',
        'statistics.likeCount':'statistics_likecount',
        'statistics.dislikeCount':'statistics_dislikecount',
        'statistics.commentCount':'statistics_commentcount',
        'topicDetails.relevantTopicIds':'freebase_topics_relevant',
        'topicDetails.topicIds':'freebase_topics'     
    }
    
    COMMENT_MAPPING = {
        'id': 'comment_id',
        'parent':'parent_id',
        'snippet.authorDisplayName':'user_name',
        'snippet.authorGoogleplusProfileUrl':'user_profile',
        'snippet.viewer_rating':'viewer_rating',
        'snippet.likeCount':'like_count',
        'snippet.totalReplyCount':'reply_count',
        'snippet.channelId':'channel_id',
        'snippet.publishedAt':'published',
        'snippet.updatedAt':'last_modified',
        'snippet.textDisplay':'content',
    }
    
    def __init__(self, search_result, mapping=VIDEO_MAPPING):
        ''' constructor initializes entry with the result'''
        dict.__init__(self)
        self.update(self.update_entry(search_result, mapping=mapping))
    
        if 'video_id' in self:
            self['url'] = ''.join([YOUTUBE_SEARCH_URL, self['video_id']])
        
    def __repr__(self):
        return '** entry: %s' % '\n'.join(['%s: %s' % (k, v) for k, v in self.iteritems()])

    def update_entry(self, search_result, mapping=VIDEO_MAPPING):
        ''' stores the mapped items in a dictionary 
        @param search_result: the search result returned by youtube
        @param entry_type: string, either comment or video
        '''             
        for attr, key in mapping.iteritems(): 
            
            if attr == 'comments' and 'comments' in search_result:
                self['comments'] = search_result['comments']
                continue
            
            value = get_value(attr, search_result)
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            if key in self and isinstance(self[key], list):
                if value:
                    self[key].append(value)
            else: 
                self[key] = value
               
        #parse dates 
        if 'published' in self and not 'last_modified' in self:
            self['last_modified'] = self['published']

        for date_field in self.DATE_FIELDS:
            if isinstance(self[date_field], basestring):
                self[date_field] = dateparser.parse(self[date_field],
                                                    ignoretz=True)
        return self
    

class YouTube_v3(WebDataSource):
    
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    def __init__(self, api_key):
        self.api_key = api_key
        self.client = build(self.YOUTUBE_API_SERVICE_NAME, 
                            self.YOUTUBE_API_VERSION,
                            developerKey=self.api_key)

    @classmethod
    def _get_yt_dict(cls, entry, mapping):
        """ stores the mapped items in a dictionary 
        @param entry: Gdata Entry
        @param mapping: dictionary with the mapping
        @return: yt_dict
        """
        yt_dict = {}
        for attr, key in mapping.iteritems(): 
            try: 
                yt_dict[key] = attrgetter(attr)(entry)
                
                if key in ('published', 'last_modified'):
                    yt_dict[key] = convert_date(yt_dict[key])
                
            except AttributeError, e:
                logger.warn('AttributeError: %s' % e)
                yt_dict[key] = None        
        
        return yt_dict
    
    def get_video_search_feed(self, search_terms, max_results=25, max_comment_count=0):
        """
        Returns a generator of youtube search results
        """
        for search_result in self.search(search_terms, max_results):
            if search_result['id']['kind'] == 'youtube#video':
                try:
                    yield self._convert_item_to_video(search_result, 
                                                      max_comment_count)
                except Exception, e:
                    logger.error('Failed to convert Youtube search result: %s' % e)
                
    def _get_video_rating(self, video_id):
        """ Returns the rating for a video ID """
        return self.client.videos().getRating(id=video_id).execute()
        
    def _get_video_details(self, video_id):
        return self.client.videos().list(id=video_id, 
                                         part='contentDetails,statistics,topicDetails').execute()
    
    def like_video(self, video_id):
        """ Adds to the video rating. This code sets the rating to "like," but you 
            could also support an additional option that supports values of "like"
            and "dislike"."""
        self.client.videos().rate(id=video_id, rating="like").execute()

    def _build_youtube_item(self, item, max_comment_count=0, get_details=False):
        """ """
        
        video_id = item['id']['videoId']
        
        # retrieve comments and details as requested
        if max_comment_count > 0:
            item['comments'] = [YouTubeEntry(comment, YouTubeEntry.COMMENT_MAPPING) 
                                for comment in self._get_video_comments(video_id=video_id)]
 
        if get_details: 
            details = self._get_video_details(video_id=video_id)['items']
            if details and len(details)>0:
                item.update(details[0])

        return YouTubeEntry(item)
    
    def search(self, 
               search_terms, 
               max_results=MAX_RESULTS_PER_QUERY, 
               since_date=None, 
               region_code=None, 
               language=None):
        """ 
        Search the youtube API for videos matching a set of search terms 
        @param search_terms, a comma separated list of search terms
        @param max_results, the maximum number of results returned
        @param max_age, the maximum number of days ago from which to include results
        @param region_code, ISO 3166-1 alpha-2 country code, e.g. AT, DE, GB, US
        @param language, ISO 639-1 two-letter language code, e.g. de, cs, en
        """
        if not since_date:
            since_date = datetime.now() - timedelta(days=1)
        if isinstance(since_date, datetime):
            since_date = since_date.isoformat("T") + "Z"
            
        items_per_page = min([max_results, MAX_RESULTS_PER_QUERY])
            
        kwargs = {'q':search_terms,
                  'part':'id,snippet',
                  'type':'video',
                  'publishedAfter':since_date,
                  'maxResults':items_per_page,
                  'order':'date'}
        
        if region_code:
            kwargs['regionCode'] = region_code
        if language:
            kwargs['relevanceLanguage'] = language
                                         
        continue_search = True
        items_count = 0 
        
        while continue_search: 
        
            response = self.client.search().list(**kwargs).execute()
            total_results = response['pageInfo']['totalResults']
            
            for search_result in response.get('items', []):
                if search_result['id']['kind'] == 'youtube#video':
                    try:
                        items_count += 1
                        yield self._build_youtube_item(search_result,
                                                       max_comment_count=10, 
                                                       get_details=True)
                    except Exception,e:
                        logger.error('Failed to convert Youtube item: %s' %e) 
            
            if items_count >= max_results:
                continue_search = False
            
            if items_count >= total_results:
                continue_search = False 
                
            if not 'nextPageToken' in response:
                continue_search = False
            else:
                kwargs['pageToken'] = response['nextPageToken']
                 
    def _get_video_comments(self, video_id):
        """ Returns the comments for a youtube ID"""
        comments = self.client.commentThreads().list(part='snippet',
                                                     videoId=video_id,
                                                     textFormat='plainText'
                                                     ).execute()
        result = []
        for item in comments['items']:
            result.append(item['snippet']['topLevelComment'])

        return result
    
    def get_freebase_topics(self, QUERY_TERM):
        """ Retrieves a list of Freebase topics associated with the query term """
        freebase_params = dict(query=QUERY_TERM, key=self.api_key)
        freebase_url = FREEBASE_SEARCH_URL % urllib.urlencode(freebase_params)
        freebase_response = json.loads(urllib.urlopen(freebase_url).read())
        if len(freebase_response['result']) == 0:
            print('No matching terms were found in Freebase.')
            
        return freebase_response['result']

class YouTube(WebDataSource):
    '''
    searches youtube video library
    '''
    
    YT_ATOM_RESULT_TO_DICT_MAPPING = {
        'media.title.text': 'title',
        'published.text':'published',
        'media.description.text': 'content',
        'media.duration.seconds':'duration', 
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
    
    YT_COMMENTS_MAPPING = {
        'id.text': 'id', 
        'title.text': 'title',
        'published.text': 'published',
        'updated.text': 'last_modified',
        'content.text': 'content'
    }
    
    def __init__(self):
        WebDataSource.__init__(self)
        self.youtube_service = YouTubeService()

        
    def search(self, search_terms, location=None, 
               max_results=MAX_RESULTS_PER_QUERY, max_age=None,
               orderby= 'published',
               max_comment_count=0):
        """ 
        Searches for youtube videos.
        
        @param search_terms: list of search terms
        @param location: tuple latitude, longitue, e.g. 37.42307,-122.08427
        @param max_results:
        @param max_age: datetime of the oldest entry  
        @param orderby: order search results by (relevance, published, 
                        viewCount, rating)
        @param max_comment_count: maximum number of comments to fetch 
                                  (default: 0)
        """
        
        if not (isinstance(search_terms, list) or 
            isinstance(search_terms, tuple) or isinstance(search_terms, set)):
            raise ValueError("Warning search requires a list of search terms, \
                             rather than a single term")

        # all youtube search parameter are here: 
        # https://developers.google.com/youtube/2.0/reference?hl=de#Custom_parameters
        query = YouTubeVideoQuery()
        query.vq = ', '.join(search_terms)
        query.orderby = orderby
        query.racy = 'include'
        query.time = self.get_query_time(max_age)
        query.max_results = MAX_RESULTS_PER_QUERY

        if location:
            query.location = location
                        
        return self.search_youtube(query, max_results, max_comment_count)
    

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
  
    def search_youtube(self, query, max_results=MAX_RESULTS_PER_QUERY, 
                       max_comment_count=0):
        ''' executes the youtube query and facilitates paging of the resultset
        @param query: YouTubeVideoQuery
        @param max_results: 
        @param max_comment_count: maximum number of comments to fetch
        @return: list of dictionaries 
        '''
        result = []
        feed = self.youtube_service.YouTubeQuery(query)
        
        while feed:
            for entry in feed.entry: 
                try: 
                    yt_dict = self.convert_feed_entry(entry, max_comment_count)
                    result.append(yt_dict)
                except Exception, e: 
                    logger.exception('Exception converting entry: %s' % e)
                    
                if len(result) == max_results:
                    return result
                
            if not feed.GetNextLink():
                break
            
            feed = self.youtube_service.GetYouTubeVideoFeed(
                                                    feed.GetNextLink().href)
            
        return result


    def convert_feed_entry(self, entry, max_comment_count):
        ''' 1. converts the feed entry to a dictionary (never change the mapping
               names, as later analyzer steps requires consistent keys)
            2. fetches comments and integrate them in the dictionary, if 
               necessary
            
            @param entry: Youtube feed entry
            @param max_comment_count: maximum number of comments to fetch
            @return: dictionary   
        '''

        yt_dict = self._get_yt_dict(entry, self.YT_ATOM_RESULT_TO_DICT_MAPPING)
        yt_dict.update({'user_name': entry.author[0].name.text, 
                        'user_url': entry.author[0].uri.text,
                        'id': entry.id.text.split('/')[-1]})
                       
        yt_dict['url'] = "http://www.youtube.com/watch?v=%s" % yt_dict['id']         
        
        # the hasattr is required for compatibility with older videos
        yt_dict['location'] = entry.geo.location() \
            if hasattr(entry, 'geo') and entry.geo else None
        
        yt_dict['related_url'] = None
        for link in entry.link:
            if link.href.endswith('related'):
                yt_dict['related_url'] = link.href
        
        #mcg: yt APIv3 returns ISO8601, do not format
        if yt_dict['duration']: 
            duration = yt_dict['duration']
        
        yt_dict['picture'] = None

        if hasattr(entry, 'media'):
            for thumbnail in entry.media.thumbnail:
                yt_dict['picture'] = thumbnail.url
                break

        yt_dict['keywords'] = [ category.label for category in entry.category \
              if category.scheme != "http://schemas.google.com/g/2005#kind" ]

        # retrieve comments, if required
        if max_comment_count > 0:
            yt_dict['comments'] = self.get_video_comments(yt_dict['id'],
                                                          max_comment_count)

        return yt_dict

    @classmethod
    def _get_yt_dict(cls, entry, mapping):
        ''' stores the mapped items in a dictionary 
        @param entry: Gdata Entry
        @param mapping: dictionary with the mapping
        @return: yt_dict
        '''
        yt_dict = {}
        for attr, key in mapping.iteritems(): 
            try: 
                yt_dict[key] = attrgetter(attr)(entry)
                
                if key in ('published', 'last_modified'):
                    yt_dict[key] = convert_date(yt_dict[key])
                
            except AttributeError, e:
                logger.warn('AttributeError: %s' % e)
                yt_dict[key] = None        
        
        return yt_dict

    def get_video_comments(self, video_id, max_comments=25):
        """ @param video_id: the video_id of the video for which we want to
                             retrieve the comments.
            @param max_comments: maximum number of comments to retrieve
            @return: a list of comments 
        """
        comments = []
        comment_feed = self.youtube_service.GetYouTubeVideoCommentFeed(
                            video_id=video_id)
        
        while comment_feed:
            
            sleep( YOUTUBE_SLEEP_TIME )
            for comment in comment_feed.entry:
                url, in_reply_to = self.get_relevant_links(comment)
                yt_dict = self._get_yt_dict(comment, self.YT_COMMENTS_MAPPING)
                yt_dict.update({'url': url,
                                'in-reply-to': in_reply_to,
                                'author': comment.author[0].name.text,})
                comments.append(yt_dict)

                if len(comments) == max_comments:
                    return comments
                
            # retrieve the next comment page, if available
            if not comment_feed.GetNextLink():
                break
           
            comment_feed = self.youtube_service.Query(
                                    comment_feed.GetNextLink().href)
        
        return comments


    @staticmethod
    def get_relevant_links(comment):
        """ 
        @param comment: a single YouTube comment.
        @return: a tuple indicating:
                 a) the comment's url, and 
                 b) the url of the comment to which this comment refers (in case
                    it is a reply)
        """
        comment_url, in_reply_to = None, None
        for link in comment.link:
            if link.rel == 'self':
                comment_url = link.href
            elif link.rel.endswith("#in-reply-to"):
                in_reply_to = link.href

        return comment_url, in_reply_to        

                                    
class YouTubeTest(unittest.TestCase):
        
#     def setUp(self):
#         self.search_terms = ["Linus Torvalds","Ubuntu"]
#         self.youtube = YouTube()
#         logger.addHandler(logging.StreamHandler())
    
    
    def test_search_v3(self):
        search_term = 'FIFA'
        api_key = 'AIzaSyAfFOJnJMd3QfP0cV9HDymin19gkYDDR5c'
        
        service = YouTube_v3(api_key)
        result = service.search(search_terms=search_term)
        for item in result:
            print item
        print result
        
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
#     def test_search(self):   
#         required_keys = ('location', 'content', 'id', 'url', 'title',
#                          'last_modified', 'published', 'user_name', 
#                          'yt_source', 'rights', 'summary', 'keywords', 
#                          'related_url', 'statistics_viewcount', 
#                          'statistics_favoritecount', 'rating_average', 
#                          'rating_max', 'rating_min', 'rating_numraters', 
#                          'picture', 'duration', 'user_url'
#                         )
#              
#         for r in self.youtube.search(self.search_terms, None, orderby='relevance'):
# 
#             assert len(required_keys) == len(r.keys())
#             assert isinstance(r['last_modified'], datetime)
#             for rk in required_keys: 
#                 if not rk in r.keys():
#                     print 'k ', sorted(r.keys())
#                     print 'rk', sorted(required_keys)
#                     assert False, 'key %s missing' % rk
#     
#     def test_convert_date(self):
#         date_str = '2012-11-24T02:48:24.000Z'
#         assert convert_date(date_str) == datetime(2012, 11, 24, 2, 48, 24)
# 
#     def test_comments_result(self):
#         search_terms = ((('Linux',), 5), (('Climate Change',), 3), 
#                         (('Microsoft',), 2))
#         
#         for search_term, max_results in search_terms:
#             print 'querying youtube for %s' % search_term
#             result = self.youtube.search(search_term, None, max_results, 
#                                          orderby='relevance', 
#                                          max_comment_count=5)
#             print '\t got %s documents, max_results was %s' % (len(result),
#                                                                max_results) 
#             self.assertEqual( len(result), max_results)
#             
#             num_comments = max([ len(r['comments']) for r in result ])
#             print "Maximum number of comments for search term '%s': %d" % (search_term[0], num_comments)
#             self.assertEqual( 5, num_comments )
#             print '-------------------------'
#             
# 
#     def test_paging(self):
#         """
#         verifies that the results contain the necessary fields.
#         <ul>
#           <li>ratings: if not disabled by the publisher, _most_ videos
#                        should contain ratings </li>
#         </ul>
#         """
#         MAX_RESULTS = 70
#         result = self.youtube.search( ("Linux", ), None, 
#                                 max_results=MAX_RESULTS, orderby='relevance')
# 
#         # verify that all videos have been retrieved
#         assert len(result) == MAX_RESULTS
# 
#         # verify that the video rating and keywords have been correctly retrieved
#         # and interpreted
#         ratings_retrieved = 0
#         for _, r in enumerate(result):
#             if r['rating_average']:
#                 ratings_retrieved += 1
#             if r['keywords']:
#                 assert isinstance(r['keywords'][0], str)
#                 
#         self.assertGreater(ratings_retrieved, MAX_RESULTS*0.9, 
#                    "Assert that at least 90% of all videos contain ratings")
# 
# 
#     def test_search_term_list(self):
#         self.assertRaises( ValueError, self.youtube.search, "Linux" )
#        
# 
#     def test_comments(self):
#         comments = self.youtube.get_video_comments(video_id="yI4g8Ti6eTM", 
#                                                    max_comments = 27)
#         assert len(comments) == 27



        

if __name__ == "__main__":
    unittest.main()
