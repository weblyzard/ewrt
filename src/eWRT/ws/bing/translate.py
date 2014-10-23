#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 23.10.2014

.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>

.. seealso:: 

    `Getting started with Microsoft Translator <http://blogs.msdn.com/b/translation/p/gettingstarted1.aspx>`


string clientID = "<Your ClientID>";
string clientSecret = "<Your Client Secret>";
String strTranslatorAccessURI = "https://datamarket.accesscontrol.windows.net/v2/OAuth2-13";

String strRequestDetails = string.Format("grant_type=client_credentials&client_id={0}&client_secret={1}&scope=http://api.microsofttranslator.com", HttpUtility.UrlEncode(clientID), HttpUtility.UrlEncode(clientSecret));


System.Net.WebRequest webRequest = System.Net.WebRequest.Create(strTranslatorAccessURI);
webRequest.ContentType = "application/x-www-form-urlencoded";
webRequest.Method = "POST";
'''
import json
import requests
from pprint import pprint

from urllib import urlencode
from eWRT.ws import AbstractWebSource

API_URL = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
REQUEST_URL = ''
class BingTranslator(AbstractWebSource):
    NAME = 'bing_translate'
    SUPPORTED_PARAMS = ('text', 'target_language', 'source_language')
    
    def __init__(self, client_id, client_secret, api_url=None):
        ''' sets the credentials for Bing Translator '''
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_url = api_url if api_url else API_URL
        self._access_token = None
        
    def search_documents(self, search_terms, source_language, target_language):
        ''' translates the `search_terms` from `source_language to the 
        `target_language`
        :returns: iterator with the translated text
        '''
        if isinstance(search_terms, basestring):
            search_terms = [search_terms]
            
        for search_term in search_terms: 
            translation = self.translate(text=search_term, 
                                         source_language=source_language, 
                                         target_language=target_language)
            yield {'text': search_term, 
                   'translation': translation, 
                   'source_language': source_language, 
                   'target_language': target_language}
            
    def translate(self, text, source_language, target_language):
        ''' tranlates the `text` in `source_language` to the `target_language`
        :param text: text to translate
        :type text: str or unicode
        :param source_language: language of the given text (iso-code)
        :param target_language: language to translate to (iso-code)
        :returns: translated text as string
        '''
        api_url = 'http://api.microsofttranslator.com/v2/Ajax.svc/Translate?'
        params = {'text': text, 
                  'from': source_language,
                  'to': target_language
                  }
        pprint(params)
        headers = {'Authorization': 'Bearer %s' % self.access_token}
        resp = requests.get(api_url+urlencode(params), headers=headers)
        return resp.text.replace('"', '')
        
    def get_new_access_token(self):
        params = {'grant_type': 'client_credentials', 
                  'client_id': self.client_id,
                  'client_secret': self.client_secret,
                  'scope': 'http://api.microsofttranslator.com'}
            
        resp = requests.post(self.api_url, data=urlencode(params))
        return json.loads(resp.text)
    
    def get_access_token(self):
        if not self._access_token: 
            self._access_token = self.get_new_access_token()
        
        return self._access_token['access_token']
            
    access_token = property(get_access_token)
    