#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import unittest

from eWRT.ws.facebook.fbBatchRequest import FbBatchRequest
from eWRT.ws.facebook import FacebookWS
from eWRT.config import FACEBOOK_ACCESS_KEY


class TestFacebookBatchRequest(unittest.TestCase):

    def setUp(self):
        self.api_key = os.getenv('FACEBOOK_ACCESS_KEY') or FACEBOOK_ACCESS_KEY
        if not self.api_key or len(self.api_key) == 0:
            raise unittest.SkipTest(
                'Skipping TestFacebookBatchRequest: missing API key')
        self.fb_batch_client = FbBatchRequest(access_token=self.api_key)

    def test_bad_request(self):
        ''' '''
        try:
            self.fb_batch_client.run_search('Linus Torvalds')
        except Exception as e:
            print('thats ok: %s' % e)
            assert True

    def test_batch_search2(self):
        ''' '''
        result = self.fb_batch_client.run_search(['Wien'], 'post', 100)
        assert len(result) > 0

    def test_feed_mirroring(self):
        ''' '''
        result = self.fb_batch_client.run_search('107961012601035/feed',
                                                 objectType='path',
                                                 limit=10)

        for x in result:
            print(x)

        assert len(result) >= 1

    def test_search(self):
        terms = ['Department of Health and Human Services', 'carcinomas',
                 'National Oceanic and Atmospheric Administration', 'Mercedes-Benz',
                 'Audi', 'BMW', 'tumour', 'cancer', 'cop18', 'jane lubchenco', 'tumour', 'irgendwas']

        fbWSList = []

        if len(FACEBOOK_ACCESS_KEY) == 0:
            print(
                'skipped TestFacebookBatchRequest::test_search due to missing facebook credentials')
            return

        for term in terms:
            fbWSList.append(FacebookWS(term, 'post', 1353954200, 100))

        result = self.fb_batch_client._send_post(access_token=self.api_key,
                                                 fbWSList=fbWSList)
        print(result)
        print(len(result))


if __name__ == "__main__":
    unittest.main()
