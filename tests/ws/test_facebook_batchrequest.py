#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from eWRT.ws.facebook.fbBatchRequest import FbBatchRequest
from eWRT.ws.facebook import FacebookWS
from eWRT.config import FACEBOOK_ACCESS_KEY


class TestFacebookBatchRequest(unittest.TestCase):
    
    def test_bad_request(self):
        ''' '''
        if len(FACEBOOK_ACCESS_KEY)==0:
            print('skipped TestFacebookBatchRequest::test_bad_request due to missing facebook credentials')
            return
        fbBatchRequest = FbBatchRequest(access_token=FACEBOOK_ACCESS_KEY)
        
        try: 
            fbBatchRequest.run_search('Linus Torvalds')
        except Exception as e: 
            print 'thats ok: %s' % e
            assert True
    
    def test_batch_search2(self):
        ''' '''
        if len(FACEBOOK_ACCESS_KEY)==0:
            print('skipped TestFacebookBatchRequest::test_batch_search2 due to missing facebook credentials')
            return
        fbBatchRequest = FbBatchRequest(access_token=FACEBOOK_ACCESS_KEY)
        result = fbBatchRequest.run_search(['Wien'], 'post', 100)
        assert len(result) > 0
    
    def test_feed_mirroring(self):
        ''' '''
        if len(FACEBOOK_ACCESS_KEY)==0:
            print('skipped TestFacebookBatchRequest::test_feed_mirroring due to missing facebook credentials')
            return
        fbBatchRequest = FbBatchRequest(access_token=FACEBOOK_ACCESS_KEY)
        result = fbBatchRequest.run_search('107961012601035/feed', 
                                           objectType='path',
                                           limit=10)
        
        for x in result:
            print x
            
        assert len(result) >= 1

    def test_search(self):
        terms = ['Department of Health and Human Services', 'carcinomas', 
                 'National Oceanic and Atmospheric Administration', 'Mercedes-Benz',
                 'Audi', 'BMW', 'tumour', 'cancer', 'cop18', 'jane lubchenco', 'tumour', 'irgendwas']
        
        fbWSList = []
        
        if len(FACEBOOK_ACCESS_KEY)==0:
            print('skipped TestFacebookBatchRequest::test_search due to missing facebook credentials')
            return
        
        for term in terms: 
            fbWSList.append(FacebookWS(term, 'post', 1353954200, 100))
        
        result = FbBatchRequest._send_post(access_token=FACEBOOK_ACCESS_KEY,
                                           fbWSList=fbWSList)
        print result
        print len(result)
        
if __name__ == "__main__":
    unittest.main()
