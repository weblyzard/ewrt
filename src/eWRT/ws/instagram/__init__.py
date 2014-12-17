#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 19.11.2014

.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>

Client for the Instgram API, see `Instagram Developer Documentation <http://instagram.com/developer/>`_
for details on how to obtain the `access_token` and usage of the API

.. todo:: use superclass Webservice and adapt this class. 

'''
import json
import requests
import logging
from datetime import datetime, timedelta

API_URL = 'https://api.instagram.com/v1/'
DEFAULT_MAX_AGE = 7 # days
DEFAULT_MAX_RESULTS = 1000

def convert_date(timestamp_str):
    ''' converts timestamp str to a datetime object'''
    if timestamp_str:
        return datetime.fromtimestamp(float(timestamp_str))

class InstagramClient(object):
 
    logger = logging.getLogger('eWRT.instagram')
 
    def __init__(self, access_token, api_url=API_URL, 
                 max_age=DEFAULT_MAX_AGE, 
                 max_results=DEFAULT_MAX_RESULTS):
        now = datetime.now()
        self.access_token = access_token
        self.api_url = api_url
        self.max_age = max_age if max_age else DEFAULT_MAX_AGE
        self.max_results = max_results if max_results else DEFAULT_MAX_RESULTS
        self.oldest_doc = now - timedelta(days=self.max_age)
     
    def _get_data(self, url, params=None):
        self.logger.debug('making request to %s' % url)
             
        response = requests.get(url, params=params)
             
        return json.loads(response.text)
     
    def _request(self, path, params=None):
        ''' executes the request and returns a generator of the found entries
        :param path: relative path of the instagram API endpoint
        :param params: additional parameters for the API request, see the API docu 
        :type params: dict or None
        :returns: generator with the entries as dictionaries
        '''
        url = '%s%s' % (self.api_url, path)
         
        params = params if params else {}
         
        if not 'access_token' in params: 
            params['access_token'] = self.access_token
        
        done = False
        total_docs = 0
        response_docs = 0
        max_docs = params.get('max_docs', self.max_results)
        
        if not 'count' in params: 
            params['count'] = 100 if max_docs >= 100 else max_docs
        
        while not done: 
            try: 
                data = self._get_data(url, params)
            except Exception, e: 
                self.logger.exception('Will stop: %s' % e)
                done = True
                continue
             
            response_docs = 0
     
            if data and 'data' in data: 
                for entry in data['data']:
                    add_entry = self.check_entry(entry)
                    
                    if add_entry:
                        total_docs += 1
                        response_docs += 1
                        yield entry
                         
                found_pagination = 'pagination' in data
                result_empty = response_docs == 0
                reached_limit = False if not max_docs else total_docs >= max_docs
                 
                if found_pagination and not result_empty and not reached_limit: 
                    if 'next_url' in data['pagination']:
                        url = data['pagination']['next_url']
                        params = None
                    else:
                        done = True
                else: 
                    done = True
            else: 
                self.logger.info('... done, data not in result')
                done = True
                 
            msg = 'done = %s, got %s / %s (request/total)' % (done, 
                                                              response_docs,
                                                              total_docs)
            
            self.logger.debug(msg)
             
    def search_tags(self, tag_name):
        return self._request('tags/search', {'q': tag_name})
     
    def get_recent_media(self, tag_name, params=None):
        return self._request(path='tags/%s/media/recent' % tag_name, 
                             params=params)
    
    def check_entry(self, entry):
        ''' checks if the entry is ok. TODO: implement this function  '''
        return True
        