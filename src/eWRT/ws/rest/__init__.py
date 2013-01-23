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

    def __init__(self, service_url, user=None, password=None,
                 authentification_method='basic',
                 module_name='eWRT.REST'):
        """ @param service_url: the base url of the web service
            @param modul_name: the module name to add to the USER AGENT
                               description (optional)
            @param user: username
            @param password: password
            @param authentification_method: authentification method to use
                                            ('basic'*, 'digest'). 
        """
        self.service_url = service_url

        url_obj = Retrieve(module_name, sleep_time=0)
        self.retrieve = partial(url_obj.open,
                                user= user,
                                pwd = password,
                                authentification_method = authentification_method)


    def _json_request(self, url, parameters=None, return_plain=False):
        """ performs the given json request
        @param url: the url to query
        @param parameters: optional paramters
        @param return_plain: whether to return the result without prior deserialization
                             using json.load (False*)
        """
        if parameters:
            handle = self.retrieve( url , dumps( parameters ),
                                    {'Content-Type': 'application/json'})
        else:
            handle = self.retrieve( url )
            
        response = handle.read()
        if response:
            return response if return_plain else loads(response)

    def execute(self, command, identifier=None, parameters=None, return_plain=False):
        """ executes a json command on the given web service
        @param command: the command to execute
        @param identifier: an optional identifier (e.g. batch_id, ...)
        @param parameters: optional paramters
        @param return_plain: return the result without prior deserialization
                             using json.load (False*)
        """
        url = '%s/%s/%s' % (self.service_url, command, identifier) \
            if identifier else "%s/%s" % (self.service_url, command)
        return self._json_request(url, parameters, return_plain)


class TestRESTClient(TestCase):
    
    TEST_URL  = 'http://test.webdav.org/auth-basic/'
    TEST_USER = 'user1'
    TEST_PASS = 'user1'
    
    def test_retrieve(self):
        r = RESTClient(self.TEST_URL, self.TEST_USER, self.TEST_PASS)
        try:
            r._json_request(self.TEST_URL)
        except HTTPError, e:
            # authentification has been succeeded, but no object could
            # be found
            assert '404: Not Found' in str(e)
        
    

if __name__ == '__main__':
    main()
