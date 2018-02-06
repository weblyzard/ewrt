#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 25.09.2012

@author: Norman Süsstrunk, Heinz-Peter Lang, Albert Weichselbraun
'''
from __future__ import print_function

import os
import unittest
import logging
import dateutil.parser as dateparser
import urllib
import json
import pytz

from six import string_types
from operator import attrgetter
from datetime import datetime, timedelta
from cPickle import dump
from time import sleep
from apiclient.discovery import build

from eWRT.ws.WebDataSource import WebDataSource


logger = logging.getLogger('eWRT.ws.youtube')

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'


def convert_date(str_date): return datetime.strptime(str_date, DATE_FORMAT)


def get_value(key, dictionary):
    if '.' in key and not key.isdigit():
        old_key, new_key = key.split('.', 1)
        if old_key in dictionary:
            return get_value(new_key, dictionary[old_key])
    else:
        if key in dictionary:
            return dictionary[key]

    return None


class YouTubeEntry(dict):

    DATE_FIELDS = ('published', 'last_modified')
    YOUTUBE_SEARCH_URL = 'https://www.youtube.com/watch?v='

    VIDEO_MAPPING = {
        'id': 'video_id',
        'comments': None,
        'channel': None,
        'snippet.title': 'title',
        'snippet.publishedAt': 'published',
        'snippet.description': 'content',
        'snippet.channelId': 'channel_id',
        'snippet.thumbnails.default.url': 'thumbnail',
        'contentDetails.duration': 'duration',
        'contentDetails.caption': 'caption',
        'contentDetails.licensedContent': 'licensed',
        'statistics.viewCount': 'statistics_viewcount',
        'statistics.favoriteCount': 'statistics_favoritecount',
        'statistics.likeCount': 'statistics_likecount',
        'statistics.dislikeCount': 'statistics_dislikecount',
        'statistics.commentCount': 'statistics_commentcount',
        'topicDetails.relevantTopicIds': 'freebase_topics_relevant',
        'topicDetails.topicIds': 'freebase_topics',
    }

    COMMENT_MAPPING = {
        'id': 'comment_id',
        'parent': 'parent_id',
        'snippet.authorDisplayName': 'user_name',
        'snippet.authorGoogleplusProfileUrl': 'user_profile',
        'snippet.viewer_rating': 'viewer_rating',
        'snippet.likeCount': 'like_count',
        'snippet.totalReplyCount': 'reply_count',
        'snippet.channelId': 'channel_id',
        'snippet.publishedAt': 'published',
        'snippet.updatedAt': 'last_modified',
        'snippet.textDisplay': 'content',
    }

    CHANNEL_MAPPING = {
        'id': 'channel_id',
        'kind': 'channel_type',
        'snippet.description': 'channel_description',
        'snippet.title': 'channel_name',
        'snippet.country': 'channel_country',
        'published_at': 'channel_published_at'
    }

    def __init__(self, search_result, mapping=VIDEO_MAPPING):
        ''' constructor initializes entry with the result'''
        dict.__init__(self)
        self.update(self.update_entry(search_result, mapping=mapping))

        if 'video_id' in self:
            self['url'] = ''.join([self.YOUTUBE_SEARCH_URL, self['video_id']])

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

            if attr == 'channel' and 'channel' in search_result:
                self['channel'] = search_result['channel']
                continue

            value = get_value(attr, search_result)
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            if key in self and isinstance(self[key], list):
                if value:
                    self[key].append(value)
            else:
                self[key] = value

        # parse dates
        if 'published' in self and not 'last_modified' in self:
            self['last_modified'] = self['published']

        for date_field in self.DATE_FIELDS:
            if date_field in self and isinstance(self[date_field], string_types):
                self[date_field] = dateparser.parse(self[date_field],
                                                    ignoretz=True)
        return self


class YouTube_v3(WebDataSource):

    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    ''' 
    number of seconds to wait between comment request
    this has been added to prevent the youtube API from
    blocking us via quota per seconds
    '''
    YOUTUBE_SLEEP_TIME = 1
    MAX_RESULTS_PER_QUERY = 50

    FREEBASE_SEARCH_URL = 'https://www.googleapis.com/freebase/v1/search?%s'

    def __init__(self, api_key, max_comment_count=10, get_details=True,
                 sleep_time=YOUTUBE_SLEEP_TIME):
        self.api_key = api_key
        self.max_comment_count = max_comment_count
        self.get_details = get_details
        self.client = build(self.YOUTUBE_API_SERVICE_NAME,
                            self.YOUTUBE_API_VERSION,
                            developerKey=self.api_key)
        self.sleep_time = sleep_time

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

            except AttributeError as e:
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
                except Exception as e:
                    logger.error(
                        'Failed to convert Youtube search result: %s' % e)

    def _get_video_rating(self, video_id):
        """ Returns the rating for a video ID """
        return self.client.videos().getRating(id=video_id).execute()

    def _get_video_status(self, video_id):
        return self.client.videos().list(id=video_id,
                                         part='id').execute()

    def _get_video_details(self, video_id):
        return self.client.videos().list(id=video_id,
                                         part='contentDetails,statistics,topicDetails').execute()

    def _get_video_channel_detail(self, channel_id):
        return self.client.channels().list(id=channel_id,
                                           part='contentOwnerDetails,snippet').execute()

    def like_video(self, video_id):
        """ Adds to the video rating. This code sets the rating to "like," but you 
            could also support an additional option that supports values of "like"
            and "dislike"."""
        self.client.videos().rate(id=video_id, rating="like").execute()

    def _build_youtube_item(self, item, max_comment_count=0, get_details=False):
        """ """

        video_id = item['id']['videoId']
        channel_id = item['snippet']['channelId']

        # retrieve comments and details as requested
        if max_comment_count > 0:
            item['comments'] = [YouTubeEntry(comment, YouTubeEntry.COMMENT_MAPPING)
                                for comment in self._get_video_comments(video_id=video_id)]

        if get_details:
            details = self._get_video_details(video_id=video_id)['items']
            if details and len(details) > 0:
                item.update(details[0])

            channel_info = self._get_video_channel_detail(
                channel_id=channel_id)['items']
            if channel_info and len(channel_info) > 0:
                item['channel'] = YouTubeEntry(
                    channel_info[0], YouTubeEntry.CHANNEL_MAPPING)

        return YouTubeEntry(item)

    def search(self,
               search_terms,
               max_results=MAX_RESULTS_PER_QUERY,
               since_date=None,
               region_code=None,
               language=None):
        """ 
        Search the Youtube API for videos matching a set of search terms 
        @param search_terms, a comma separated list of search terms
        @param max_results, the maximum number of results returned
        @param max_age, the maximum number of days ago from which to include results
        @param region_code, ISO 3166-1 alpha-2 country code, e.g. AT, DE, GB, US
        @param language, ISO 639-1 two-letter language code, e.g. de, cs, en
        """
        if not since_date:
            since_date = datetime.utcnow() - timedelta(days=1)
            since_date = since_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        if isinstance(since_date, datetime):
            local = pytz.timezone("Europe/Vienna")
            local_dt = local.localize(since_date, is_dst=None)
            utc_dt = local_dt.astimezone(pytz.utc)
            since_date = utc_dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        items_per_page = min([max_results, self.MAX_RESULTS_PER_QUERY])
#         search_terms = search_terms.encode('utf8')
#         search_terms = quote_plus(search_terms)
        kwargs = {'q': search_terms,
                  'part': 'id,snippet',
                  'type': 'video',
                  'publishedAfter': since_date,
                  'maxResults': items_per_page,
                  'order': 'date'}
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
                                                       max_comment_count=self.max_comment_count,
                                                       get_details=self.get_details)
                    except Exception as e:
                        logger.error('Failed to convert Youtube item: %s' % e)
                        yield None

            if items_count >= max_results:
                continue_search = False

            if items_count >= total_results:
                continue_search = False

            if items_count == 0:
                continue_search = False

            if not 'nextPageToken' in response:
                continue_search = False
            else:
                kwargs['pageToken'] = response['nextPageToken']

    def _get_video_comments(self, video_id):
        """ Returns the comments for a youtube ID"""
        result = []
        try:
            comments = self.client.commentThreads().list(part='snippet',
                                                         videoId=video_id,
                                                         textFormat='plainText'
                                                         ).execute()
        except Exception:
            return result  # just ignore, comments might be disabled

        if not comments or not 'items' in comments:
            return result  # just ignore, comments might be disabled

        for item in comments['items']:
            result.append(item['snippet']['topLevelComment'])

        return result

    def get_freebase_topics(self, QUERY_TERM):
        """ Retrieves a list of Freebase topics associated with the query term """
        freebase_params = dict(query=QUERY_TERM, key=self.api_key)
        freebase_url = self.FREEBASE_SEARCH_URL % urllib.urlencode(
            freebase_params)
        freebase_response = json.loads(urllib.urlopen(freebase_url).read())
        if len(freebase_response['result']) == 0:
            print('No matching terms were found in Freebase.')

        return freebase_response['result']

# class YouTube(WebDataSource):
#     '''
#     searches youtube video library
#     '''
#
#     YT_ATOM_RESULT_TO_DICT_MAPPING = {
#         'media.title.text': 'title',
#         'published.text':'published',
#         'media.description.text': 'content',
#         'media.duration.seconds':'duration',
#         'statistics.view_count': 'statistics_viewcount',
#         'statistics.favorite_count': 'statistics_favoritecount',
#         'rating.average': 'rating_average',
#         'rating.max': 'rating_max',
#         'rating.min': 'rating_min',
#         'rating.num_raters': 'rating_numraters',
#         'summary': 'summary',
#         'rights': 'rights',
#         'updated.text': 'last_modified',
#         'source': 'yt_source'
#     }
#
#     YT_COMMENTS_MAPPING = {
#         'id.text': 'id',
#         'title.text': 'title',
#         'published.text': 'published',
#         'updated.text': 'last_modified',
#         'content.text': 'content'
#     }
#
#     def __init__(self):
#         WebDataSource.__init__(self)
#         self.youtube_service = YouTubeService()
#
#
#     def search(self, search_terms, location=None,
#                max_results=MAX_RESULTS_PER_QUERY, max_age=None,
#                orderby= 'published', max_comment_count=0):
#         """
#         Searches for youtube videos.
#
#         @param search_terms: list of search terms
#         @param location: tuple latitude, longitue, e.g. 37.42307,-122.08427
#         @param max_results:
#         @param max_age: datetime of the oldest entry
#         @param orderby: order search results by (relevance, published,
#                         viewCount, rating)
#         @param max_comment_count: maximum number of comments to fetch
#                                   (default: 0)
#         """
#
#         if not (isinstance(search_terms, list) or
#             isinstance(search_terms, tuple) or isinstance(search_terms, set)):
#             raise ValueError("Warning search requires a list of search terms, \
#                              rather than a single term")
#
#         # all youtube search parameter are here:
#         # https://developers.google.com/youtube/2.0/reference?hl=de#Custom_parameters
#         query = YouTubeVideoQuery()
#         query.vq = ', '.join(search_terms)
#         query.orderby = orderby
#         query.racy = 'include'
#         query.time = self.get_query_time(max_age)
#         query.max_results = MAX_RESULTS_PER_QUERY
#
#         if location:
#             query.location = location
#
#         return self.search_youtube(query, max_results, max_comment_count)
#
#
#     @classmethod
#     def get_query_time(cls, max_age):
#         ''' converts a datetime or int (age in minutes) to the youtube specific
#         query parameter (e.g. this_month, today ...)
#         @param max_age: int or datetime object
#         @return: youtube specific query_time
#         '''
#         if not max_age:
#             return 'all_time'
#
#         if isinstance(max_age, datetime):
#             # convert datetime to minutes
#             max_age = (datetime.now() - max_age).total_seconds() / 60
#
#         if max_age <= 1440:
#             query_time = 'today'
#         elif max_age > 1440 and max_age <= 10080:
#             query_time = 'this_week'
#         else:
#             query_time = 'this_month'
#
#         return query_time
#
#     def search_youtube(self, query, max_results=MAX_RESULTS_PER_QUERY,
#                        max_comment_count=0):
#         ''' executes the youtube query and facilitates paging of the resultset
#         @param query: YouTubeVideoQuery
#         @param max_results:
#         @param max_comment_count: maximum number of comments to fetch
#         @return: list of dictionaries
#         '''
#         result = []
#         feed = self.youtube_service.YouTubeQuery(query)
#
#         while feed:
#             for entry in feed.entry:
#                 try:
#                     yt_dict = self.convert_feed_entry(entry, max_comment_count)
#                     result.append(yt_dict)
#                 except Exception as e:
#                     logger.exception('Exception converting entry: %s' % e)
#
#                 if len(result) == max_results:
#                     return result
#
#             if not feed.GetNextLink():
#                 break
#
#             feed = self.youtube_service.GetYouTubeVideoFeed(
#                                                     feed.GetNextLink().href)
#
#         return result
#
#
#     def convert_feed_entry(self, entry, max_comment_count):
#         ''' 1. converts the feed entry to a dictionary (never change the mapping
#                names, as later analyzer steps requires consistent keys)
#             2. fetches comments and integrate them in the dictionary, if
#                necessary
#
#             @param entry: Youtube feed entry
#             @param max_comment_count: maximum number of comments to fetch
#             @return: dictionary
#         '''
#
#         yt_dict = self._get_yt_dict(entry, self.YT_ATOM_RESULT_TO_DICT_MAPPING)
#         yt_dict.update({'user_name': entry.author[0].name.text,
#                         'user_url': entry.author[0].uri.text,
#                         'id': entry.id.text.split('/')[-1]})
#
#         yt_dict['url'] = "http://www.youtube.com/watch?v=%s" % yt_dict['id']
#
#         # the hasattr is required for compatibility with older videos
#         yt_dict['location'] = entry.geo.location() \
#             if hasattr(entry, 'geo') and entry.geo else None
#
#         yt_dict['related_url'] = None
#         for link in entry.link:
#             if link.href.endswith('related'):
#                 yt_dict['related_url'] = link.href
#
#         #mcg: yt APIv3 returns ISO8601, do not format
#         if yt_dict['duration']:
#             duration = yt_dict['duration']
#
#         yt_dict['picture'] = None
#
#         if hasattr(entry, 'media'):
#             for thumbnail in entry.media.thumbnail:
#                 yt_dict['picture'] = thumbnail.url
#                 break
#
#         yt_dict['keywords'] = [ category.label for category in entry.category \
#               if category.scheme != "http://schemas.google.com/g/2005#kind" ]
#
#         # retrieve comments, if required
#         if max_comment_count > 0:
#             yt_dict['comments'] = self.get_video_comments(yt_dict['id'],
#                                                           max_comment_count)
#
#         return yt_dict
#
#     @classmethod
#     def _get_yt_dict(cls, entry, mapping):
#         ''' stores the mapped items in a dictionary
#         @param entry: Gdata Entry
#         @param mapping: dictionary with the mapping
#         @return: yt_dict
#         '''
#         yt_dict = {}
#         for attr, key in mapping.iteritems():
#             try:
#                 yt_dict[key] = attrgetter(attr)(entry)
#
#                 if key in ('published', 'last_modified'):
#                     yt_dict[key] = convert_date(yt_dict[key])
#
#             except AttributeError, e:
#                 logger.warn('AttributeError: %s' % e)
#                 yt_dict[key] = None
#
#         return yt_dict
#
#     def get_video_comments(self, video_id, max_comments=25):
#         """ @param video_id: the video_id of the video for which we want to
#                              retrieve the comments.
#             @param max_comments: maximum number of comments to retrieve
#             @return: a list of comments
#         """
#         comments = []
#         comment_feed = self.youtube_service.GetYouTubeVideoCommentFeed(
#                             video_id=video_id)
#
#         while comment_feed:
#
#             sleep( YOUTUBE_SLEEP_TIME )
#             for comment in comment_feed.entry:
#                 url, in_reply_to = self.get_relevant_links(comment)
#                 yt_dict = self._get_yt_dict(comment, self.YT_COMMENTS_MAPPING)
#                 yt_dict.update({'url': url,
#                                 'in-reply-to': in_reply_to,
#                                 'author': comment.author[0].name.text,})
#                 comments.append(yt_dict)
#
#                 if len(comments) == max_comments:
#                     return comments
#
#             # retrieve the next comment page, if available
#             if not comment_feed.GetNextLink():
#                 break
#
#             comment_feed = self.youtube_service.Query(
#                                     comment_feed.GetNextLink().href)
#
#         return comments
#
#
#     @staticmethod
#     def get_relevant_links(comment):
#         """
#         @param comment: a single YouTube comment.
#         @return: a tuple indicating:
#                  a) the comment's url, and
#                  b) the url of the comment to which this comment refers (in case
#                     it is a reply)
#         """
#         comment_url, in_reply_to = None, None
#         for link in comment.link:
#             if link.rel == 'self':
#                 comment_url = link.href
#             elif link.rel.endswith("#in-reply-to"):
#                 in_reply_to = link.href
#
#         return comment_url, in_reply_to
