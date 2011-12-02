#!/usr/bin/env python

# (C)opyrights 2008-2009 by Albert Weichselbraun <albert@weichselbraun.net>
#                           Heinz-Peter Lang <heinz@langatium.net>
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

__version__ = "$Header$"

import re, unittest, optparse, sys, logging, StringIO
from eWRT.access.http import Retrieve
import time
import datetime
from xml.dom.minidom import parse, parseString
from lxml import etree

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
SEARCH_URL = 'http://www.google.com/search?hl=en&ie=UTF-8&lr=&tbm=blg{maxAge}&q={searchTerm}&num={number}&safe=active&start={start}'

# Google displays a maximum 100 results per page
MAX_RESULTS_PAGE = 100
SLEEP_TIME = 10

class GoogleBlogSearch(object):
    ''' implements functions for accessing Google's Blogsearch '''

    @staticmethod
    def get_content(url, sleep_time=SLEEP_TIME):
        ''' fetches the content
        @param url: url to fetch
        @param sleep_time: time to sleep
        @return: HTML string'''
        assert(url.startswith("http"))
        return Retrieve("GoogleBlogSearch",
                        sleep_time=sleep_time).open(url).read()

    @staticmethod
    def get_blog_links(searchTerm, maxResults=100, offset=0, maxAge=0):
        ''' returns a list of URLs 
        @param searchTerm:
        @param maxResult:
        @param offset:
        @param maxAge:
        @return:     
        '''

        if isinstance(searchTerm, list):
            searchTerm = '+'.join(searchTerm)

        searchTerm = re.sub(' ', '+', searchTerm)

        if maxAge > 0:
            dateFormat = '%m/%d/%Y'
            max = datetime.date.today().strftime(dateFormat)
            min = (datetime.date.today() - datetime.timedelta(days=maxAge)).strftime(dateFormat)
            maxAgeString = '&tbs=cdr:1,cd_min:{min},cd_max:{max}'.format(
                                                min=min, max=max)
        else:
            maxAgeString = ''

        url = SEARCH_URL.format(searchTerm=searchTerm, start=offset,
                                number=maxResults, maxAge=maxAgeString)

        tree = etree.HTML(GoogleBlogSearch.get_content(url))
        resultList = tree.xpath('.//div[@id="ires"]/ol')

        counter = 0
        firstElement = True
        urls = []

        for element in resultList[0].iterchildren():
            if firstElement:
                firstElement = False
            else:
                url = element.xpath('./h3[@class="r"]/a')[0].attrib['href']
                linkDate = element.xpath('./div[@class="s"]/span[@class="f"]')[0].text
                abstract = ' '.join(element.xpath('./div[@class="s"]/text()'))

                blogLink = {}
                blogLink['url'] = url
                blogLink['source'] = 'GoogleBlogSearch - Keyword "%s"' % searchTerm
                blogLink['abstract'] = abstract
                blogLink['reach'] = '0'
                blogLink['date'] = linkDate

                m = re.match('(\d{1,2} \w* \d{2,4})', linkDate)

                if m:
                    linkDate = datetime.datetime.strptime(m.groups()[0], '%d %b %Y')
                    blogLink['date'] = linkDate

                urls.append(blogLink)

                counter += 1

                if (counter + offset) >= maxResults:
                    break

        if maxResults > (MAX_RESULTS_PAGE) and (counter + offset) < maxResults:

            urls.extend(GoogleBlogSearch.get_blog_links(searchTerm,
                        maxResults=maxResults, offset=(counter + offset) ,
                        maxAge=maxAge))
        return urls

class TestGoogleSearch(unittest.TestCase):
    ''' '''

    def setUp(self):
        ''' set up'''
        self.search = GoogleBlogSearch()

    def test_get_url(self):
        ''' tests getting the urls '''

        urls = GoogleBlogSearch.get_blog_links('hallo welt', maxResults=10)
        assert len(urls) == 10

    def test_paging(self):
        ''' tests if paging working '''
        urls = GoogleBlogSearch.get_blog_links('hallo welt', maxResults=101)
        assert len(urls) == 101
        urls = GoogleBlogSearch.get_blog_links('hallo welt', maxResults=102)
        assert len(urls) == 102
        urls = GoogleBlogSearch.get_blog_links('hallo welt', maxResults=137)
        assert len(urls) == 137
        urls = GoogleBlogSearch.get_blog_links('hallo welt', maxResults=200)
        assert len(urls) == 200

if __name__ == '__main__':

    unittest.main()
