#!/usr/bin/env python

''' @package eWRT.access.http
    provides access to resources using http '''
from __future__ import print_function


# (C)opyrights 2008-2015 by Albert Weichselbraun <albert@weblyzard.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from future import standard_library
standard_library.install_aliases()
from builtins import object
try:
    # urllib2 is merged into urllib in python3 (SV)
    # import urllib.request as urllib2  # [mig] urllib2 --> urllib in py3
    import urllib, urllib.request  # [mig]
except:
    import urllib.request, urllib.error, urllib.parse  # python2

from eWRT.config import (USER_AGENT, DEFAULT_WEB_REQUEST_SLEEP_TIME,
                         PROXY_SERVER)

#USER_AGENT = 'eWRT Version/0.1; Module %s +http://p.semanticlab.net/eWRT'
#DEFAULT_WEB_REQUEST_SLEEP_TIME = 1
#PROXY_SERVER = None

try:
    from urllib.parse import urlsplit, urlunsplit  # porting to python 3.4 (SV)
except:
    from urllib.parse import urlsplit, urlunsplit  # python2

import time
import io

from gzip import GzipFile
from random import randint


# logging
import logging
log = logging.getLogger(__name__)

RETRY_WAIT_TIME_RANGE = (2, 10)              # in seconds
# error codes which might trigger a retry:
HTTP_TEMPORARY_ERROR_CODES = (500, 503, 504)

# set default socket timeout (otherwise urllib might hang!)
from socket import setdefaulttimeout
DEFAULT_TIMEOUT = 60


def getHostName(x): return "://".join(urlsplit(x)[:2])


class Retrieve(object):
    ''' @class Retrieve
        retrieves URLs using HTTP

        .. remarks:
           this class supports transparent
           - authentication and
           - compression
           - support for the context protocol (python)
           - automatic throttling support

        @warning
        There are certain urls such as
        http://www.mfsa.com.mt/insguide/english/glossarysearch.jsp?letter=all
        which are _not_ handled correctly by the underlying urllib2 library(!)
        Please use urllib in such cases.

    '''

    __slots__ = ('module', 'sleep_time', 'last_access_time', 'user_agent',
                 '_supported_http_authentification_methods')

    def __init__(self, module, sleep_time=DEFAULT_WEB_REQUEST_SLEEP_TIME,
                 user_agent=USER_AGENT, default_timeout=DEFAULT_TIMEOUT):
        setdefaulttimeout(default_timeout)
        self.module = module
        self.sleep_time = sleep_time
        self.last_access_time = 0

        self._supported_http_authentification_methods = {
            'basic': Retrieve._getHTTPBasicAuthOpener,
            'digest': Retrieve._getHTTPDigestAuthOpener}

        self.user_agent = user_agent % self.module \
            if "%s" in user_agent else user_agent

    def open(self, url, data=None, headers={}, user=None, pwd=None, retry=0,
             authentification_method="basic", accept_gzip=True,
             head_only=False):
        ''' Opens an URL and returns the matching file object
            @param[in] url
            @param[in] data    optional data to submit
            @param[in] headers a dictionary of optional headers
            @param[in] user    optional user name
            @param[in] pwd     optional password
            @param[in] retry   number of retries in case of an temporary error
            @param[in] authentification_method the used authentification_method
                        ('basic'*, 'digest')
            @param[in] accept_gzip flag to change the accepted encoding, gzip
                        or not
            @param[in] head_only   if True: only execute a HEAD request
            @returns a file object for reading the url
        '''
        auth_handler = self._supported_http_authentification_methods[
            authentification_method]
        urlObj = None
        tries = 0
        while not urlObj:
            request = urllib.request.Request(url, data, headers)

            if head_only:
                request.get_method = lambda: 'HEAD'

            request.add_header('User-Agent', self.user_agent)

            if accept_gzip:
                request.add_header('Accept-encoding', 'gzip')

            self._throttle()

            opener = []
            if PROXY_SERVER:
                opener.append(urllib.request.ProxyHandler({"http": PROXY_SERVER}))
            if user and pwd:
                opener.append(auth_handler(url, user, pwd))

            urllib.request.install_opener(urllib.request.build_opener(*opener))
            try:
                urlObj = urllib.request.urlopen(request)
            except urllib.error.HTTPError as e:
                if e.code in HTTP_TEMPORARY_ERROR_CODES and tries < retry:
                    time.sleep(randint(*RETRY_WAIT_TIME_RANGE))
                    tries += 1
                    continue
                else:
                    raise e

            # check whether the data stream is compressed
            if urlObj.headers.get('Content-Encoding') == 'gzip':
                return self._getUncompressedStream(urlObj)

        return urlObj

    @staticmethod
    def _getHTTPBasicAuthOpener(url, user, pwd):
        ''' returns an opener, capable of handling http-auth '''
        passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, user, pwd)
        auth_handler = urllib.request.HTTPBasicAuthHandler(passman)
        return auth_handler

    @staticmethod
    def _getHTTPDigestAuthOpener(url, user, pwd):
        '''
        returns an opener, capable of handling http-digest authentification
        '''
        passwdmngr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        passwdmngr.add_password('realm', url, user, pwd)
        auth_handler = urllib.request.HTTPDigestAuthHandler(passwdmngr)
        return auth_handler

    @staticmethod
    def _getUncompressedStream(urlObj):
        ''' transparently uncompressed the given data stream
            @param[in] urlObj
            @returns an urlObj containing the uncompressed data
        '''
        compressedStream = io.BytesIO(urlObj.read())
        return GzipFile(fileobj=compressedStream)

    def _throttle(self):
        ''' delays web access according to the content provider's policy '''

        if (time.time() - self.last_access_time) < \
                DEFAULT_WEB_REQUEST_SLEEP_TIME:
            time.sleep(self.sleep_time)
        self.last_access_time = time.time()

    def __enter__(self):
        ''' support of the context protocol '''
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        ''' context protocol support '''
        if exc_type is not None:
            log.critical("%s" % exc_type)

    @staticmethod
    def get_user_password(url):
        ''' returns the url, username, password if present in the url
        @param url: well formed url, starting with a schema
        @return: tuple (new_url, user, password) '''
        if not url.startswith('http'):
            url = 'http://%s' % url

        split_url = urlsplit(url)
        user = split_url.username
        password = split_url.password
        if user and password:
            new_url = (split_url.scheme,
                       split_url.netloc.replace('%s:%s@' % (user, password),
                                                ''),
                       split_url.path,
                       split_url.query,
                       split_url.fragment)
            url = urlunsplit(new_url)
        else:
            assert not user and not password, 'if set, user AND pwd required'

        return url, user, password

    @staticmethod
    def add_user_password(url, user, password):
        split_url = urlsplit(url)
        return urlunsplit((split_url.scheme,
                           '%s:%s@%s' % (user, password, split_url.netloc),
                           split_url.path,
                           split_url.query,
                           split_url.fragment))
