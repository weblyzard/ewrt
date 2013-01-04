# -*- coding: UTF-8 -*-
#!/usr/bin/env python

""" @package eWRT.ws.rest
eWRT REST Client barebone with support for authentificated https requests
"""

import urllib2, urllib
from json import dumps, loads
from functools import partial
from unittest import TestCase, main
from urllib2 import HTTPError

from eWRT.access.http import Retrieve

class RESTClient(object):

    def __init__(self, user=None, password=None,
                 authentification_method='basic',
                 module_name='eWRT.REST'):
        """ @param modul_name: the module name to add to the USER AGENT
                               description (optional)
            @param user: username
            @param password: password
            @param authentification_method: authentification method to use
                                            ('basic'*, 'digest'). 
        """
        url_obj = Retrieve(module_name, sleep_time=0)
        self.retrieve = partial(url_obj.open,
                                user= user,
                                pwd = password,
                                authentification_method = authentification_method)

    def json_request(self, url, parameters=None):
        """ performs the given json request
        @param url: the url to query
        @param parameters: optional paramters
        """
        if parameters:
            handle = self.retrieve( url , dumps( parameters ),
                                 {'Content-Type': 'application/json'})
        else:
            handle = self.retrieve( url )
            
        response = handle.read()
        if response:
            return loads(response)


class TestRESTClient(TestCase):
    
    TEST_URL  = 'http://test.webdav.org/auth-basic/'
    TEST_USER = 'user1'
    TEST_PASS = 'user1'
    
    def test_retrieve(self):
        r = RESTClient(self.TEST_USER, self.TEST_PASS)
        try:
            r.json_request(self.TEST_URL)
        except HTTPError, e:
            # authentification has been succeeded, but no object could
            # be found
            assert '404: Not Found' in str(e)
        
    

if __name__ == '__main__':
    main()