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
        'snippet.description': 'description',
        'snippet.channelId': 'user_id',
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
        'id': 'user_id',
        'kind': 'user_type',
        'snippet.description': 'user_status',
        'snippet.title': 'user_name',
        'snippet.country': 'user_location',
        'published_at': 'location'
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

    def get_channelId_for_user(self, user_name):
        ''' 

        https://www.googleapis.com/youtube/v3/channels?key={YOUR_API_KEY}&forUsername={USER_NAME}&part=id
        '''
        result = self.client.channels().list(part='id,snippet',
                                             forUsername=user_name)
        return result

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

    def username_to_channels(self, username):
        """
        Retreive the channel_id of a youtube user
        @param username, username of youtube account
        """
        response = self.client.channels().list(
            forUsername=username, part='id').execute()
        for item in response['items']:
            yield item['id']

    def search(self, search_terms, since_date=None, region_code=None, language=None,
               max_results=MAX_RESULTS_PER_QUERY, is_channel=False):
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
        kwargs = {
            'part': 'id,snippet',
            'type': 'video',
            'publishedAfter': since_date,
            'maxResults': items_per_page,
            'order': 'date'}
        if is_channel:
            kwargs['channelId'] = search_terms
        else:
            kwargs['q'] = search_terms

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
