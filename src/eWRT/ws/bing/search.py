'''
Created on Sep 02, 2014

:author: svakulenko
'''

# Bing API Version 2.0
# sample URL for web search
# https://api.datamarket.azure.com/Bing/Search/Web?$format=json&Query=%27Xbox%27&$top=2

from eWRT.ws.rest import RESTClient
from eWRT.ws import AbstractWebSource
# from pprint import pprint

ROOT_URL = 'https://api.datamarket.azure.com/Bing/Search'
DEFAULT_COMMAND = 'Web'  # Image, News
DEFAULT_START_INDEX = 1


class BingSearch(AbstractWebSource):

    NAME = "Bing Search"

    DEFAULT_MAX_RESULTS = 50  # requires only 1 api access

    DEFAULT_PARAMS = {'$format': 'json'}

    MAPPING = {'date': ('valid_from', 'convert_date'),

               'text': ('content', None),

               'title': 'Title',

               }

    def __init__(self, api_key, username, api_url=ROOT_URL):

        assert(api_key)

        self.api_key = api_key
        self.api_url = api_url
        self.username = username
        self.client = RESTClient(
            self.api_url, password=self.api_key, user=self.username, authentification_method='basic')

    def search_documents(self, search_terms, max_results=DEFAULT_MAX_RESULTS, from_date=None, to_date=None, parameters=DEFAULT_PARAMS):
        ''' runs the actual search / calls the webservice / API ... '''
        # search_params = self._check_params(kwargs)

        # Web search is by default
        for search_term in search_terms:

            if (max_results > self.DEFAULT_MAX_RESULTS):
                mid_results = self.DEFAULT_MAX_RESULTS
                # number of reguests
                for i in range(DEFAULT_START_INDEX, max_results + 1, self.DEFAULT_MAX_RESULTS):
                    # detect the last iteration
                    if (i + self.DEFAULT_MAX_RESULTS > max_results):
                        mid_results = max_results % self.DEFAULT_MAX_RESULTS
                    fetched = self.request(
                        search_term, mid_results, parameters)

                    for item in fetched['d']['results']:
                        try:
                            yield self.convert_item(item)
                        except Exception as e:  # ported to Python3
                            print('Error %s occured' % e)
                            continue
            else:
                fetched = self.request(search_term, max_results, parameters)

                # return fetched

                for item in fetched['d']['results']:
                    try:
                        yield self.convert_item(item)
                    except Exception as e:  # ported to Python3
                        print('Error %s occured' % e)
                        continue

    def request(self, search_term, max_results=DEFAULT_MAX_RESULTS, parameters=DEFAULT_PARAMS, command=DEFAULT_COMMAND):
        ''' searches Bing for the given search_term
        '''
        parameters['Query'] = search_term
        parameters['$top'] = max_results

        response = self.client.execute(command, query_parameters=parameters)
        # print(response)
        return response

    @classmethod
    def convert_item(cls, item):
        ''' applies a mapping to convert the result to the required format
        '''

        result = {'url': item['Url'],
                  'title': item['Title'],
                  }

        return result


class TestBingSearch(object):
    # tested only Web command

    username = 'svitlana.vakulenko@gmail.com'
    my_acmid_results_key = 'kieVYyuW1uwvUnVo3b1+vXWtim6TuxFiYkSpPtloUhI'

    search_terms = ["'modul'", "'university'"]

    # test default api call (max_results = DEFAULT_MAX_RESULTS)
    def test_default(self):
        bs = BingSearch(self.my_acmid_results_key, self.username)

        results = bs.search_documents(self.search_terms)

        # assert the correct number of the results
        assert len(list(results)) == bs.DEFAULT_MAX_RESULTS * \
            len(self.search_terms)

    # test api call with additional parameters
    def test_params(self):
        bs = BingSearch(self.my_acmid_results_key, self.username)

        params = {'$format': 'json'}

        results = bs.search_documents(
            self.search_terms, parameters=params)

        # print(results)
        # assert the correct number of the results
        assert len(list(results)) == bs.DEFAULT_MAX_RESULTS * \
            len(self.search_terms)
        # [pprint(res) for res in results]

    def test_smaller_max_results(self):
        max_results = 4
        bs = BingSearch(self.my_acmid_results_key, self.username)
        results = bs.search_documents(self.search_terms, max_results)

    # assert the correct number of the results
        assert len(list(results)) == max_results * len(self.search_terms)

    def test_larger_max_results(self):
        max_results = 70
        bs = BingSearch(self.my_acmid_results_key, self.username)
        results = bs.search_documents(self.search_terms, max_results)

    # assert the correct number of the results
        assert len(list(results)) == max_results * len(self.search_terms)

if __name__ == '__main__':
    test = TestBingSearch()
    test.test_params()
