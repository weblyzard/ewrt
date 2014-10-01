'''
Created on Sep 02, 2014

:author: svakulenko
'''

# Bing API Version 2.0
# sample URL for web search
# https://api.datamarket.azure.com/Bing/Search/Web?$format=json&Query=%27Xbox%
# 27&$top=2

from eWRT.ws.rest import RESTClient
from eWRT.ws import AbstractIterableWebSource


class BingSearch(AbstractIterableWebSource):

    """wrapper for the Bing Search API"""

    NAME = "Bing Search"
    ROOT_URL = 'https://api.datamarket.azure.com/Bing/Search'
    DEFAULT_MAX_RESULTS = 50  # requires only 1 api access
    SUPPORTED_PARAMS = ['command', 'output_format']
    DEFAULT_COMMAND = 'Web'  # Image, News
    DEFAULT_FORMAT = 'json'
    DEFAULT_START_INDEX = 0
    RESULT_PATH = lambda x: x['d']['results']  # path to the results in json

    MAPPING = {'date': ('valid_from', 'convert_date'),
               'text': ('content', None),
               'title': 'Title',
               }

    def __init__(self, api_key, username, api_url=ROOT_URL):
        """fixes the credentials and initiates the RESTClient"""

        assert(api_key)

        self.api_key = api_key
        self.api_url = api_url
        self.username = username
        self.client = RESTClient(
            self.api_url, password=self.api_key, user=self.username,
            authentification_method='basic')

    def search_documents(self, search_terms, max_results=DEFAULT_MAX_RESULTS,
                         from_date=None, to_date=None, command=DEFAULT_COMMAND,
                         output_format=DEFAULT_FORMAT):
        """calls iterator and results' post-processor"""
        # Web search is by default
        fetched = self.invoke_iterator(search_terms, max_results, from_date,
                                       to_date, command, output_format)

        result_path = lambda x: x['d']['results']
        return self.process_output(fetched, result_path)

    def request(self, search_term, current_index,
                max_results=DEFAULT_MAX_RESULTS, from_date=None,
                to_date=None, command=DEFAULT_COMMAND,
                output_format=DEFAULT_FORMAT):
        """calls Bing Search API"""

        parameters = {'Query': search_term,
                      '$format': output_format,
                      '$top': max_results,
                      '$skip': current_index}

        # for testing purposes
        # print(current_index, max_results, search_term)

        response = self.client.execute(command, query_parameters=parameters)
        return response

    @classmethod
    def convert_item(cls, item):
        """output convertor: applies a mapping to convert
        the result to the required format
        """

        result = {'url': item['Url'],
                  'title': item['Title'],
                  }

        return result


class TestBingSearch(object):
    # tested only Web command

    username = 'svitlana.vakulenko@gmail.com'
    my_acmid_results_key = 'kieVYyuW1uwvUnVo3b1+vXWtim6TuxFiYkSpPtloUhI'

    search_terms = ['modul', 'university']

    # test default api call (max_results = DEFAULT_MAX_RESULTS)
    def test_default(self):
        bs = BingSearch(self.my_acmid_results_key, self.username)

        results = bs.search_documents(self.search_terms)

        # for the testing purposes
        # [ print(res) for res in results ]

        # assert the correct number of the results
        assert len(list(results)) == bs.DEFAULT_MAX_RESULTS * \
            len(self.search_terms)

    def test_smaller_max_results(self, max_results=4):
        bs = BingSearch(self.my_acmid_results_key, self.username)

        assert max_results < bs.DEFAULT_MAX_RESULTS

        results = bs.search_documents(self.search_terms, max_results)

        # assert the correct number of the results
        assert len(list(results)) == max_results * len(self.search_terms)

    def test_larger_max_results(self, max_results=70):
        bs = BingSearch(self.my_acmid_results_key, self.username)

        assert max_results > bs.DEFAULT_MAX_RESULTS
        assert max_results % bs.DEFAULT_MAX_RESULTS != 0

        results = bs.search_documents(self.search_terms, max_results)

        # for the testing purposes
        # print(next(results))

        # assert the correct number of the results
        assert len(list(results)) == max_results * len(self.search_terms)


# for the testing purposes
if __name__ == '__main__':
    test = TestBingSearch()
    test.test_larger_max_results()
