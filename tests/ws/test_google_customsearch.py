#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from eWRT.ws.google.custom import CustomSearch
from eWRT.config import GOOGLE_CUSTOM_SEARCH_API_KEY,\
    GOOGLE_CUSTOM_SEARCH_ENGINE_ID


class TestCustomSearch(unittest.TestCase):

    search_terms = ['modul', 'university']

    def setUp(self):
        self.api_key = GOOGLE_CUSTOM_SEARCH_API_KEY
        self.engine_id = GOOGLE_CUSTOM_SEARCH_ENGINE_ID

    def test_default(self):
        ''' test default api call '''
        if not len(self.api_key):
            return
        cs = CustomSearch(self.api_key, self.engine_id)
        max_results = cs.DEFAULT_MAX_RESULTS
        results = cs.search_documents(self.search_terms)

        # assert the correct number of the results
        assert len(list(results)) == max_results * len(self.search_terms)

    def test_smaller_max_results(self, max_results=4):
        ''' '''
        if not len(self.api_key):
            return
        cs = CustomSearch(self.my_api_key, self.my_engine_id)

        assert max_results < cs.DEFAULT_MAX_RESULTS

        results = cs.search_documents(self.search_terms, max_results)

        # assert the correct number of the results
        assert len(list(results)) == max_results * len(self.search_terms)

    def test_larger_max_results(self, max_results=21):
        ''' test several api calls (limit > DEFAULT_MAX_RESULTS) '''
        if not len(self.api_key):
            return
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
    unittest.main()