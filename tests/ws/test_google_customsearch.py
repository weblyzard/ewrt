#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from eWRT.ws.google.custom import CustomSearch


class TestCustomSearch(unittest.TestCase):

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
    unittest.main()