#!/usr/bin/python
# -*- coding: utf-8 -*-
'''

'''
import os
import unittest

from eWRT.ws.bing.search import BingSearch
from eWRT.config import BING_USERNAME, BING_API_KEY


class TestBingSearch(unittest.TestCase):
    # tested only Web command

    def setUp(self):
        self.api_key = os.getenv('BING_USERNAME') or BING_USERNAME
        if not self.api_key or len(self.api_key) == 0:
            raise unittest.SkipTest(
                'Skipping TestBingSearch: missing username')
        self.username = BING_USERNAME
        self.api_key = BING_API_KEY
        self.client = BingSearch(api_key=self.api_key,
                                 username=self.username)

    def test_default(self):
        ''' test default api call (max_results = DEFAULT_MAX_RESULTS) '''
        search_terms = ['modul', 'university']
        results = self.client.search_documents(search_terms)

        # for the testing purposes
        # [ print(res) for res in results ]

        # assert the correct number of the results
        assert len(list(results)) == self.client.DEFAULT_MAX_RESULTS * \
            len(self.search_terms)

    def test_smaller_max_results(self, max_results=4):
        ''' '''
        assert max_results < self.client.DEFAULT_MAX_RESULTS

        results = self.client.search_documents(self.search_terms, max_results)

        # assert the correct number of the results
        assert len(list(results)) == max_results * len(self.search_terms)

    def test_larger_max_results(self, max_results=70):
        ''' '''
        assert max_results > self.client.DEFAULT_MAX_RESULTS
        assert max_results % self.client.DEFAULT_MAX_RESULTS != 0

        results = self.client.search_documents(self.search_terms, max_results)

        # for the testing purposes
        # print(next(results))

        # assert the correct number of the results
        assert len(list(results)) == max_results * len(self.search_terms)


# for the testing purposes
if __name__ == '__main__':
    unittest.main()
