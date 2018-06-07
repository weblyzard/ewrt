#!/usr/bin/env python

'''
Created on Aug 30, 2014

:author: svakulenko
'''

from eWRT.ws.rest import RESTClient
from eWRT.ws import AbstractIterableWebSource


def RESULT_PATH(x): return x['items']  # path to the results


class CustomSearch(AbstractIterableWebSource):

    """wrapper for the Google Custom Search API"""

    NAME = "Google Custom Search"
    ROOT_URL = 'https://www.googleapis.com/customsearch'
    DEFAULT_MAX_RESULTS = 10  # requires only 1 api access
    SUPPORTED_PARAMS = ['command', 'output_format', 'language']
    DEFAULT_COMMAND = 'v1'
    DEFAULT_FORMAT = 'json'
    DEFAULT_START_INDEX = 1

    DEFAULT_RESULT_LANGUAGE = 'lang_de'  # lang_en

    MAPPING = {'date': ('valid_from', 'convert_date'),
               'text': ('content', None),
               'title': 'Title',
               }

    def __init__(self, api_key, engine_id, api_url=ROOT_URL):
        """fixes the credentials and initiates the RESTClient"""

        assert(api_key)
        self.api_key = api_key

        assert(engine_id)
        self.engine_id = engine_id

        self.api_url = api_url
        self.client = RESTClient(self.api_url, authentification_method='basic')

    def search_documents(self, search_terms, max_results=DEFAULT_MAX_RESULTS,
                         from_date=None, to_date=None, command=DEFAULT_COMMAND,
                         output_format=DEFAULT_FORMAT,
                         language=DEFAULT_RESULT_LANGUAGE):
        """calls iterator and results' post-processor"""

        fetched = self.invoke_iterator(search_terms, max_results, from_date,
                                       to_date, command, output_format, language)

        return self.process_output(fetched, RESULT_PATH)

    def request(self, search_term, current_index,
                max_results=DEFAULT_MAX_RESULTS, from_date=None, to_date=None,
                command=DEFAULT_COMMAND, output_format=DEFAULT_FORMAT,
                language=DEFAULT_RESULT_LANGUAGE):
        """calls Google Custom Search API"""
        parameters = {'q': '"%s"' % search_term,
                      'alt': output_format,
                      'cx': self.engine_id,
                      'key': self.api_key,
                      'num': max_results,
                      'start': current_index,
                      'sort': 'date'}

        # set language
        if language is not None and not language.startswith('lang_') and len(language) == 2:
            language = 'lang_{}'.format(language)
        if language is not None and len(language) == 7:
            parameters['lr'] = language

        response = self.client.execute(command, query_parameters=parameters)
        return response

    @classmethod
    def convert_item(cls, item):
        """output convertor: applies a mapping to convert
        the result to the required format
        """

        result = {'url': item['link'],
                  'title': item['title'],
                  }

        return result
