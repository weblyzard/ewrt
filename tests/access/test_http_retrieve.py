#!/usr/bin/env python

''' @package eWRT.access.http
    provides access to resources using http '''
from __future__ import print_function

# (C)opyrights 2008-2012 by Albert Weichselbraun <albert@weblyzard.com>
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
import unittest
import urllib.request, urllib.error, urllib.parse

from pytest import raises
from socket import timeout

from eWRT.access.http import DEFAULT_TIMEOUT, Retrieve, setdefaulttimeout, log


class TestHttpRetrieve(unittest.TestCase):
    ''' tests the http class '''

    TEST_URLS = (
        'http://www.google.at/search?hl=de&q=andreas&btnG=Google-Suche&meta=',
        'http://www.heise.de')

    def setUp(self):
        from logging import StreamHandler
        self.default_timeout = DEFAULT_TIMEOUT

        # set logging handler
        log.addHandler(StreamHandler())

    def tearDown(self):
        setdefaulttimeout(self.default_timeout)

    def testRetrieval(self):
        ''' tries to retrieve the following url's from the list '''

        r_handler = Retrieve(self.__class__.__name__)
        for url in self.TEST_URLS:
            print(url)
            r = r_handler.open(url)
            r.read()
            r.close()

    def testRetrieveContext(self):
        ''' tests the retrieve context module '''
        with Retrieve(self.__class__.__name__) as r:
            c = r.open("http://www.heise.de")
            content = c.read()
        assert len(content) > 100

    def testRetrievalTimeout(self):
        ''' tests whether the socket timeout is honored by our class '''
        SLOW_URL = "http://www.csse.uwa.edu.au/"

        with raises((timeout, urllib.error.URLError)):
            r = Retrieve(self.__class__.__name__,
                         default_timeout=0.1).open(SLOW_URL)
            content = r.read()
            r.close()

    def testMultiProcessing(self):
        ''' verifies that retrieves works with multi-processing '''
        from multiprocessing import Pool
        p = Pool(5)

        TEST_URLS = ['http://www.heise.de',
                     # 'http://linuxtoday.com', # site anavailable (2020-06)
                     'http://www.kurier.at',
                     'http://www.diepresse.com',
                     'http://www.spiegel.de',
                     'http://www.sueddeutsche.de',
                     ]
        results = []
        for res in p.map(t_retrieve, TEST_URLS):
            assert len(res) > 20

    def testGettingUserPassword(self):
        urls = (('http://irgendwas.com', None, None),
                ('http://heinz:secret@irgendwas.com', 'heinz', 'secret'))

        for test_url, exp_user, exp_passwd in urls:
            print('testing url ' + test_url)
            url, user, passwd = Retrieve.get_user_password(test_url)
            assert user == exp_user
            assert passwd == exp_passwd
            if user:
                assert url != test_url


def t_retrieve(url):
    ''' retrieves the given url from the web

        @remarks
        helper module for the testMultiProcessing unit test.
    '''
    r = Retrieve(__name__).open(url)
    try:
        content = r.read()
    finally:
        # this is required as GzipFile does not support the context protocol
        # in python 2.6
        r.close()
    return content

if __name__ == '__main__':
    unittest.main()
