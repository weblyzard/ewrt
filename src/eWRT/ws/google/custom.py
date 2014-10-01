#!/usr/bin/env python

'''
Created on Aug 30, 2014

:author: svakulenko
'''

from eWRT.ws.rest import RESTClient
from eWRT.ws import AbstractIterableWebSource


class CustomSearch(AbstractIterableWebSource):

    """wrapper for the Google Custom Search API"""

    NAME = "Google Custom Search"
    ROOT_URL = 'https://www.googleapis.com/customsearch'
    DEFAULT_MAX_RESULTS = 10  # requires only 1 api access
    SUPPORTED_PARAMS = ['command', 'output_format', 'language']
    DEFAULT_COMMAND = 'v1'
    DEFAULT_FORMAT = 'json'
    DEFAULT_START_INDEX = 1
    RESULT_PATH = lambda x: x['items']  # path to the results
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
                                       to_date, command, output_format)

        result_path = lambda x: x['items']
        return self.process_output(fetched, result_path)

    def request(self, search_term, current_index,
                max_results=DEFAULT_MAX_RESULTS, from_date=None, to_date=None,
                command=DEFAULT_COMMAND, output_format=DEFAULT_FORMAT,
                language=DEFAULT_RESULT_LANGUAGE):
        """calls Google Custom Search API"""

        parameters = {'q': '"%s"' % search_term,
                      'alt': output_format,
                      'cx': self.engine_id,
                      'key': self.api_key,
                      'lr': language,
                      'num': max_results,
                      'start': current_index}

        # for testing purposes
        # print(current_index, max_results, search_term)

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


class TestCustomSearch(object):

    # provide your google api key for browser applications (from Developers
    # Console)
    my_api_key = 'AIzaSyAlXco-6Bpikl0Ji2H9NEloe4OsL-pUs2g'
    # provide your Custom search engine ID
    my_engine_id = '013438061017685574719:90y0qqxdojg'

    search_terms = ['modul', 'university']

    # test default api call
    def test_default(self):
        cs = CustomSearch(self.my_api_key, self.my_engine_id)
        max_results = cs.DEFAULT_MAX_RESULTS
        results = cs.search_documents(self.search_terms)

        # assert the correct number of the results
        assert len(list(results)) == max_results * len(self.search_terms)

    def test_smaller_max_results(self, max_results=4):
        cs = CustomSearch(self.my_api_key, self.my_engine_id)

        assert max_results < cs.DEFAULT_MAX_RESULTS

        results = cs.search_documents(self.search_terms, max_results)

        # assert the correct number of the results
        assert len(list(results)) == max_results * len(self.search_terms)

    # test several api calls (limit > DEFAULT_MAX_RESULTS)
    def test_larger_max_results(self, max_results=21):
        cs = CustomSearch(self.my_api_key, self.my_engine_id)

        assert max_results > cs.DEFAULT_MAX_RESULTS
        assert max_results % cs.DEFAULT_MAX_RESULTS != 0

        results = cs.search_documents(self.search_terms, max_results)

        # for the testing purposes
        # print(next(results))

        # assert the correct number of the results
        assert len(list(results)) == max_results * len(self.search_terms)

# for the testing purposes
if __name__ == '__main__':
    test = TestCustomSearch()
    test.test_larger_max_results()
