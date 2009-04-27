#!/usr/bin/env python

""" unittests covering the del.icio.us functions provided by eWRT """

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


from __init__ import Delicious
import unittest

DELICIOUS_TEST_URLS = ( 'http://www.iaeste.at', 'http://www.wu-wien.ac.at', 'http://www.heise.de', 
                        'http://www.kurier.at', 'http://news.bbc.co.uk', )


class DeliciousTest( unittest.TestCase ):

    def test(self):
        for url in DELICIOUS_TEST_URLS:
            print Delicious.delicious_info_retrieve(url)



if __name__ == '__main__':
    unittest.main()

