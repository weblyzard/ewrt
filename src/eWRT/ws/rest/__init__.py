# -*- coding: UTF-8 -*-
#!/usr/bin/env python

''' .. module:: eWRT.ws.rest
    .. moduleauthor:: Albert Weichselbraun <weichselbraun@weblyzard.com>
    .. moduleauthor:: Heinz-Peter Lang <lang@weblyzard.com>

    eWRT REST Client barebone with support for authentificated https requests
'''
import traceback
import unittest
import logging
import random

try:
    # urllib2 is merged into urllib in python3 (SV)
    from urllib.error import HTTPError
except:
    from urllib2 import HTTPError  # python2

import urllib

try:
    from urllib.parse import urlsplit, urlunsplit  # porting to python 3.4 (SV)
except:
    from urlparse import urlsplit, urlunsplit  # python2

from json import dumps, loads
from functools import partial
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
        # remove superfluous slashes, if required
        self.service_url = service_url[:-1] if service_url.endswith("/") \
            else service_url
        self.user = user
        self.password = password

        if not default_timeout: 
            default_timeout = WS_DEFAULT_TIMEOUT

        url_obj = Retrieve(module_name, sleep_time=0,
                           default_timeout=default_timeout)
        self.retrieve = partial(url_obj.open,
                                user=user,
                                pwd=password,
                                authentification_method=authentification_method
                                )

    def _json_request(self, url, parameters=None, return_plain=False,
                      json_encode_arguments=True,
                      content_type='application/json'):
        ''' performs the given json request
        :param url: the url to query
        :param parameters: optional paramters
        :param return_plain: whether to return the result without prior
                             deserialization using json.load (False*)
        :param json_encode_arguments: whether to json encode the parameters
                                      (True*)
        :param content_type: one of 'application/json', 'application/xml'
        '''
        if parameters:
            handle = self.retrieve(
                url,
                dumps(parameters) if json_encode_arguments else parameters,
                {'Content-Type': content_type})
        else:
            handle = self.retrieve(url)

        response = handle.read()
        if response:
            return response if return_plain else loads(response.decode('utf8'))
        else:
            # this will also return empty list, dicts ...
            return response

    @staticmethod
    def get_request_url(service_url, command, identifier=None,
                        query_parameters=None):
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
            try:
                url = url + "?" + urllib.parse.urlencode(query_parameters,
                                                         doseq=True)
            except:
                url = url + "?" + urllib.urlencode(query_parameters,
                                                   doseq=True)

        return url

    def execute(self, command, identifier=None, parameters=None,
                return_plain=False, json_encode_arguments=True,
                query_parameters=None, content_type='application/json'):
        ''' executes a json command on the given web service
        :param command: the command to execute
        :param identifier: an optional identifier (e.g. batch_id, ...)
        :param parameters: optional post paramters
        :param return_plain: return the result without prior deserialization
                             using json.load (False*)
        :param json_encode_arguments: whether to json encode the parameters
        :param query_parameters: optional query parameters
        :rtype: the query result
        '''
        url = self.get_request_url(self.service_url, command, identifier,
                                   query_parameters)
        
        logger.debug('requesting url %s' % url)
        
        return self._json_request(url, parameters, return_plain,
                                  json_encode_arguments, content_type)

