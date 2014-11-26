#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 23.10.2014

.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>

.. seealso:: 

    `Translate API - Getting Started <https://cloud.google.com/translate/v2/getting_started>`_

    `Google Developer Console <https://console.developers.google.com>`_
        Configure your application in the developer console
    
'''
import json
import requests
import logging
from urllib import urlencode

from eWRT.ws import AbstractWebSource

API_URL = 'https://www.googleapis.com/language/translate/v2'

class GoogleTranslator(AbstractWebSource):
    NAME = 'google_translate'
    SUPPORTED_PARAMS = ('text', 'target_language', 'source_language')
    logger = logging.getLogger('google_translator')
    
    def __init__(self, api_key, api_url=API_URL):
        self.api_key = api_key
        self.api_url = api_url
    
    def search_documents(self, search_terms, source_language, target_language):
        ''' translates the `search_terms` from `source_language to the 
        `target_language`
        :returns: iterator with the translated text
        '''
        if isinstance(search_terms, basestring):
            search_terms = [search_terms]
            
        for search_term in search_terms: 
            self.logger.info('... will translate "%s"' % search_term)
            result = self.translate(text=search_term, 
                                    target_language=target_language,
                                    source_language=source_language)

            translations = []
            
            if 'error' in result:
                self.logger.error(result['error']) 
                yield result
                continue
                
            for t in result['data']['translations']:
                lang_key = 'detectedSourceLanguage'
                source_lang = t[lang_key] if lang_key in t else source_language
                translations.append((t['translatedText'], 
                                     source_lang, 
                                     target_language))
                
            yield {'text': search_term, 
                   'translations': translations}             
         
    def _make_request(self, params, path=''):
        ''' makes the request to GoogleAPI ''' 
        if not 'key' in params: 
            params['key'] = self.api_key
        full_url = self.api_url + path + '?' + urlencode(params)
        resp = requests.get(full_url)
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
        