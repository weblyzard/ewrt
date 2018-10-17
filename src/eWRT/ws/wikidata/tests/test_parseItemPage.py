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
from eWRT.ws.wikidata.preferred_claim_value import attribute_preferred_value
from eWRT.ws.wikidata.sample_itempage import itempage
from eWRT.ws.wikidata.wikibot_parse_item import ParseItemPage

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


douglas_adams_extract = {
    'aliases': {'de': [u'Douglas No\xebl Adams', u'Douglas Noel Adams'],
                'en': [u'Douglas No\xebl Adams',
                       u'Douglas Noel Adams',
                       u'Douglas N. Adams']},
    'descriptions': {'de': u'britischer Schriftsteller',
                     'en': u'author and humorist',
                     'sv': u'brittisk f\xf6rfattare'},
    u'employer': {'url': 'https://www.wikidata.org/wiki/Property:P108',
                  'values': [
                      {'claim_id': u'Q42$853B16C8-1AB3-489A-831E-AEAD7E94AB87',
                       'labels': {'de': u'British Broadcasting Corporation',
                                  'en': u'BBC',
                                  'sv': u'BBC'},
                       'url': u'https://www.wikidata.org/wiki/Q9531'}]},
    'full_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c0/Douglas_adams_portrait_cropped.jpg',
    u'image_description': 'https://commons.wikimedia.org/wiki/File:Douglas_adams_portrait_cropped.jpg',
    'labels': {'de': u'Douglas Adams',
               'en': u'Douglas Adams',
               'sv': u'Douglas Adams'},
    u'occupation': {'url': 'https://www.wikidata.org/wiki/Property:P106',
                    'values': [{
                        'claim_id': u'Q42$e0f736bd-4711-c43b-9277-af1e9b2fb85f',
                        'labels': {'de': u'Dramatiker',
                                   'en': u'playwright',
                                   'sv': u'dramatiker'},
                        'url': u'https://www.wikidata.org/wiki/Q214917'},
                        {
                            'claim_id': u'q42$E13E619F-63EF-4B72-99D9-7A45C7C6AD34',
                            'labels': {'de': u'Drehbuchautor',
                                       'en': u'screenwriter',
                                       'sv': u'manusf\xf6rfattare'},
                            'url': u'https://www.wikidata.org/wiki/Q28389'},
                        {
                            'claim_id': u'Q42$D6E21D67-05D6-4A0B-8458-0744FCEED13D',
                            'labels': {'de': u'Romancier',
                                       'en': u'novelist',
                                       'sv': u'romanf\xf6rfattare'},
                            'url': u'https://www.wikidata.org/wiki/Q6625963'},
                        {
                            'claim_id': u'Q42$7eb8aaef-4ddf-8b87-bd02-406f91a296bd',
                            'labels': {'de': u'Kinderbuchautor',
                                       'en': u"children's writer",
                                       'sv': u'barnboksf\xf6rfattare'},
                            'url': u'https://www.wikidata.org/wiki/Q4853732'},
                        {
                            'claim_id': u'q42$CBDC4890-D5A2-469C-AEBB-EFB682B891E7',
                            'labels': {
                                'de': u'Science-Fiction-Schriftsteller',
                                'en': u'science fiction writer',
                                'sv': u'science fiction-f\xf6rfattare'},
                            'url': u'https://www.wikidata.org/wiki/Q18844224'},
                        {
                            'claim_id': u'Q42$58F0D772-9CE4-46AC-BF0D-FBBBAFA09603',
                            'labels': {'de': u'Komiker',
                                       'en': u'comedian',
                                       'sv': u'komiker'},
                            'url': u'https://www.wikidata.org/wiki/Q245068'},
                        {
                            'claim_id': u'Q42$e469cda0-475d-8bb1-1dcd-f72c91161ebf',
                            'labels': {'de': u'Dramaturg',
                                       'en': u'dramaturge',
                                       'sv': u'dramaturg'},
                            'url': u'https://www.wikidata.org/wiki/Q487596'}]},
    u'place of birth': {'url': 'https://www.wikidata.org/wiki/Property:P19',
                        'values': [{
                            'claim_id': u'q42$3D284234-52BC-4DA3-83A3-7C39F84BA518',
                            'labels': {'de': u'Cambridge',
                                       'en': u'Cambridge',
                                       'sv': u'Cambridge'},
                            'url': u'https://www.wikidata.org/wiki/Q350'}]},
    'wikidata_id': 'Q42',
    'wikidata_timestamp': '+2018-10-04T02:20:35Z'}


