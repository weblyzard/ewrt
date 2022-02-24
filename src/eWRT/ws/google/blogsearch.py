from datetime import datetime, timedelta, date
import logging
import re
from urllib.parse import urlparse, parse_qs

from eWRT.access.http import Retrieve
from lxml import etree

SEARCH_URL = 'http://www.google.com/search?hl=en&ie=UTF-8&q={searchTerm}&num={number}&safe=active&start={start}'
#
XPATHS = {'blog_url': './h3[@class="r"]/a',
          'blog_date': './div[@class="s"]/span[@class="f"]',
          'search_result': './/div[@id="ires"]/ol',
          'blog_abstract': './div[@class="s"]/text()'}

# Google displays a maximum 100 results per page
MAX_RESULTS_PAGE = 100
SLEEP_TIME = 10
SUPPORTED_COUNTRIES = ('AT', 'DE')

logger = logging.getLogger('logger')


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
            if country.upper() in SUPPORTED_COUNTRIES:
                url = '%s&cr=country%s' % (url, country.upper())
                url = url.replace('.com/', '.%s/' % country.lower())
            else:
                logger.error('Do not recognize country "%s"' % country)

        logger.debug('Searching URL %s' % url)
        html_content = GoogleBlogSearch.get_content(url)
        # print html_content
        tree = etree.HTML(html_content)
        resultList = tree.xpath('.//div[@id="ires"]/ol')

        counter = 0
        firstElement = True
        urls = []

        for element in resultList[0].iterchildren():
            if firstElement:
                firstElement = False
            else:
                itemList = element.xpath('./h3[@class="r"]/a')
                if len(itemList) == 1:
                    url = itemList[0].attrib['href']
                    abstract = ' '.join(element.xpath(
                        './div[@class="s"]/text()'))
                    url = GoogleBlogSearch.parse_url(url)
                    if url is None:
                        continue
                    if url:
                        blogLink = {}
                        blogLink['url'] = url
                        blogLink['source'] = 'GoogleBlogSearch - Keyword "%s"' % searchTerm
                        blogLink['abstract'] = abstract
                        blogLink['reach'] = '0'

                        try:
                            blogLink['date'] = GoogleBlogSearch.get_link_date(
                                element)
                        except IndexError as e:
                            pass

                        urls.append(blogLink)

                        counter += 1

                    if (counter + offset) >= maxResults:
                        break

        if maxResults > (MAX_RESULTS_PAGE) and (counter + offset) < maxResults:

            urls.extend(GoogleBlogSearch.get_blog_links(searchTerm,
                                                        maxResults=maxResults, offset=(
                                                            counter + offset),
                                                        maxAge=maxAge))
        return urls

    @staticmethod
    def parse_url(url):

        if url.startswith('/'):
            if '?q=' in url:
                sub_url = url.split('?q=')[1]
                if not sub_url.startswith('http'):
                    return None
            url = 'https://www.google.com%s' % url

        o = urlparse(url)
        query = parse_qs(o.query)

        correct_url = None

        if not 'q' in query:
            logger.critical('URL %s does not contain the parameter "q"' % url)
        else:
            if isinstance(query['q'], list):
                correct_url = query['q'][0]
            elif isinstance(query['q'], list):
                correct_url = query['q'][0]
            else:
                logger.critical(
                    'Unknown type "%s" for query["q"]' % type(query['q']))

        return correct_url

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