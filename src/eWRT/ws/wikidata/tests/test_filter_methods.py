#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on October 09, 2018

@author: jakob <jakob.steixner@modul.ac.at>
'''
import datetime

import pytest

from eWRT.ws.wikidata.filters import filter_result, \
    filter_language_values

input_raw_result = {
    "descriptions": {
        "de": "japanischer Sportler",
        "en": "Japanese sprinter",
        "fr": "athl\u00e8te japonais, sp\u00e9cialiste des \u00e9preuves de sprint",
        "es": "atleta japon\u00e9s"
    },
    'labels': {
        "de": "Yoshihide Kiryu",
        "en": "Yoshihide Kiry\u016b",
        "fr": "Yoshihide Kiry\u016b",
        "es": "Yoshihide Kiry\u016b"
    }
}
expected_result = [
    ('de',
     {'labels': "Yoshihide Kiryu", 'descriptions': "japanischer Sportler"}),
    ("en",
     {'labels': "Yoshihide Kiry\u016b", 'descriptions': "Japanese sprinter"}),
    ("fr", {'labels': "Yoshihide Kiry\u016b",
            'descriptions': "athl\u00e8te japonais, sp\u00e9cialiste des \u00e9preuves de sprint"})
]

@pytest.mark.parametrize('language,expected', expected_result)
def test_filter_result(language, expected):
    filtered_result = filter_result(language, input_raw_result)
    print
    assert filter_result(language, input_raw_result) == expected


unfiltered_positions_held_GW = [
    {'claim_id': u'q23$B6E5D112-C27E-4E3F-BB65-CB12B9364092',
     'labels': {'de': u'Pr\xe4sident der Vereinigten Staaten',
                'en': u'President of the United States',
                'fr': u'pr\xe9sident des \xc9tats-Unis',
                'lv': u'ASV prezidents',
                'pt': u'Presidente dos Estados Unidos'},
     'temporal_attributes': {'end date': u'+1797-03-04T00:00:00Z',
                             'start date': u'+1789-04-30T00:00:00Z'},
     'url': u'https://www.wikidata.org/wiki/Q11696'},
    {'claim_id': u'Q23$6A44E261-3592-4928-979B-0BF1CAB2D39C',
     'labels': {'de': u'Commanding General of the United States Army',
                'en': u'Commanding General of the United States Army',
                'fr': u'Commanding General of the United States Army',
                'pt': u'General Comandante do Ex\xe9rcito dos Estados Unidos'},
     'temporal_attributes': {'end date': u'+1799-12-14T00:00:00Z',
                             'start date': u'+1798-07-13T00:00:00Z'},
     'url': u'https://www.wikidata.org/wiki/Q1115127'},
    {'claim_id': u'Q23$2c113ca2-4177-4a24-eb0c-6c284ff03416',
     'labels': {'de': u'Commanding General of the United States Army',
                'en': u'Commanding General of the United States Army',
                'fr': u'Commanding General of the United States Army',
                'pt': u'General Comandante do Ex\xe9rcito dos Estados Unidos'},
     'temporal_attributes': {'end date': u'+1788-12-23T00:00:00Z',
                             'start date': u'+1775-06-15T00:00:00Z'},
     'url': u'https://www.wikidata.org/wiki/Q1115127'}]

filtered_positions_held_expected = [
    {
        "url": "https://www.wikidata.org/wiki/Q11696",
        "temporal_attributes": {
            "end date": "+1797-03-04T00:00:00Z",
            "start date": "+1789-04-30T00:00:00Z"
        },
        "labels": "President of the United States",
        "claim_id": "q23$B6E5D112-C27E-4E3F-BB65-CB12B9364092"
    },
    {
        "url": "https://www.wikidata.org/wiki/Q1115127",
        "temporal_attributes": {
            "end date": "+1799-12-14T00:00:00Z",
            "start date": "+1798-07-13T00:00:00Z"
        },
        "labels": "Commanding General of the United States Army",
        "claim_id": "Q23$6A44E261-3592-4928-979B-0BF1CAB2D39C"
    },
    {
        "url": "https://www.wikidata.org/wiki/Q1115127",
        "temporal_attributes": {
            "end date": "+1788-12-23T00:00:00Z",
            "start date": "+1775-06-15T00:00:00Z"
        },
        "labels": "Commanding General of the United States Army",
        "claim_id": "Q23$2c113ca2-4177-4a24-eb0c-6c284ff03416"
    }
]


def test_filter_language_values():
    result = filter_language_values(language='en',
                                    value_list=unfiltered_positions_held_GW)
    assert result == filtered_positions_held_expected