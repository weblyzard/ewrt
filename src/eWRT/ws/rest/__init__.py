# -*- coding: UTF-8 -*-
#!/usr/bin/env python

''' module:: eWRT.ws.rest
    moduleauthor:: Albert Weichselbraun <weichselbraun@weblyzard.com>
    moduleauthor:: Heinz-Peter Lang <lang@weblyzard.com>

    eWRT REST Client barebone with support for authentificated https requests
'''
import traceback
import unittest
import logging
import urllib2
import urllib
import urlparse
from json import dumps, loads
from functools import partial
from urllib2 import HTTPError
from socket import setdefaulttimeout

from eWRT.access.http import Retrieve

# set higher timeout values 
WS_DEFAULT_TIMEOUT = 900

logger = logging.getLogger('eWRT.ws.rest')

class RESTClient(object):
    '''
    class:: RESTClient
    '''

    def __init__(self, service_url, user=None, password=None,
                 authentification_method='basic',
                 module_name='eWRT.REST', default_timeout=WS_DEFAULT_TIMEOUT):
        ''' :param service_url: the base url of the web service
            :param modul_name: the module name to add to the USER AGENT
                               description (optional)
            :param user: username
            :param password: password
            :param authentification_method: authentification method to use
                                            ('basic'*, 'digest'). 
        '''
        setdefaulttimeout(default_timeout)
        # remove superfluous slashes, if required
        self.service_url = service_url[:-1] if service_url.endswith("/") else service_url
        self.user = user
        self.password = password

        url_obj = Retrieve(module_name, sleep_time=0)
        self.retrieve = partial(url_obj.open,
                                user= user,
                                pwd = password,
                                authentification_method = authentification_method)


    def _json_request(self, url, parameters=None, return_plain=False, json_encode_arguments=True):
        ''' performs the given json request
        :param url: the url to query
        :param parameters: optional paramters
        :param return_plain: whether to return the result without prior deserialization
                            using json.load (False*)
        :param json_encode_arguments: whether to json encode the parameters (True*)
        '''
        if parameters:
            handle = self.retrieve( url , dumps( parameters ) if json_encode_arguments else parameters,
                                    {'Content-Type': 'application/json'})
        else:
            handle = self.retrieve( url )
            
        response = handle.read()
        if response:
            return response if return_plain else loads(response)
        else:
            # this will also return empty list, dicts ... 
            return response

    @staticmethod
    def get_request_url(service_url, command, identifier=None, query_parameters=None):
        '''
        Returns the request url given the command and query parameters
        :param base_url: the base url of the web service
        :param command: the command to execute at the web service
        :param identifier: an optional identifier (e.g. batch_id, ...)
        :param query_parameters: query parameters to include in the url
                                 (e.g. execute?debug=True
        :rtype: the complete request url
        '''
        # remove superfluous slashes
        if command.startswith("/"):
            command = command[1:]

        url = '%s/%s/%s' % (service_url, command, identifier) \
            if identifier else "%s/%s" % (service_url, command)

        # add query string, if necessary
        if query_parameters:
            url = url + "?" + urllib.urlencode(query_parameters)

        return url

    def execute(self, command, identifier=None, parameters=None, 
                return_plain=False, json_encode_arguments=True,
                query_parameters=None):
        ''' executes a json command on the given web service
        :param command: the command to execute
        :param identifier: an optional identifier (e.g. batch_id, ...)
        :param parameters: optional post paramters
        :param return_plain: return the result without prior deserialization
                             using json.load (False*)
        :param json_encode_arguments: whether to json encode the parameters
        :param query_parameters: optional query parameters
        '''
        url = self.get_request_url(self.service_url, command, identifier, 
                        query_parameters)
        return self._json_request(url, parameters, return_plain, 
                        json_encode_arguments)


class MultiRESTClient(object):
    ''' allows multiple URLs for access REST services '''

    def __init__(self, service_urls):
        ''' '''  
        self._service_urls = service_urls
        self.clients = self._connect_clients(self._service_urls) 
    
    @classmethod
    def _connect_clients(cls, service_urls):

        clients = []
        if isinstance(service_urls, basestring):
            service_urls = [service_urls]
            
        for url in service_urls:
            service_url, user, password = Retrieve.get_user_password(url)
       
            clients.append(RESTClient(service_url=service_url, 
                                      user=user, password=password)) 
        return clients
 
    def request(self, path, parameters=None, return_plain=False, 
                execute_all_services=False):
        ''' performs the given json request
        @param url: the url to query
        @param parameters: optional paramters
        @param return_plain: whether to return the result without prior
                             deserialization using json.load (False*)
        ''' 
        response = None
        errors = []
        for client in self.clients:
            try:
                response = client.execute(self, command=path, 
                                parameters=parameters, return_plain=return_plain)

                if not execute_all_services:
                    break
            except Exception, e:
                msg = 'could not execute %s, error %s\n%s' % (path, e, 
                                                              traceback.format_exc())
                logger.warn(msg)
                errors.append(msg)
         
        if len(errors) == len(self.clients):
            print '\n'.join(errors)
            raise Exception('Could not make request to path %s: %s' % (path,
                                                                       '\n'.join(errors)))
        
        return response
        
class TestRESTClient(unittest.TestCase):
    
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

    def test_multi_request(self):
        urls = (('http://irgendwas.com', None, None),
                ('http://heinz:secret@irgendwas.com', 'heinz', 'secret'))
        service_urls = [url[0] for url in urls] 
        client = MultiRESTClient(service_urls)
        
        for i, (service_url, user, passwd) in enumerate(urls): 
            c = client.clients[i]
            if user: 
                assert service_url != c.service_url
            assert c.user == user
            assert c.password == passwd 
       
        try: 
            client.request('irgendwas') 
            assert False
        except Exception, e:
            assert 'Could not make request to path' in str(e)
        
        try: 
            urls = ('https://heinz@irgendwas.com', )
            client = MultiRESTClient(urls)
            assert False, 'must raise an assertion error'
        except Exception, e:
            assert 'if set, user AND pwd required' in e

    def test_get_url(self):
        assert RESTClient.get_request_url(self.TEST_URL, 'execute', '12') \
                    .endswith("/execute/12")
        assert RESTClient.get_request_url(self.TEST_URL, 'execute', '12', {'debug': True}) \
                    .endswith("/execute/12?debug=True")
            

if __name__ == '__main__':
    unittest.main()
