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
            page_info = wikipedia_page_info_from_title(title, language).next()
            print('Retrieved meta info!')
        except StopIteration:
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
        with pytest.raises(StopIteration):
            wikipedia_page_info_from_title('Georgia', 'en').next()


    def test_get_sitelinks_from_wdid(self):
        try:
            assert get_sitelinks_from_wd_id('Q42', ['en', 'ru', 'sr']) == \
                   {'ruwiki': u'Адамс, Дуглас', 'enwiki': u'Douglas Adams',
                    'srwiki': u'Даглас Адамс'}
            print('Expected site titles retrieved.')
        except AssertionError:
            raise AssertionError(
                'Unexpected result for get_sitelinks_from_wdid!')

    def test_get_multiple_results(self):
        """Multiple titles are not significantly slower a single title.
        This checks whether they're properly filtered - we don't want
        any redirects or disambiguation pages since we're working with exact titles"""
        titles = u'Wiener Neustadt', u'Douglas Adams', u'Wien 19', u'Ferdinand Raimund', u'Österreich', u'Frankreich', u'Deutschland', u'Mesopotamien', u'Neuschwanstein',

        results = list(wikipedia_page_info_from_title('|'.join(titles),
                'de'))
        expected_failures = (
            'Wien 19', # is a redirect, we only accept strict matches
            u'Döbling', # the result of the redirection
            'Neuschwanstein' # a disambiguation page
        )
        titles_retrieved = [r['title'] for r in results]
        print(titles_retrieved)
        assert not any([t in expected_failures for t in titles_retrieved])
        # for t in titles:
        #     if t not in expected_failures:
        #         assert t in titles_retrieved
        assert all([t in titles_retrieved for t in titles if t not in expected_failures])
        assert len(results) == 7

TestWikipedia_page_info_from_title().test_get_multiple_results()




# '''
# {u'lastrevid': 862105845, u'pagelanguagedir': u'ltr', u'pageid': 26964606,
#  u'canonicalurl': u'https://en.wikipedia.org/wiki/Austria',
#  u'title': u'Austria',
#  u'editurl': u'https://en.wikipedia.org/w/index.php?title=Austria&action=edit',
#  u'pagelanguagehtmlcode': u'en', u'length': 134765,
#  u'contentmodel': u'wikitext',
#  u'pagelanguage': u'en',
#  u'touched': u'2018-10-02T06:20:36Z',
#  u'ns': 0,
#  u'extract': u"Austria ( ( listen), ; German: \xd6sterreich [\u02c8\xf8\u02d0st\u0250ra\u026a\xe7] ( listen)), officially the Republic of Austria (German: Republik \xd6sterreich,  listen ), is a  landlocked country of over 8.8 million people  in Central Europe. It is bordered by the Czech Republic and Germany to the north, Hungary and Slovakia to the east, Slovenia and Italy to the south, and Switzerland and Liechtenstein to the west. The territory of Austria covers 83,879 km2 (32,386 sq mi). The terrain is highly mountainous, lying within the Alps; only 32% of the country is below 500 m (1,640 ft), and its highest point is 3,798 m (12,461 ft). The majority of the population  speaks local Bavarian dialects of German as their native language, and German in its standard form is the country's official language. Other local official languages are Hungarian, Burgenland Croatian, and Slovene.Austria is a federal republic  with a    parliamentary representative democracy comprising nine federated states. The capital and largest city, with a population exceeding 1.8 million, is Vienna. Other major urban areas of Austria include Graz, Linz, Salzburg and Innsbruck. Austria is consistently ranked as one of the richest countries in the world by per capita GDP terms. The country has developed a high standard of living and in 2018 was ranked 20th in the world for its Human Development Index. The republic declared its perpetual neutrality in foreign political affairs in 1955. Austria has been a member of the United Nations since 1955, joined the European Union in 1995, and is a founder of the OECD. Austria also signed the Schengen Agreement in 1995, and adopted the euro currency in 1999.",
#  u'fullurl': u'https://en.wikipedia.org/wiki/Austria',
#  }

# timeit.timeit('''
# print(wikipedia_page_info_from_title("Austria", "en"))
# ''', setup=setup, number=1)

# {u'batchcomplete': u'', u'query': {u'pages': {
#     u'26964606': {u'ns': 0, u'pageid': 26964606, u'revisions': [{
#         u'comment': u'/* top */ ministries change after elections, comparing to the pan-German Duden is "ambitious"',
#         u'timestamp': u'2018-10-02T06:20:36Z',
#         u'user': u'Purgy Purgatorio',
#         u'revid': 862105845,
#         u'parentid': 862097184}],
#                   u'title': u'Austria'}}},
#  u'warnings': {u'main': {u'*': u'Unrecognized parameter: ellimit.'}}}
