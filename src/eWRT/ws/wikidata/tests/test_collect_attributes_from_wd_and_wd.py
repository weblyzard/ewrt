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

#
# def is_connected():
#     import socket
#     try:
#         host = socket.gethostbyname("www.google.com")
#         socket.create_connection((host, 80), 2)
#         return True
#     except:
#         pass
#     return False


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
                                                   require_country=False)
    assert adams_data['date of death']['values'][0]['value'].startswith(
        '+2001-05-11')
    pprint(adams_data)
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
                                                   require_country=False)
    assert adams_data['date of death']['values'][0]['value'].startswith(
        '+2001-05-11')
    pprint(adams_data)
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
