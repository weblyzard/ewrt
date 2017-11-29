#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import logging

from eWRT.ws.google import GoogleBlogSearch


logger = logging.getLogger('logger')

class TestGoogleSearch(unittest.TestCase):
    ''' '''

    def setUp(self):
        ''' set up'''
        self.search = GoogleBlogSearch()
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)

    def no_test_get_url(self):
        ''' tests getting the urls '''

        urls = GoogleBlogSearch.get_blog_links('hallo welt', maxResults=10)
        assert len(urls) == 10
        for url in urls:
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
            print(url)
            assert url['url'].startswith('http')

    def test_parsing_url(self):
        url = '/url?q=http://wiweb.at/index.php%3Foption%3Dcom_content%26view%3Darticle%26id%3D650:eu-budget-kommissar%26catid%3D36:welt&sa=U&ei=BfYoT4_DGuSD4gTEsv3rAw&ved=0CD0QmAEwBw&usg=AFQjCNEToCVos-YrGnS4Jnuuv0L-x_hnXA'

        url = GoogleBlogSearch.parse_url(url)
        print(url)
        assert url == 'http://wiweb.at/index.php?option=com_content&view=article&id=650:eu-budget-kommissar&catid=36:welt'

if __name__ == '__main__':

    unittest.main()
