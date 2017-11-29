#!/usr/bin/python
# -*- coding: utf-8 -*-
'''

'''
import unittest

from eWRT.ws.bing.search import BingSearch
from eWRT.config import BING_USERNAME, BING_API_KEY


class TestBingSearch(unittest.TestCase):
    # tested only Web command

    username = BING_USERNAME
    api_key = BING_API_KEY

    search_terms = ['modul', 'university']

    # test default api call (max_results = DEFAULT_MAX_RESULTS)
    def test_default(self):
        bs = BingSearch(api_key=self.api_key, 
                        username=self.username)

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
    unittest.main()
