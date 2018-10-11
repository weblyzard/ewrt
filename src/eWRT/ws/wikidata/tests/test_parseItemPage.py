#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on September 24, 2018

@author: jakob <jakob.steixner@modul.ac.at>
'''

import copy
from collections import OrderedDict

import mock
import pytest
from eWRT.ws.wikidata.sample_itempage import itempage
from eWRT.ws.wikidata.wikibot_parse_item import ParseItemPage
from eWRT.ws.wikidata.preferred_claim_value import attribute_preferred_value


entity_mock = mock.Mock()
entity_mock.text = itempage
entity_mock.claims = itempage['claims']

expected_labels = [('labels', 'en', {'labels': {'en': 'Douglas Adams'}}),
                   ('labels', 'ru', {'labels': {
                       'ru': u'\u0414\u0443\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441'}}),
                   ('labels', 'lv', {'labels': {'lv': u'Duglass Adamss'}}),
                   ('descriptions', u'nb', {'descriptions': {
                       'nb': u'engelsk science fiction-forfatter og humorist'}})]


@pytest.mark.parametrize(u'literal_type,language,expected',
                         expected_labels)
def test_extract_literal_properties(literal_type, language, expected):
    """test the extraction of literals (labels, descriptions)
    parametrized for language and type and literal returns the expected
    and only the expected result."""
    result = ParseItemPage.extract_literal_properties(entity=entity_mock,
                                                      languages=[language],
                                                      literals=[literal_type]
                                                      )
    assert result == expected


expected_names_result = {'url': 'https://www.wikidata.org/wiki/Property:P735',
                         'values': [
                             {'url': u'https://www.wikidata.org/wiki/Q463035',
                              'labels': {'en': u'Douglas'},
                              'claim_id': u'Q42$1d7d0ea9-412f-8b5b-ba8d-405ab9ecf026'},
                             {'url': u'https://www.wikidata.org/wiki/Q19688263',
                              'labels': {'en': u'No\xebl'},
                              'claim_id': u'Q42$1e106952-4b58-6067-c831-8593ce3d70f5'}],
                         'preferred': [
                             {'url': u'https://www.wikidata.org/wiki/Q463035',
                              'labels': {'en': u'Douglas'},
                              'claim_id': u'Q42$1d7d0ea9-412f-8b5b-ba8d-405ab9ecf026'}]}


def test_complete_claim_details():
    """With the given name parameter ('P735') as an example, test
    that the result is the expected result, including a list of values (first
    and second name), one marked as preferred (the first name)."""
    entity = entity_mock
    names = entity.text['claims']['P735']
    names_result = ParseItemPage.complete_claim_details(
        'P735',
        names,
        ['en'],
        ['labels']
    )
    assert names_result == expected_names_result


def test_attribute_preffered_value():
    """test_complete_claim_details already implicitly tests that a preferred
    value is marked when present. This test focusses on the correct behaviour
    when this is not the case: A result without a 'preferred'-key for
    complete_claim_details, an error when 'attribute_preferred_value is called
    directly.
    """
    names = entity_mock.claims['P735']
    names_new = [copy.copy(name) for name in names]

    for name in names_new:
        name.rank = 'normal'
    names_without_preferred = ParseItemPage.complete_claim_details(
        'P735',
        names_new,
        ['en'],
        ['labels']
    )
    assert 'preferred' not in names_without_preferred

    try:
        attribute_preferred_value(names_new)
        raise AssertionError(
            'This should raise a ValueError: No item marked preferred!')
    except ValueError:
        pass


def test_get_country_from_location():
    # we expect a ValueError when the only local attribute tried is
    # P17 = country - Douglas Adams doesn't have a country attribute
    try:
        country_found = ParseItemPage.get_country_from_any(
            entity_mock,
            local_attributes=['P17'],
            languages=['en'])
        raise ValueError('Country should not be identified, entity contains no '
                         'attribute P17!')
    except ValueError:
        pass

    # still a ValueError with local attributes not applicable to persons
    local_attributes = OrderedDict([
        ("P17", u"country"),
        ("P131", u"located in the administrative territorial entity"),
        ("P159", u"headquarters location"),
        ("P740", u"location of formation"),
    ])
    try:
        country_found = ParseItemPage.get_country_from_any(
            entity_mock,
            local_attributes=local_attributes,
            languages=['en'])
        raise ValueError('Country should not be identified, wrong type of '
                         'location attributes for person entity Douglas Adams!')
    except ValueError:
        pass

    # with birth place ranked higher than residence, we expect
    # UK
    local_attributes = OrderedDict([
        ("P17", u"country"),
        ("P131", u"located in the administrative territorial entity"),
        ("P19", u"place of birth"),
        ("P551", u"residence"),
        ("P27", u"country of citizenship"),
        ("P159", u"headquarters location"),
        ("P740", u"location of formation"),
    ])
    country_found = ParseItemPage.get_country_from_any(
        entity_mock,
        local_attributes=local_attributes,
        languages=['en'])
    assert len(country_found) == 1
    assert country_found[0]['url'] == u'https://www.wikidata.org/wiki/Q145'
    assert country_found[0]['labels'] == {'en': 'United Kingdom'}

    # with the attributes reordered, i. e. residence before place of birth,
    # this should return the United States (last residence: Santa Barbara
    local_attributes = OrderedDict([
        ("P17", u"country"),
        ("P131", u"located in the administrative territorial entity"),
        ("P551", u"residence"),
        ("P19", u"place of birth"),
        ("P27", u"country of citizenship"),
        ("P159", u"headquarters location"),
        ("P740", u"location of formation"), ])

    country_found = ParseItemPage.get_country_from_any(
        entity_mock,
        local_attributes=local_attributes,
        languages=['en'])
    assert len(country_found) == 1
    assert country_found == \
           [{'url': u'https://www.wikidata.org/wiki/Q30',
             'labels': {'en': u'United States of America'},
             'claim_id': u'q159288$0D0A08B9-BC36-4B45-B1CF-5547215DEFCB'
             # this claim is actually about Santa Barbara being in the US, not about Adams per se
             }
            ]

