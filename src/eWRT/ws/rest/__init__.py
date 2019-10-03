# -*- coding: UTF-8 -*-
#!/usr/bin/env python

''' .. module:: eWRT.ws.rest
    .. moduleauthor:: Albert Weichselbraun <weichselbraun@weblyzard.com>
    .. moduleauthor:: Heinz-Peter Lang <lang@weblyzard.com>

    eWRT REST Client barebone with support for authentificated https requests
'''
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import range
from builtins import object
import traceback
import logging
import random

try:
    # urllib2 is merged into urllib in python3 (SV)
    from urllib.error import HTTPError
except:
    from urllib.error import HTTPError  # python2

import urllib.request, urllib.parse, urllib.error

try:
    from urllib.parse import urlsplit, urlunsplit  # porting to python 3.4 (SV)
except:
    from urllib.parse import urlsplit, urlunsplit  # python2

from six import string_types
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
                url = url + "?" + urllib.parse.urlencode(query_parameters,
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
            self.request('status')
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

        if isinstance(urls, string_types):
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
                query_parameters=None, content_type='application/json',
                pass_through_exceptions=()):
        ''' performs the given json request
        @param url: the url to query
        @param parameters: optional paramters
        @param pass_through_exceptions:
            set to True, if the client shall pass through all exceptions
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
                if pass_through_exceptions:
                    raise e
                else:
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

    def get_service_urls(self): 
        ''' '''
        return [client.service_url for client in self.clients]
    
    @classmethod
    def get_document_batch(cls, documents, batch_size=None):
        batch_size = batch_size if batch_size else cls.MAX_BATCH_SIZE
        for i in range(0, len(documents), batch_size):
            yield documents[i:i+batch_size]
            
