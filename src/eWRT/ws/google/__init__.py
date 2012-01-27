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

import re
import unittest
import optparse
import sys
import logging
import StringIO
import time
from datetime import datetime, timedelta, date

from xml.dom.minidom import parse, parseString
from lxml import etree

from eWRT.access.http import Retrieve

SEARCH_URL = 'http://www.google.com/search?hl=en&ie=UTF-8&lr=&tbm=blg{maxAge}&q={searchTerm}&num={number}&safe=active&start={start}'

XPATHS = {'blog_url': './h3[@class="r"]/a',
          'blog_date': './div[@class="s"]/span[@class="f"]',
          'search_result': './/div[@id="ires"]/ol',
          'blog_abstract': './div[@class="s"]/text()'}

# Google displays a maximum 100 results per page
MAX_RESULTS_PAGE = 100
SLEEP_TIME = 10
SUPPORTED_COUNTRIES = ('AT', 'DE')

logger = logging.getLogger('eWRT')

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
    def get_blog_links(searchTerm, maxResults=100, offset=0, maxAge=0,
                       country=None):
        ''' returns a list of URLs 
        @param searchTerm:
        @param maxResult:
        @param offset:
        @param maxAge:
        @param country: country code, e.g. AT, DE, ... 
        @return:     
        '''

        if isinstance(searchTerm, list):
            searchTerm = '+'.join(searchTerm)

        searchTerm = re.sub(' ', '+', searchTerm)

        if maxAge > 0:
            dateFormat = '%m/%d/%Y'
            max = date.today().strftime(dateFormat)
            min = (date.today() - timedelta(days=maxAge)).strftime(dateFormat)
            maxAgeString = '&tbs=cdr:1,cd_min:{min},cd_max:{max}'.format(
                                                min=min, max=max)
        else:
            maxAgeString = ''

        url = SEARCH_URL.format(searchTerm=searchTerm, start=offset,
                                number=maxResults, maxAge=maxAgeString)
        
        if country: 
            if country in SUPPORTED_COUNTRIES:
                url = '%s&cr=country%s' % (url, country.upper())
                url = url.replace('.com/', '.%s/' % country.lower())
            else: 
                logger.error('Do not recognize country "%s"' % country)
                
        logger.debug('Searching URL %s' % url)
        html_content = GoogleBlogSearch.get_content(url)
        print html_content
        tree = etree.HTML(html_content)
        resultList = tree.xpath('.//div[@id="ires"]/ol')

        counter = 0
        firstElement = True
        urls = []

        for element in resultList[0].iterchildren():
            if firstElement:
                firstElement = False
            else:
                url = element.xpath('./h3[@class="r"]/a')[0].attrib['href']
                abstract = ' '.join(element.xpath('./div[@class="s"]/text()'))
                if not url.startswith('http'):
                    url = url.replace('/url?q=', '')
                    url = re.sub('/\&sa=U\&ei=.*', '', url)
                if not url.startswith('http'):
                    logger.critical('Url does not start with http: %s' % url)
                blogLink = {}
                blogLink['url'] = url
                blogLink['source'] = 'GoogleBlogSearch - Keyword "%s"' % searchTerm
                blogLink['abstract'] = abstract
                blogLink['reach'] = '0'
                blogLink['date'] = GoogleBlogSearch.get_link_date(element)

                urls.append(blogLink)

                counter += 1

                if (counter + offset) >= maxResults:
                    break

        if maxResults > (MAX_RESULTS_PAGE) and (counter + offset) < maxResults:

            urls.extend(GoogleBlogSearch.get_blog_links(searchTerm,
                        maxResults=maxResults, offset=(counter + offset) ,
                        maxAge=maxAge))
        return urls

    @staticmethod
    def get_link_date(element):
        linkDate = element.xpath('./div[@class="f"]/text()')[0]
        linkDate = linkDate.split('by')[0]
        
        m = re.match('(\d{1,2} \w* \d{2,4})', linkDate)

        if m:
            linkDate = datetime.strptime(m.groups()[0], '%d %b %Y')
        else:
            now = datetime.today()
            if 'ago' in linkDate:

                tdelta = None
                if 'day' in linkDate:
                    days = int(re.split(' ', linkDate)[0])
                    tdelta = timedelta(days=days)
                elif 'hour' in linkDate:
                    hours = int(re.split(' ', linkDate)[0])
                    tdelta = timedelta(hours=hours)
                elif 'minute' in linkDate:
                    minutes = int(re.split(' ', linkDate)[0])
                    tdelta = timedelta(minutes=minutes)
                    
                linkDate = now - tdelta
            
        return linkDate
    
class TestGoogleSearch(unittest.TestCase):
    ''' '''

    def setUp(self):
        ''' set up'''
        self.search = GoogleBlogSearch()
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        
    def test_get_url(self):
        ''' tests getting the urls '''

        urls = GoogleBlogSearch.get_blog_links('hallo welt', maxResults=10)
        assert len(urls) == 10
        for url in urls:
            print url
            assert url['url'].startswith('http')

    def no_test_paging(self):
        ''' tests if paging working '''
        urls = GoogleBlogSearch.get_blog_links('hallo welt', maxResults=101)
        assert len(urls) == 101
        urls = GoogleBlogSearch.get_blog_links('hallo welt', maxResults=102)
        assert len(urls) == 102
        urls = GoogleBlogSearch.get_blog_links('hallo welt', maxResults=137)
        assert len(urls) == 137
        urls = GoogleBlogSearch.get_blog_links('hallo welt', maxResults=200)
        assert len(urls) == 200

    def test_country(self):
        urls = GoogleBlogSearch.get_blog_links('finanzkrise', maxResults=10, country='AT')
        for url in urls:
            print url

if __name__ == '__main__':

    unittest.main()