def test_parseItemPage_all():
    entity = itempage
    import pprint
    parsed_without_attribute_labels = ParseItemPage(entity,
                                                    include_literals=True,
                                                    languages=['en', 'de',
                                                               'sv'],
                                                    require_country=False,
                                                    include_attribute_labels=False
                                                    ).details

    parsed_with_attribute_labels = ParseItemPage(entity, include_literals=True,
                                                 languages=['en', 'de', 'sv'],
                                                 require_country=False,
                                                 include_attribute_labels=True
                                                 ).details
    assert set(parsed_with_attribute_labels.keys()) == set(
        parsed_without_attribute_labels.keys())
    assert not any(
        ('labels' in val for val in parsed_without_attribute_labels.values()))
    # assert any(('labels' in val for val in parsed_with_attribute_labels.values()))
    assert all((parsed_with_attribute_labels[literal] ==
                parsed_without_attribute_labels[literal]
                for literal in ('labels', 'descriptions', 'aliases')))
    pprint.pprint(parsed_with_attribute_labels)

    assert parsed_with_attribute_labels == douglas_adams_extract
    for val in parsed_with_attribute_labels.values():
        if 'values' in val:
            assert all(('labels' in sub_val for sub_val in val['values']))
    parsed_with_country = ParseItemPage(entity,
                                        include_literals=False,
                                        claims_of_interest=[],
                                        languages=['en', 'de',
                                                   'sv'],
                                        require_country=True,
                                        include_attribute_labels=True,
                                        qualifiers_of_interest=[]
                                        ).details
    assert 'country' in parsed_with_country
    pprint.pprint(parsed_with_country['country'])
    pprint.pprint(parsed_with_country)
    assert parsed_with_country['country'] == {
        'url': 'https://www.wikidata.org/wiki/Property:P17',
        'values': [
            {'claim_id': u'Q42@q350$8E72D3A5-A067-47CB-AF45-C73ED7CFFF9E',
             'labels': {'de': u'Vereinigtes K\xf6nigreich',
                        'en': u'United Kingdom',
                        'sv': u'Storbritannien'},
             'url': u'https://www.wikidata.org/wiki/Q145'}]
    }


def test_parseItemPage_filter():
    """Filtering method, allows to filter entities by a) presence of a certain
    parameter or b) minimal value (str"""
    try:
        filter_params = {'P39': ('has_attr', None)}
        parsed_with_filter = ParseItemPage(itempage,
                                       include_literals=True,
                                       languages=['en', 'de',
                                                  'sv'],
                                       require_country=False,
                                       include_attribute_labels=False,
                                       filter=filter_params
                                       ).details
        raise ValueError('The sample itempage does not contain a claim "P39", '
                         'this should raise an error!')
    except ValueError:
        pass
    try:
        filter_params = {'P19': ('has_attr', None)}
        parsed_with_filter = ParseItemPage(itempage,
                                       include_literals=True,
                                       languages=['en', 'de',
                                                  'sv'],
                                       require_country=False,
                                       include_attribute_labels=False,
                                       filter=filter_params
                                       ).details
        parsed_without_filter = ParseItemPage(itempage,
                                       include_literals=True,
                                       languages=['en', 'de',
                                                  'sv'],
                                       require_country=False,
                                       include_attribute_labels=False
                                       ).details
        assert parsed_with_filter == parsed_without_filter
    except ValueError:
        raise ValueError('The sample itempage does contain a claim "P19" '
                         '(place of birth), this should pass the filter')
    try:
        filter_params = {'P569': ('min', '+1952-01-01')}
        parsed_with_filter = ParseItemPage(itempage,
                                       include_literals=True,
                                       languages=['en', 'de',
                                                  'sv'],
                                       require_country=False,
                                       include_attribute_labels=False,
                                       filter=filter_params
                                       ).details
    except ValueError:
        raise ValueError('Failed to identify Douglas Adams birth date as '
                         '>= 1952')
    try:
        filter_params = {'P569': ('min', '+1956-01-01')}
        parsed_with_filter = ParseItemPage(itempage,
                                       include_literals=True,
                                       languages=['en', 'de',
                                                  'sv'],
                                       require_country=False,
                                       include_attribute_labels=False,
                                       filter=filter_params
                                       ).details
        raise ValueError('Douglas Adams misidentified')
    except ValueError:
        pass


