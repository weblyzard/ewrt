#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on September 20, 2018

@author: jakob <jakob.steixner@modul.ac.at>
'''

import pytest
from eWRT.ws.wikidata.enrich_from_wikipedia import (
    wikipedia_page_info_from_title,
    get_sitelinks_from_wd_id)
from wikipedia.exceptions import PageError
from wikipedia import DisambiguationError

douglas_adams_result_expected = {
    u'title': u'Douglas Adams',
    u'url': u'valid_url_dummy',
    u'language': u'en',
    u'summary': u'author',
    u'revision_id': 1,
    u'revision_timestamp': u'+0000-00-00T00:00:00Z'
}

austria_expected = {
    u'url': u'https://de.wikipedia.org/wiki/%C3%96sterreich',
    u'title': u'Österreich',
    u'language': u'de',
    u'summary': u'Republik',
    u'revision_id': 1,
    u'revision_timestamp': u'+0000-00-00T00:00:00Z'
}


class TestWikipedia_page_info_from_title():

    @pytest.mark.parametrize(u'title,language,expected',
                             [('Douglas Adams', 'en',
                               douglas_adams_result_expected),
                              ('Österreich', 'de', austria_expected)])
    def test_wikipedia_page_info_from_title(self, title, language, expected):
        try:
            page_info = wikipedia_page_info_from_title(title, language)
            print('Retrieved meta info!')
        except (PageError, DisambiguationError):
            raise ValueError(u'No English Wikipedia page identified for '
                             u'{}'.format(title))
        try:
            assert page_info['title'] == expected['title']
            print('Titles identical.')
        except AssertionError:
            raise AssertionError(u'Title returned differs')
        try:
            assert expected['summary'] in page_info[u'summary']
            print(u'Obligatory keywords contained in summary')
        except AssertionError:
            raise AssertionError(u'Summary does not match expected keywords')
        with pytest.raises(DisambiguationError):
            page_info = wikipedia_page_info_from_title('Georgia', 'en')

    def test_get_sitelinks_from_wdid(self):
        try:
            assert get_sitelinks_from_wd_id('Q42', ['en', 'ru', 'sr']) == \
                   {'ruwiki': u'Адамс, Дуглас', 'enwiki': u'Douglas Adams',
                    'srwiki': u'Даглас Адамс'}
            print('Expected site titles retrieved.')
        except AssertionError:
            raise AssertionError(
                'Unexpected result for get_sitelinks_from_wdid!')

    # @pytest.mark.run(after='test_get_sitelinks_from_wdid')
    # def test_wp_summary_from_wdid(self):
    #     try:
    #         adams =  wp_summary_from_wdid()
        # except AssertionError:

    # def runTest(self):
    #     pass

# if __name__ == '__main__':
#     testcase = TestWikipedia_enrich_from_wikipedia()
#     testcase.test_wikipedia_page_info_from_title(*[u'Douglas Adams', u'en'])
