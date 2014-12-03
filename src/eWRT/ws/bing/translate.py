#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 23.10.2014

.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>

.. seealso:: 

    `Getting started with Microsoft Translator <http://blogs.msdn.com/b/translation/p/gettingstarted1.aspx>`_

    `Translator Language Codes <http://msdn.microsoft.com/en-us/library/hh456380.aspx>`_

'''
import json
import requests
from datetime import datetime, timedelta

from urllib import urlencode
from eWRT.ws import AbstractWebSource

TOKEN_URL = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
API_URL = 'http://api.microsofttranslator.com/v2/Ajax.svc/Translate?'
REFRESH_TOKEN_INTERVAL = 10 # in minutes

class BingTranslator(AbstractWebSource):
    NAME = 'bing_translate'
    SUPPORTED_PARAMS = ('text', 'target_language', 'source_language')
    
    def __init__(self, client_id, client_secret, api_url=None, token_url=None):
        ''' sets the credentials for Bing Translator 
        .. todo:: store the urls in the database as welll !!! 
        
        '''
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_url = api_url if api_url else API_URL
        self.token_url = token_url if token_url else TOKEN_URL
        self._access_token = None
        self._next_refresh = None
         
    def search_documents(self, search_terms, source_language, target_language):
        ''' translates the `search_terms` from `source_language to the 
        `target_language`
        :returns: iterator with the translated text
        '''
        if isinstance(search_terms, basestring):
            search_terms = [search_terms]
            
        for search_term in search_terms: 
            translation = self.translate(text=search_term, 
                                         target_language=target_language,
                                         source_language=source_language)
            
            yield {'text': search_term, 
                   'translations': [(translation.strip(), 
                                     source_language,
                                     target_language)]}
            
    def translate(self, text, target_language, source_language):
        ''' tranlates the `text` in `source_language` to the `target_language`
        :param text: text to translate
        :type text: str or unicode
        :param target_language: language to translate to (iso-code)
        :param source_language: language of the given text (iso-code)
        :returns: translated text as string
        '''
        params = {'text': text, 
                  'from': source_language,
                  'to': target_language
                  }
        headers = {'Authorization': 'Bearer %s' % self.access_token}
        resp = requests.get(self.api_url+urlencode(params), headers=headers)
        return resp.text.replace('"', '').replace(u'\ufeff', '')
        
    def get_new_access_token(self):
        params = {'grant_type': 'client_credentials', 
                  'client_id': self.client_id,
                  'client_secret': self.client_secret,
                  'scope': 'http://api.microsofttranslator.com'}
            
        resp = requests.post(self.token_url, data=urlencode(params))
        return json.loads(resp.text)
    
    def get_access_token(self):
        now = datetime.now()

        too_old = False if not self._next_refresh else now > self._next_refresh
        
        if too_old or not self._access_token: 
            self._access_token = self.get_new_access_token()
            self._next_refresh = now + timedelta(minutes=REFRESH_TOKEN_INTERVAL)
            
        return self._access_token['access_token']
            
    access_token = property(get_access_token)
    