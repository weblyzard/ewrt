#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on September 22, 2018

@author: jakob <jakob.steixner@modul.ac.at>
'''
from pprint import pprint

import mock
from pywikibot import ItemPage
from eWRT.ws.wikidata.extract_meta import (collect_attributes_from_wp_and_wd,
                                           )
from eWRT.ws.wikidata.sample_itempage import itempage as adams_itempage


adams = mock.Mock()

adams.get.return_value = adams.text = adams_itempage
adams.claims = adams_itempage[u'claims']
adams.id = 'Q42'
adams.timestamp = '+2018-09-25T00:00:00Z'

WD_PARAMETERS = [
    'P18',  # image
    'P19',  # place of birth
    'P39',  # position held
    'P569',  # date of birth
    'P570',  # date of death
    'P1411'  # nominated for
]


def test_collect_attributes_from_wp_and_wd_offline():
    """Test the version of the data collection loop that does
    without a new call to the API for every attribute to retrieve
    human readable values."""
    adams_data = collect_attributes_from_wp_and_wd(adams, ['en'],
                                                   wd_parameters=WD_PARAMETERS,
                                                   include_literals=False,
                                                   raise_on_no_wikipage=False,
                                                   include_attribute_labels=False,
                                                   require_country=False).next()
    assert adams_data['date of death']['values'][0]['value'].startswith(
        '+2001-05-11')
    for claim in adams_data.values():
        if isinstance(claim, dict):
            if 'values' in claim:
                # no labels expected to be stored with attribute values
                assert not any(
                    ['labels' in instance for instance in claim['values']])


def test_collect_attributes_from_wp_and_wd_online():
    """"""
    adams_data = collect_attributes_from_wp_and_wd(adams, ['en'],
                                                   wd_parameters=WD_PARAMETERS,
                                                   include_literals=False,
                                                   raise_on_no_wikipage=False,
                                                   include_attribute_labels=True,
                                                   include_wikipedia=True,
                                                   delay_wikipedia_retrieval=False,
                                                   require_country=False).next()
    assert adams_data['date of death']['values'][0]['value'].startswith(
        '+2001-05-11')
    for claim in adams_data.values():
        if isinstance(claim, dict):
            if 'values' in claim:
                # two types of attributes in
                try:
                    assert all(
                        ['labels' in instance for instance in claim['values']])
                except AssertionError:
                    assert all(
                        ['value' in instance for instance in claim['values']])
    assert 'enwiki' in adams_data
    assert isinstance(adams_data['enwiki'], dict)
    assert 'summary' in adams_data['enwiki']

def test_collect_attributes_from_wp_and_wd_delay_wikipedia():
    """
    Check that the 'delay_wikipedia_retrieval' switch does what it should:
    return a string for the e. g. 'enwiki' key (the title of the page), instead
    of the dict with retrieved data.
    :return:
    """
    adams_data = collect_attributes_from_wp_and_wd(adams, ['en'],
                                                   wd_parameters=WD_PARAMETERS,
                                                   include_literals=False,
                                                   raise_on_no_wikipage=False,
                                                   include_attribute_labels=True,
                                                   require_country=False,
                                                   include_wikipedia=True,
                                                   delay_wikipedia_retrieval=True).next()
    assert 'enwiki' in adams_data
    assert isinstance(adams_data['enwiki'], basestring)

print(test_collect_attributes_from_wp_and_wd_online())