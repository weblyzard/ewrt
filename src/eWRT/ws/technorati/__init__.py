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

import re, logging, sys
from eWRT.access.http import Retrieve
from eWRT.ws.TagInfoService import TagInfoService
import time
from lxml import etree
from datetime import timedelta, date

SLEEP_TIME = 5
NON_ABSTRACT_TEXT = ['a', 'h3']
RESULTS_PER_PAGE = 10

cleanText = lambda text: trim(re.sub('\n', ' ', text))

logger = logging.getLogger('Technorati')
handler = logging.StreamHandler()
logger.addHandler(handler)

class Technorati(TagInfoService):
    """ retrieves data using the del.icio.us API """

    RE_TAG_COUNT = re.compile('Posts relating to &ldquo;.*?&rdquo; \((\S+)\)',
        re.IGNORECASE | re.DOTALL)
    RE_TAG_CONTAINER = re.compile('<div id="related-tags".*?<ul>(.*?)</ul>.*?</div>',
        re.IGNORECASE | re.DOTALL)
    RE_RELATED_TAG = re.compile('<a.*?">(.*?)</a>',
        re.IGNORECASE | re.DOTALL)

    AVAILABLE_TOPICS = ['overall', 'entertainment', 'business', 'sports', 'politics', 'autos', 'technology', 'living', 'green', 'science']
    AVAILABLE_AUTHORITY = ['all', 'high', 'medium', 'low']
    AVAILABLE_SOURCE = ['advanced-source-blogs', 'advanced-source-news', 'advanced-source-all']
    AVAILABLE_RETURN = ['posts', 'news']

    TOPIC = 'overall'
    AUTHORITY = 'high'
    SOURCE = 'advanced-source-all'
    RETURN = 'posts'

    TECHNORATI_URL = 'http://technorati.com/search?usingAdvanced=1&q=%s&return=%s&source=%s&topic=%s&authority=%s'

    __slots__ = ()
    last_access = 0


    @staticmethod
    def getTagInfo(tags):
        """ @param   tags   A list of tags to retrieve information for
            @returns        the number of bookmarks using the given tags
        """
        url = Technorati._parseURL(tags)
        content = Technorati.get_content(url)

        return Technorati._parse_tag_counts(content)


    @staticmethod
    def getRelatedTags(tags, withCounts=True):
        """ @param tags - list of tags
            @param booelan withCounts to print counts for tags
            @return list of related tags 
        """

        # not supported at the moment

        return []

        url = Technorati._parseURL(tags)

        content = Technorati.get_content(url)
        tag_container = Technorati.RE_TAG_CONTAINER.findall(content)
        related_tags_with_count = []

        if len(tag_container) > 0:

            related_tags = Technorati.RE_RELATED_TAG.findall(tag_container[0])
            if withCounts:
                for tag in related_tags:
                    tag = re.sub(' ', '-', tag)
                    related_tags_with_count.append((tag, Technorati._getRelatedTagCount(tags, tag)))

                return related_tags_with_count

            else:
                return related_tags



    # 
    # helper functions
    #
    @staticmethod
    def _parse_tag_counts(content):
        """ parses technorati html content and returns the number of counts for the tags 
            @param content: HTML content of technorati
            @return: count of related posts
        """

        m = Technorati.RE_TAG_COUNT.search(content)
        if m:
            return re.sub(',', '', m.group(1))
        else:
            return 0

    @staticmethod
    def _getRelatedTagCount(tags, filter):
        """ returns the related tag count
            @param tags - list of tags
            @param filtered tag
            @return count of related tag """

        url = Technorati._parseURL(tags, filter)
        content = Technorati.get_content(url)
        return Technorati._parse_tag_counts(content)

    @staticmethod
    def _parseURL(tags, filter=''):
        """ parses the URL """

        if type(tags).__name__ == 'str':
            url = Technorati.TECHNORATI_URL % (tags, Technorati.RETURN, Technorati.SOURCE, Technorati.TOPIC, Technorati.AUTHORITY)
        else:
            url = Technorati.TECHNORATI_URL % ("+".join(tags), Technorati.RETURN, Technorati.SOURCE, Technorati.TOPIC, Technorati.AUTHORITY)

        if filter == '':
            return url
        else:
            return '%s&filter=%s' % (url, filter)


    @staticmethod
    def get_content(url):
        """ returns the content from Technorati """
        assert(url.startswith("http"))

        logger.debug('Fetching content for URL %s' % url)

        if (time.time() - Technorati.last_access) < SLEEP_TIME:
            logger.debug('Sleeping %s seconds!' % SLEEP_TIME)
            time.sleep(SLEEP_TIME)

        Technorati.last_access = time.time()

        f = Retrieve("%s_new" % Technorati.__name__).open(url)
        content = f.read()
        f.close()
        return content

    @staticmethod
    def get_blog_links (searchTerm, maxResults=100, offset=0, maxAge=0, 
                        country=None):
        '''
        Searches Technorati for the given term and returns a list of links 
        to the blogs
        @param searchTerm: term to search
        @param maxResults: max search results 
        @param offset:
        @param maxAge: maximum age of the articles in days,
            if set links are ordered by relevance and not by date
        @param country: currently not supported
        @return: dictionary with all the relevant info
        '''

        if isinstance(searchTerm, list):
            searchTerm = '+'.join(searchTerm)

        searchTerm = re.sub(' ', '+', searchTerm)
        if offset >= RESULTS_PER_PAGE:
            page = (offset / RESULTS_PER_PAGE) + 1
        else:
            page = 1

        if maxAge == 0: orderBy = 'relevance'
        else: orderBy = 'date'

        url = '%s&page=%s&sort=%s' % (Technorati._parseURL(searchTerm), 
                                      page, orderBy)
        content = Technorati.get_content(url)
        print '.'
        return Technorati._parseLinksFromContent(content, searchTerm, 
                                                 maxResults=maxResults, 
                                                 offset=offset, maxAge=maxAge)


    @staticmethod
    def _parseLinksFromContent(content, searchTerm, maxResults=100, 
                               offset=0, maxAge=0):
        ''' parses the links from the content '''
        tree = etree.HTML(content)
        links = []
        resultList = tree.xpath('//ol[@class="search-results post-list"]')

        logger.debug('Parsing links from Technorati result: %s, %s, %s, %s ' % (searchTerm, maxResults, offset, maxAge))

        if len(resultList) > 0:
            counter = 0
            for element in resultList[0].iterchildren():
                blogLink = {}
                linkDate = Technorati._getDate(element, maxAge)
                if not linkDate == None:

                    try:
                        blogLink['url'] = element.xpath('.//a[@class="offsite"]')[0].attrib['href']
                        logger.info('Found url %s' % blogLink['url'])
                    except IndexError:
                        logger.error('Could not parse the URL')

                    try:
                        blogLink['authority'] = int(re.sub('Authority ', '', element.xpath('.//a[@class="authority"]')[0].text))
                    except:
                        logger.error('Could not parse the authority!')
                        blogLink['authority'] = ''

                    blogLink['source'] = 'Technorati - Keyword "%s"' % searchTerm
                    blogLink['abstract'] = Technorati._getAbstract(element)
                    blogLink['reach'] = '0'
                    blogLink['date'] = linkDate

                    if blogLink.has_key('url'):
                        logger.debug('Found URL %s' % blogLink['url'])
                        links.append(blogLink)
                        offset += 1
                        counter += 1
                        if offset == maxResults:
                            break
                    else:
                        offset += 1

            if offset < maxResults and counter == RESULTS_PER_PAGE:
                links.extend(Technorati.get_blog_links(searchTerm, maxResults, 
                                                       offset, maxAge))

        else:
            if offset == 0:
                logger.warning('At the first page - should find a result for %s -> Changes in the site structure' % searchTerm)

        return links

    @staticmethod
    def _getAbstract(element):
        ''' gets the abstract from the element '''
        text = []

        if not element.tag in NON_ABSTRACT_TEXT and not element.text == None:
            text.append(element.text.lstrip())

        for child in element.getchildren():
            text.extend(Technorati._getAbstract(child))

        if not element.tag in NON_ABSTRACT_TEXT and not element.tail == None:
            text.append(element.tail.lstrip())

        return ''.join(text)

    @staticmethod
    def _getDate(element, maxAge=0):
        ''' returns the date of the link '''

        p = re.compile('(\d+)\s(\w+)\sago')

        minDate = (date.fromtimestamp(time.time()) - timedelta(days=maxAge))
        linkDate = None
        for div in element.xpath('.//div'):
            m = p.search(div.text)
            if m:
                age = int(m.groups()[0])
                timeDim = m.groups()[1]

                if re.search('week.?', timeDim):
                    hours = age * 7 * 24
                elif re.search('day.?', timeDim):
                    hours = age * 24
                elif re.search('hour.?', timeDim):
                    hours = age
                elif re.search('minute.?', timeDim):
                    hours = 1
                else:
                    hours = 0

                if hours > 0:
                    linkDate = date.fromtimestamp(time.time()) - timedelta(hours=hours)

                    if linkDate < minDate and maxAge > 0:
                        linkDate = None
            else:
                logger.warning("Could not find a date")

        return linkDate


if __name__ == '__main__':

    print Technorati.getRelatedTags(("Linux",))
