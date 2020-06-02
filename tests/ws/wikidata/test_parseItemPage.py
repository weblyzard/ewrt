#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on September 24, 2018

@author: jakob <jakob.steixner@modul.ac.at>
'''
from __future__ import print_function

import copy
import unittest

import mock
import pytest

from collections import OrderedDict



try:
    from pywikibot import Claim, ItemPage
    from pywikibot.site import DataSite
except RuntimeError:
    import os
    os.environ['PYWIKIBOT_NO_USER_CONFIG'] = '1'
    from pywikibot import Claim, ItemPage
    from pywikibot.site import DataSite

from eWRT.ws.wikidata.preferred_claim_value import attribute_preferred_value
from eWRT.ws.wikidata.sample_itempage import sample_output
from eWRT.ws.wikidata.wikibot_parse_item import ParseItemPage, DoesNotMatchFilterError


try:
    from eWRT.ws.wikidata.sample_itempage import itempage
    API_ERROR=False
except:
    API_ERROR = True


expected_labels = [('labels', 'en', {'labels': {'en': 'Douglas Adams'}}),
                       ('labels', 'ru', {'labels': {
                           'ru': u'\u0414\u0443\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441'}}),
                       ('labels', 'lv', {'labels': {'lv': u'Duglass Adamss'}}),
                       ('descriptions', u'nb', {'descriptions': {
                           'nb': u'engelsk science fiction-forfatter og humorist'}})]


@pytest.mark.skipif(API_ERROR is True, reason='external API not available')
class TestParseItemPage(unittest.TestCase):

    entity_mock = mock.Mock()
    entity_mock.text = itempage
    entity_mock.claims = itempage['claims']

    @pytest.mark.parametrize(u'literal_type,language,expected',
                             expected_labels)
    def test_extract_literal_properties(self, literal_type, language, expected):
        """test the extraction of literals (labels, descriptions)
        parametrized for language and type and literal returns the expected
        and only the expected result."""
        result = ParseItemPage.extract_literal_properties(entity=self.entity_mock,
                                                          languages=[language],
                                                          literals=[literal_type]
                                                          )
        assert result == expected


    def test_extract_literal_properties_freestanding(self):
        """

        :return:
        """
        claim = Claim.fromJSON(DataSite("wikidata", "wikidata"),
                               {u'type': u'statement', u'references': [{
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 5375741}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'355b56329b78db22be549dec34f2570ca61ca056',
                                   u'snaks-order': [
                                       u'P248']},
                                   {
                                   u'snaks': {
                                       u'P1476': [
                                           {
                                               u'datatype': u'monolingualtext',
                                               u'datavalue': {
                                                   u'type': u'monolingualtext',
                                                   u'value': {
                                                       u'text': u'Obituary: Douglas Adams',
                                                       u'language': u'en'}},
                                               u'property': u'P1476',
                                               u'snaktype': u'value'}],
                                       u'P407': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 1860}},
                                               u'property': u'P407',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002013-12-07T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P1433': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 11148}},
                                               u'property': u'P1433',
                                               u'snaktype': u'value'}],
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.theguardian.com/news/2001/may/15/guardianobituaries.books'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}],
                                       u'P577': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002001-05-15T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P577',
                                               u'snaktype': u'value'}],
                                       u'P50': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 18145749}},
                                               u'property': u'P50',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'3f4d26cf841e20630c969afc0e48e5e3ef0c5a49',
                                   u'snaks-order': [
                                       u'P854',
                                       u'P577',
                                       u'P813',
                                       u'P1433',
                                       u'P50',
                                       u'P1476',
                                       u'P407']},
                                   {
                                   u'snaks': {
                                       u'P123': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 192621}},
                                               u'property': u'P123',
                                               u'snaktype': u'value'}],
                                       u'P1476': [
                                           {
                                               u'datatype': u'monolingualtext',
                                               u'datavalue': {
                                                   u'type': u'monolingualtext',
                                                   u'value': {
                                                       u'text': u"Hitch Hiker's Guide author Douglas Adams dies aged 49",
                                                       u'language': u'en'}},
                                               u'property': u'P1476',
                                               u'snaktype': u'value'}],
                                       u'P407': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 1860}},
                                               u'property': u'P407',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002015-01-03T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.telegraph.co.uk/news/uknews/1330072/Hitch-Hikers-Guide-author-Douglas-Adams-dies-aged-49.html'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}],
                                       u'P577': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002001-05-13T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P577',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'51a934797fd7f7d3ee91d4d541356d4c5974075b',
                                   u'snaks-order': [
                                       u'P1476',
                                       u'P577',
                                       u'P123',
                                       u'P407',
                                       u'P854',
                                       u'P813']},
                                   {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 36578}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002015-07-07T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P227': [
                                           {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'119033364'},
                                               u'property': u'P227',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'a02f3a77ddd343e6b88be25696b055f5131c3d64',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P227',
                                       u'P813']}],
                                u'mainsnak': {
                                   u'datatype': u'wikibase-item',
                                   u'datavalue': {
                                       u'type': u'wikibase-entityid',
                                       u'value': {
                                           u'entity-type': u'item',
                                           u'numeric-id': 350}},
                                   u'property': u'P19',
                                   u'snaktype': u'value'},
                                u'id': u'q42$3D284234-52BC-4DA3-83A3-7C39F84BA518',
                                u'rank': u'normal'})
        # target_id = 'Q{}'.format(claim['mainsnak']['datavalue']['value']['numeric-id'])

        target = claim.target
        # target = pywikibot.ItemPage.from_entity_uri(site=DataSite('wikidata', 'wikidata'), uri=target_id)
        result = ParseItemPage.extract_literal_properties(
            entity=target, languages=['en'], literals=['labels'])
        print(result)
        assert result['labels']['en'] == 'Cambridge'
        entity_id = 'Q350'
        target = ItemPage.from_entity_uri(
            site=DataSite('wikidata', 'wikidata'), uri='http://www.wikidata.org/entity' + '/' + entity_id)
        print(target)
        result = ParseItemPage.extract_literal_properties(
            entity=target, languages=['en'], literals=['labels'])
        print(result)
        assert result['labels']['en'] == 'Cambridge'


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


    def test_complete_claim_details(self):
        """With the given name parameter ('P735') as an example, test
        that the result is the expected result, including a list of values (first
        and second name), one marked as preferred (the first name)."""
        entity = self.entity_mock
        names = entity.text['claims']['P735']
        names_result = ParseItemPage.complete_claim_details(
            'P735',
            names,
            ['en'],
            ['labels']
        )
        assert names_result == self.expected_names_result


    def test_attribute_preferred_value(self):
        """test_complete_claim_details already implicitly tests that a preferred
        value is marked when present. This test focuses on the correct behaviour
        when this is not the case: A result without a 'preferred'-key for
        complete_claim_details, an error when 'attribute_preferred_value is called
        directly.
        """
        names = self.entity_mock.claims['P735']
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


    def test_get_country_from_location(self):
        # we expect a ValueError when the only local attribute tried is
        # P17 = country - Douglas Adams doesn't have a country attribute
        try:
            country_found = ParseItemPage.get_country_from_any(
                self.entity_mock,
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
                self.entity_mock,
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
            self.entity_mock,
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
            self.entity_mock,
            local_attributes=local_attributes,
            languages=['en'])
        assert len(country_found) == 1
        assert country_found == \
            [{'url': u'https://www.wikidata.org/wiki/Q30',
              'labels': {'en': u'United States of America'},
              'claim_id': u'q159288$0D0A08B9-BC36-4B45-B1CF-5547215DEFCB'
              # this claim is actually about Santa Barbara being in the US, not
              # about Adams per se
              }
             ]


    def result_without_timestamp(self, result):
        return dict([item for item in list(result.items()) if item[0] != 'wikidata_timestamp'])


    def test_parseItemPage_all(self):
        entity = itempage
        import pprint
        parsed_without_attribute_labels = ParseItemPage(entity,
                                                        include_literals=True,
                                                        languages=['en', 'de',
                                                                   'sv'],
                                                        resolve_country=False,
                                                        include_attribute_labels=False
                                                        ).details

        parsed_with_attribute_labels = ParseItemPage(entity, include_literals=True,
                                                     languages=['en', 'de', 'sv'],
                                                     resolve_country=False,
                                                     include_attribute_labels=True
                                                     ).details
        assert set(parsed_with_attribute_labels.keys()) == set(
            parsed_without_attribute_labels.keys())
        assert not any(
            ('labels' in val for val in list(parsed_without_attribute_labels.values())))
        # assert any(('labels' in val for val in parsed_with_attribute_labels.values()))
        assert all((parsed_with_attribute_labels[literal] ==
                    parsed_without_attribute_labels[literal]
                    for literal in ('labels', 'descriptions', 'aliases')))
        pprint.pprint(parsed_with_attribute_labels)

        assert self.result_without_timestamp(
            parsed_with_attribute_labels) == self.result_without_timestamp(
            sample_output
        )
        for val in list(parsed_with_attribute_labels.values()):
            if 'values' in val and 'P18' not in val['url']:
                assert all(('labels' in sub_val for sub_val in val['values']))
        parsed_with_country = ParseItemPage(entity,
                                            include_literals=False,
                                            wd_parameters={},
                                            languages=['en', 'de',
                                                       'sv'],
                                            resolve_country=True,
                                            include_attribute_labels=True,
                                            qualifiers_of_interest=[],
                                            entity_type='person',
                                            ).details
        assert 'country' in parsed_with_country
        pprint.pprint(parsed_with_country['country'])
        pprint.pprint(parsed_with_country)
        assert parsed_with_country['country'] == {
            'url': 'https://www.wikidata.org/wiki/Property:P17',
            'values': [
                {'claim_id': u'q350$8E72D3A5-A067-47CB-AF45-C73ED7CFFF9E',
                 'derived': True,
                 'labels': {'de': u'Vereinigtes K\xf6nigreich',
                            'en': u'United Kingdom',
                            'sv': u'Storbritannien'},
                 'url': u'https://www.wikidata.org/wiki/Q145'}]
        }


    def test_parseItemPage_filter(self):
        """Filtering method, allows to filter entities by a) presence of a certain
        parameter or b) maximal/minimal value (use +/- prefixed string for dates!)"""
        try:
            filter_params = {'person': [('P39', 'has_attr', None)]}
            parsed_with_filter = ParseItemPage(itempage,
                                               include_literals=True,
                                               languages=['en', 'de',
                                                          'sv'],
                                               resolve_country=False,
                                               include_attribute_labels=False,
                                               param_filter=filter_params,
                                               entity_type='person'
                                               ).details
            raise ValueError('The sample itempage does not contain a claim "P39", '
                             'this should raise an error!')
        except DoesNotMatchFilterError:
            pass
        try:
            filter_params = {'person': [('P569', 'min', '+1952-01-01')]}
            parsed_with_filter = ParseItemPage(itempage,
                                               include_literals=True,
                                               languages=['en', 'de',
                                                          'sv'],
                                               resolve_country=False,
                                               include_attribute_labels=False,
                                               param_filter=filter_params,
                                               entity_type='person'
                                               ).details
            parsed_without_filter = ParseItemPage(itempage,
                                                  include_literals=True,
                                                  languages=['en', 'de',
                                                             'sv'],
                                                  resolve_country=False,
                                                  include_attribute_labels=False,
                                                  entity_type='person'
                                                  ).details
            assert parsed_with_filter == parsed_without_filter
        except ValueError:
            raise ValueError('The sample itempage does contain a claim "P19" '
                             '(place of birth), this should pass the filter')
        try:
            filter_params = {'person': [('P569', 'min', '+1952-01-01')]}
            parsed_with_filter = ParseItemPage(itempage,
                                               include_literals=True,
                                               languages=['en', 'de',
                                                          'sv'],
                                               resolve_country=False,
                                               include_attribute_labels=False,
                                               param_filter=filter_params,
                                               entity_type='person'
                                               ).details
        except ValueError:
            raise ValueError('Failed to identify Douglas Adams birth date as '
                             '>= 1952')
        try:
            filter_params = {'person': [('P569', 'min', '+1955-01-01')]}
            parsed_with_filter = ParseItemPage(itempage,
                                               include_literals=True,
                                               languages=['en', 'de',
                                                          'sv'],
                                               resolve_country=False,
                                               include_attribute_labels=False,
                                               param_filter=filter_params,
                                               entity_type='person'
                                               ).details
            raise ValueError('Douglas Adams misidentified as being younger than '
                             '1955-01-01')
        except DoesNotMatchFilterError:
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
