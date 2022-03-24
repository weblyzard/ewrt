#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on September 22, 2018

@author: jakob <jakob.steixner@modul.ac.at>
'''
from builtins import next
from past.builtins import basestring

import unittest

import mock
import pytest


from eWRT.ws.wikidata.extract_meta import collect_attributes_from_wp_and_wd

try:
    from eWRT.ws.wikidata.sample_itempage import itempage as adams_itempage
    API_ERROR=False
except:
    API_ERROR = True


@pytest.mark.skipif(API_ERROR is True, reason='External API not available')
class TestCollectAttributesFromWpAndWd(unittest.TestCase):
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
    def test_collect_attributes_from_wp_and_wd_offline(self):
        """Test the version of the data collection loop that does
        without a new call to the API for every attribute to retrieve
        human readable values."""
        adams_data = next(collect_attributes_from_wp_and_wd(self.adams, ['en'],
                                                       wd_parameters={
                                                           'person': self.WD_PARAMETERS},
                                                       include_literals=False,
                                                       raise_on_no_wikipage=False,
                                                       include_attribute_labels=False,
                                                       resolve_country=False,
                                                       entity_type='person'))
        assert adams_data['date of death']['values'][0]['value'].startswith(
            '+2001-05-11')
        for claim in list(adams_data.values()):
            if isinstance(claim, dict):
                if 'values' in claim:
                    # no labels expected to be stored with attribute values
                    assert not any(
                        ['labels' in instance for instance in claim['values']])


    def test_collect_attributes_from_wp_and_wd_online(self):
        """"""
        adams_data = next(collect_attributes_from_wp_and_wd(self.adams, ['en'],
                                                       wd_parameters={
                                                           'person': self.WD_PARAMETERS},
                                                       include_literals=False,
                                                       raise_on_no_wikipage=False,
                                                       include_attribute_labels=True,
                                                       include_wikipedia=True,
                                                       delay_wikipedia_retrieval=False,
                                                       resolve_country=False,
                                                       entity_type='person'))
        assert adams_data['date of death']['values'][0]['value'].startswith(
            '+2001-05-11')
        for claim in list(adams_data.values()):
            if isinstance(claim, dict):
                if 'values' in claim and claim['url'] != 'P18':
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


    def test_collect_attributes_from_wp_and_wd_delay_wikipedia(self):
        """
        Check that the 'delay_wikipedia_retrieval' switch does what it should:
        return a string for the e. g. 'enwiki' key (the title of the page), instead
        of the dict with retrieved data.
        :return:
        """
        adams_data = next(collect_attributes_from_wp_and_wd(self.adams, ['en'],
                                                       wd_parameters={
                                                           'person': self.WD_PARAMETERS},
                                                       entity_type='person',
                                                       include_literals=False,
                                                       raise_on_no_wikipage=False,
                                                       include_attribute_labels=True,
                                                       resolve_country=False,
                                                       include_wikipedia=True,
                                                       delay_wikipedia_retrieval=True))
        assert 'enwiki' in adams_data
        assert isinstance(adams_data['enwiki'], basestring)