#
#
# {'aliases': {'de': [u'Douglas No\xebl Adams', u'Douglas Noel Adams'],
#              'en': [u'Douglas No\xebl Adams',
#                     u'Douglas Noel Adams',
#                     u'Douglas N. Adams']},
#  'descriptions': {'de': u'britischer Schriftsteller',
#                   'en': u'author and humorist',
#                   'sv': u'brittisk f\xf6rfattare'},
#  u'employer': {'url': 'https://www.wikidata.org/wiki/Property:P108',
#                'values': [{'claim_id': u'Q42$853B16C8-1AB3-489A-831E-AEAD7E94AB87',
#                            'labels': {'de': u'British Broadcasting Corporation',
#                                       'en': u'BBC',
#                                       'sv': u'BBC'},
#                            'url': u'https://www.wikidata.org/wiki/Q9531'}]},
#  'full_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c0/Douglas_adams_portrait_cropped.jpg',
#  u'image_description': 'https://commons.wikimedia.org/wiki/File:Douglas_adams_portrait_cropped.jpg',
#  'labels': {'de': u'Douglas Adams',
#             'en': u'Douglas Adams',
#             'sv': u'Douglas Adams'},
#  u'occupation': {'url': 'https://www.wikidata.org/wiki/Property:P106',
#                  'values': [{'claim_id': u'Q42$e0f736bd-4711-c43b-9277-af1e9b2fb85f',
#                              'labels': {'de': u'Dramatiker',
#                                         'en': u'playwright',
#                                         'sv': u'dramatiker'},
#                              'url': u'https://www.wikidata.org/wiki/Q214917'},
#                             {'claim_id': u'q42$E13E619F-63EF-4B72-99D9-7A45C7C6AD34',
#                              'labels': {'de': u'Drehbuchautor',
#                                         'en': u'screenwriter',
#                                         'sv': u'manusf\xf6rfattare'},
#                              'url': u'https://www.wikidata.org/wiki/Q28389'},
#                             {'claim_id': u'Q42$D6E21D67-05D6-4A0B-8458-0744FCEED13D',
#                              'labels': {'de': u'Romancier',
#                                         'en': u'novelist',
#                                         'sv': u'romanf\xf6rfattare'},
#                              'url': u'https://www.wikidata.org/wiki/Q6625963'},
#                             {'claim_id': u'Q42$7eb8aaef-4ddf-8b87-bd02-406f91a296bd',
#                              'labels': {'de': u'Kinderbuchautor',
#                                         'en': u"children's writer",
#                                         'sv': u'barnboksf\xf6rfattare'},
#                              'url': u'https://www.wikidata.org/wiki/Q4853732'},
#                             {'claim_id': u'q42$CBDC4890-D5A2-469C-AEBB-EFB682B891E7',
#                              'labels': {'de': u'Science-Fiction-Schriftsteller',
#                                         'en': u'science fiction writer',
#                                         'sv': u'science fiction-f\xf6rfattare'},
#                              'url': u'https://www.wikidata.org/wiki/Q18844224'},
#                             {'claim_id': u'Q42$58F0D772-9CE4-46AC-BF0D-FBBBAFA09603',
#                              'labels': {'de': u'Komiker',
#                                         'en': u'comedian',
#                                         'sv': u'komiker'},
#                              'url': u'https://www.wikidata.org/wiki/Q245068'},
#                             {'claim_id': u'Q42$e469cda0-475d-8bb1-1dcd-f72c91161ebf',
#                              'labels': {'de': u'Dramaturg',
#                                         'en': u'dramaturge',
#                                         'sv': u'dramaturg'},
#                              'url': u'https://www.wikidata.org/wiki/Q487596'}]},
#  u'place of birth': {'url': 'https://www.wikidata.org/wiki/Property:P19',
#                      'values': [{'claim_id': u'q42$3D284234-52BC-4DA3-83A3-7C39F84BA518',
#                                  'labels': {'de': u'Cambridge',
#                                             'en': u'Cambridge',
#                                             'sv': u'Cambridge'},
#                                  'url': u'https://www.wikidata.org/wiki/Q350'}]},
#  'wikidata_id': 'Q42',
#  'wikidata_timestamp': '+2018-10-04T02:20:35Z'}
# {'url': 'https://www.wikidata.org/wiki/Property:P17',
#  'values': [{'claim_id': u'Q42@q350$8E72D3A5-A067-47CB-AF45-C73ED7CFFF9E',
#              'labels': {'de': u'Vereinigtes K\xf6nigreich',
#                         'en': u'United Kingdom',
#                         'sv': u'Storbritannien'},
#              'url': u'https://www.wikidata.org/wiki/Q145'}]}
# {'country': {'url': 'https://www.wikidata.org/wiki/Property:P17',
#              'values': [{'claim_id': u'Q42@q350$8E72D3A5-A067-47CB-AF45-C73ED7CFFF9E',
#                          'labels': {'de': u'Vereinigtes K\xf6nigreich',
#                                     'en': u'United Kingdom',
#                                     'sv': u'Storbritannien'},
#                          'url': u'https://www.wikidata.org/wiki/Q145'}]},
#  'labels': {'de': u'Douglas Adams',
#             'en': u'Douglas Adams',
#             'sv': u'Douglas Adams'},
#  'wikidata_id': 'Q42',
#  'wikidata_timestamp': '+2018-10-04T02:20:35Z'}
