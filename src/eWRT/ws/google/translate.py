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
import logging
from typing import Union, List, Iterator
from urllib.parse import urlencode

from eWRT.ws import AbstractWebSource
from future import standard_library
import requests
from six import string_types

standard_library.install_aliases()

logger = logging.getLogger(__name__)

API_URL = 'https://www.googleapis.com/language/translate/v2'


class GoogleTranslator(AbstractWebSource):
    NAME = 'google_translate'
    SUPPORTED_PARAMS = ('text', 'target_language', 'source_language')

    def __init__(self, api_key, api_url=API_URL):
        self.api_key = api_key
        self.api_url = api_url

    def search_documents(self, search_terms:Union[List[str], str],
                         source_language:str, target_language:str) -> Iterator[dict]:
        ''' translates the `search_terms` from `source_language to the 
        `target_language`
        :returns: iterator with the translated text
        '''
        if isinstance(search_terms, string_types):  # p2/3 string check
            search_terms = [search_terms]

        for search_term in search_terms:
            logger.info('translating: %s (source=%s;target=%s)',
                             search_term,
                             source_language,
                             target_language)
            result = self.translate(text=search_term,
                                    target_language=target_language,
                                    source_language=source_language)

            translations = []

            if 'error' in result:
                logger.error(result['error'])
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
        # set format to not default to html encoding (in response)
        params['format'] = 'text'
        full_url = self.api_url + path + '?' + urlencode(params)
        resp = requests.get(full_url)
        status = resp.status_code

        text = params['q'].decode('utf-8')
        log_params = f"{text} (source={params['source']};target={params['target']})"
        if status == 200:
            logger.debug(f'translate request successful, {status} ({log_params})')
        else:
            logger.error(f'translate request error, {status} ({log_params})')

        return json.loads(resp.text)

    def translate(self, text, target_language, source_language=None):
        ''' translates the text '''
        if isinstance(text, str):
            text = text.encode('utf8')
        params = {'target': target_language, 'q': text}

        if source_language:
            params['source'] = source_language

        return self._make_request(params)

    def detect_language(self, text):
        ''' detects the language of the given `text` '''
        return self._make_request({'q': text}, path='/detect')
