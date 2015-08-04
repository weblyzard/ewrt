#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Dec 13, 2011

:author: heinz
'''
import json
import logging
from urllib import urlencode
from datetime import datetime

from eWRT.access.http import Retrieve
from eWRT.ws.WebDataSource import WebDataSource

API_URL = 'https://www.googleapis.com/plus/v1/{path}?{query}'
DEFAULT_ORDER_BY = 'recent' # other possibility: best
DEFAULT_MAX_RESULTS = 20 # requires only 1 api access

logger = logging.getLogger('eWRT.ws.google')

class GooglePlus(object):
    '''
    classdocs
    '''

    def __init__(self, api_key, api_url=API_URL):
        ''' Constructor      '''
        WebDataSource.__init__(self)
        self.api_key = api_key
        self.api_url = api_url
        self.retrieve = Retrieve('google-plus')
        
    def search(self, search_terms, max_results=DEFAULT_MAX_RESULTS):
        ''' searches Google+ for the given search_terms 
        :param search_terms: search terms
        :type search_terms: list
        :param max_results: maximum number of result
        :type max_results: int
        :returns: generator with the result
        '''
        for search_term in search_terms: 
            if isinstance(search_term, unicode):
                search_term = search_term.encode('utf-8')
            params = {'query': '"%s"' % search_term,
                      'orderBy': DEFAULT_ORDER_BY,
                      'maxResults': max_results}
        
            fetched = self.make_request(params, 'activities')
            
            for item in fetched['items']:
                try: 
                    yield self.convert_item(item)
                except Exception, e: 
                    logger.info('Error %s occured' % e)
                    continue
        
    def get_activity(self, activity_id):
        ''' returns the activity with the given ID
        :param activity_id: GooglePlus activity ID
        :type activity_id: basestring
        :returns: mapped result
        :rtype: dict
        '''
        item = self.make_request(path='activities/%s' % activity_id)
        return self.convert_item(item)
    
    def make_request(self, params=None, path='activities'):
        ''' executes the request to GooglePlus
        :param params: paremeters for the query
        :type params: list or None
        :param path: path to query, e.g. activities
        :type path: basestring
        :returns: GooglePlus result
        :rtype: dict
        '''
        url = self.get_request_url(params, path)
        data = self.retrieve.open(url)
        return json.load(data)

    
    def get_request_url(self, params=None, path='activities'):
        ''' returns a correctly parsed request URL 
        :param params: paremeters for the query
        :type params: list or None
        :param path: path to query, e.g. activities
        :type path: basestring
        :returns: GooglePlus request URL
        :rtype: str
        
        Usage: 
            >>> plus = GooglePlus('abcd')
            >>> plus.get_request_url()
            'https://www.googleapis.com/plus/v1/activities?key=abcd'
        '''
        params = params if params else {}
        
        if not 'key' in params:
            params['key'] = self.api_key
        
        if 'maxResults' in params and params['maxResults'] > DEFAULT_MAX_RESULTS:
            params['maxResults'] = DEFAULT_MAX_RESULTS
        
        return self.api_url.format(path=path, query=urlencode(params))

    @classmethod
    def convert_item(cls, item):
        ''' applies a mapping to convert the result to the required format
        :param item: GooglePlus Activity
        :type item: dict
        :rtype: dict
        '''

        last_modified = datetime.strptime(item['updated'], 
                                          '%Y-%m-%dT%H:%M:%S.%fZ')
        published = datetime.strptime(item['updated'], 
                                          '%Y-%m-%dT%H:%M:%S.%fZ')

        content = cls.convert_content(item['object']['content'])

        if not item['verb'] == 'post':
            raise Exception('Skipping activity of type "%s"' % item['verb']) 

        if not len(content):
            logger.info('Skipping "%s" -> content is empty' % item['title'])
            raise Exception('content is empty')
    
        if 'attachments' in item['object']:
            for attachment in item['object']['attachments']:
                if attachment['objectType'] == 'article':
                    if not 'content' in attachment:
                        raise Exception('no content in attachment')
                    
                    content = '%s\n"%s" (%s)' % (content, 
                                                 cls.convert_content(attachment['content']),
                                                 attachment['url'])   
    
        activity = {'content': content,
                    'title': item['actor']['displayName'],
                    'url':item['url'],
                    'last_modified': last_modified,
                    'user_id': item['actor']['id'],
                    'user_img_url': item['actor']['image']['url'],
                    'screen_name': item['actor']['displayName'],
                    'encoding': u'utf-8',
                    'user_url': item['actor']['url'],
                    'valid_from': published,
                    'reshares': item['object']['resharers']['totalItems'],
                    'plusoners': item['object']['plusoners']['totalItems'],
                    'activity_id': item['id'],
                    }

        if 'geocode' in activity:
            activity['geocode'] = item['geocode']

        return activity


if __name__ == '__main__':
    import doctest
    doctest.testmod()