class MultiRESTClient(object):
    ''' allows multiple URLs for access REST services '''
    MAX_BATCH_SIZE = 500
    URL_PATH = None

    def __init__(self, service_urls, user=None, password=None,
                 default_timeout=WS_DEFAULT_TIMEOUT, use_random_server=False):
        
        self._service_urls = self.fix_urls(service_urls, user, password)
        
        if use_random_server:
            random.shuffle(self._service_urls)
        
        self.clients = self._connect_clients(self._service_urls,
                                             default_timeout=default_timeout)
              
    def is_online(self):
        try:
            self.request('meminfo')
            return True
        except:
            return False

    @classmethod
    def fix_urls(cls, urls, user=None, password=None):
        ''' fixes the urls and put them into the correct format, to maintain
        the compability to the remaining platform
        :param urls: service urls
        :type urls: string or list or tuple
        :param user: username
        :param password: password
        :returns: correctly formated urls
        :rtype: list
        '''
        correct_urls = []

        try:
            if isinstance(urls, basestring):
                urls = [urls]
        except NameError:
            #  basestring no longer exists in python 3, producing an error.
            if isinstance(urls, str):
                urls = [urls]

        for url in urls:
            if not url.endswith('/'):
                url = '%s/' % url

            if not 'rest' in url:
                if cls.URL_PATH and not url.endswith(cls.URL_PATH):
                    if cls.URL_PATH.startswith('/'):
                        cls.URL_PATH = cls.URL_PATH[1:]
                    url = '%s%s' % (url, cls.URL_PATH)

            if user and password:
                url = Retrieve.add_user_password(url, user, password)

            correct_urls.append(url)

        return correct_urls

    @classmethod
    def _connect_clients(cls, service_urls, user=None, password=None,
                         default_timeout=WS_DEFAULT_TIMEOUT):

        clients = []

        if isinstance(service_urls, str):
            service_urls = [service_urls]

        for url in service_urls:
            service_url, user, password = Retrieve.get_user_password(url)

            clients.append(RESTClient(service_url=service_url,
                                      user=user,
                                      password=password,
                                      default_timeout=default_timeout))
        return clients

    def request(self, path, parameters=None, return_plain=False,
                execute_all_services=False, json_encode_arguments=True,
                query_parameters=None, content_type='application/json'):
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
                response = client.execute(
                    command=path,
                    parameters=parameters,
                    return_plain=return_plain,
                    json_encode_arguments=json_encode_arguments,
                    query_parameters=query_parameters,
                    content_type=content_type)

                if not execute_all_services:
                    break

            except Exception as e:  # ported to python3 (SV)
                msg = 'could not execute %s %s, error %s\n%s' % (
                    client.service_url, path, e,
                    traceback.format_exc())
                logger.warn(msg)
                errors.append(msg)

        if len(errors) == len(self.clients):
            print ('\n'.join(errors))
            raise Exception('Could not make request to path %s: %s' % (
                path,
                '\n'.join(errors)))

        return response

    @classmethod
    def get_document_batch(cls, documents, batch_size=None):
        batch_size = batch_size if batch_size else cls.MAX_BATCH_SIZE
        for i in range(0, len(documents), batch_size):
            yield documents[i:i+batch_size]


class TestRESTClient(unittest.TestCase):

    TEST_URL = 'http://test.webdav.org/auth-basic/'
    TEST_USER = 'user1'
    TEST_PASS = 'user1'

    def test_retrieve(self):
        r = RESTClient(self.TEST_URL, self.TEST_USER, self.TEST_PASS)
        try:
            r._json_request(self.TEST_URL)
        except HTTPError as e:
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
        except Exception as e:
            assert 'Could not make request to path' in str(e)
 
        try:
            urls = ('https://heinz@irgendwas.com', )
            client = MultiRESTClient(urls)
            assert False, 'must raise an assertion error'
        except Exception as e:
            print '!!! previous exception is OK, we expected that'
            assert 'if set, user AND pwd required' in e.args # not tested (SV)
 
    def test_get_url(self):
        assert RESTClient.get_request_url(self.TEST_URL, 'execute', '12') \
            .endswith("/execute/12")
        assert RESTClient.get_request_url(
            self.TEST_URL,
            'execute',
            '12',
            {'debug': True}).endswith("/execute/12?debug=True")
 
    def test_fix_url(self):
        ''' tests fix url '''

    def test_randomize_urls(self):
        ''' this test might fail, if random returns the same list, but this is 
        very unlikely ''' 
        client = MultiRESTClient(service_urls='http://test.url', 
                                 use_random_server=True)
        
        assert isinstance(client._service_urls, list)
        assert len(client._service_urls) == 1
    
        service_urls = ['http://test.url%s' % i for i in range(1000)]
    
        client = MultiRESTClient(service_urls=service_urls, 
                                 use_random_server=True)
        
        assert len(client._service_urls) == len(service_urls)
        assert service_urls <> client._service_urls
        
if __name__ == '__main__':
    unittest.main()
