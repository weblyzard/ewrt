#!/usr/bin/env python

""" http.py
    - accesses resources using http """

# (C)opyrights 2008 by Albert Weichselbraun <albert@weichselbraun.net>
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

import urllib2
from config import USER_AGENT, DEFAULT_WEB_REQUEST_SLEEP_TIME
import time


class Retrieve(object):
    """ retrieves URL's using http """

    def __init__(self, module, sleep_time=DEFAULT_WEB_REQUEST_SLEEP_TIME):
        self.module = module
        self.sleep_time       = sleep_time
        self.last_access_time = 0


    def open(self, url ):
        """ opens an url """
        request = urllib2.Request( url )
        request.add_header('User-Agent', USER_AGENT % self.module)
        self._throttle()
        return urllib2.build_opener().open( request )


    def _throttle( self ):
        """ delays web access according to the content provider's policy """
        if (time.time() - self.last_access_time) < DEFAULT_WEB_REQUEST_SLEEP_TIME:
            time.sleep( self.sleep_time )
        self.last_access_time= time.time()



if __name__ == '__main__':
    
    from unittest import TestCase, main

    class TestHttp(TestCase):
        """ tests the http class """
        TEST_URLS = ('http://www.google.at/search?hl=de&q=andreas&btnG=Google-Suche&meta=', 
                     'http://www.heise.de' )

        def testRetrieval(self):
            """ tries to retrieve the following url's from the list """

            r_handler = Retrieve( self.__class__.__name__ )
            for url in self.TEST_URLS:
                print url
                r=r_handler.open( url )
                r.read()
                r.close()

    main()

