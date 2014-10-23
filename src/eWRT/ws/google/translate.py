#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 23.10.2014

.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>
'''
import json
import requests
from urllib import urlencode

from eWRT.ws import AbstractWebSource

API_URL = 'https://www.googleapis.com/language/translate/v2'

class GoogleTranslate(AbstractWebSource):
    NAME = 'google_translate'
    SUPPORTED_PARAMS = ('text', 'target_language', 'source_language')
    
    def __init__(self, api_key, api_url=API_URL):
        self.api_key = api_key
        self.api_url = api_url
        
    def _make_request(self, params, path=''):
        ''' makes the request to GoogleAPI ''' 
        if not 'key' in params: 
            params['key'] = self.api_key
            
        resp = requests.get(self.api_url + path + '?' + urlencode(params))
        
        return json.loads(resp.text)
    
    def translate(self, text, target_language, source_language=None):
        ''' translates the text '''
        params = {'target': target_language, 'q': text}
        
        if source_language: 
            params['source'] = source_language
       
        return self._make_request(params)
    
    def detect_language(self, text):
        ''' detects the language of the given `text` '''
        return self._make_request({'q': text}, path='/detect')
        