#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on October 04, 2018

@author: jakob <jakob.steixner@modul.ac.at>
'''
import datetime

import mock
import pytest
from eWRT.ws.wikidata.bundle_wikipedia_requests import collect_multiple_from_wikipedia, \
    wikipedia_request_dispatcher, batch_enrich_from_wikipedia

GW_snapshot_wikidata_result = {
    u'https://www.wikidata.org/wiki/Q23': {u'frwiki': u'George Washington',
                                           u'position held': {
                                               'url': 'https://www.wikidata.org/wiki/Property:P39',
                                               'values': [{
                                                   'url': u'https://www.wikidata.org/wiki/Q11696',
                                                   'temporal_attributes': {
                                                       'end date': u'+1797-03-04T00:00:00Z',
                                                       'start date': u'+1789-04-30T00:00:00Z'},
                                                   'labels': {
                                                       'de': u'Pr\xe4sident der Vereinigten Staaten',
                                                       'en': u'President of the United States',
                                                       'fr': u'pr\xe9sident des \xc9tats-Unis',
                                                       'es': u'presidente de Estados Unidos'},
                                                   'claim_id': u'q23$B6E5D112-C27E-4E3F-BB65-CB12B9364092'},
                                                   {
                                                       'url': u'https://www.wikidata.org/wiki/Q1115127',
                                                       'temporal_attributes': {
                                                           'end date': u'+1799-12-14T00:00:00Z',
                                                           'start date': u'+1798-07-13T00:00:00Z'},
                                                       'labels': {
                                                           'de': u'Commanding General of the United States Army',
                                                           'en': u'Commanding General of the United States Army',
                                                           'fr': u'Commanding General of the United States Army',
                                                           'es': u'comandante general del Ej\xe9rcito de los Estados Unidos'},
                                                       'claim_id': u'Q23$6A44E261-3592-4928-979B-0BF1CAB2D39C'},
                                                   {
                                                       'url': u'https://www.wikidata.org/wiki/Q1115127',
                                                       'temporal_attributes': {
                                                           'end date': u'+1788-12-23T00:00:00Z',
                                                           'start date': u'+1775-06-15T00:00:00Z'},
                                                       'labels': {
                                                           'de': u'Commanding General of the United States Army',
                                                           'en': u'Commanding General of the United States Army',
                                                           'fr': u'Commanding General of the United States Army',
                                                           'es': u'comandante general del Ej\xe9rcito de los Estados Unidos'},
                                                       'claim_id': u'Q23$2c113ca2-4177-4a24-eb0c-6c284ff03416'}]},
                                           'wikidata_timestamp': '2018-10-03T00:05:30Z',
                                           'url': u'https://www.wikidata.org/wiki/Q23',
                                           u'date of birth': {
                                               'url': 'https://www.wikidata.org/wiki/Property:P569',
                                               'values': [{
                                                   'claim_id': u'Q23$3BF0223A-D656-435B-9FD1-32E0B8F54A69',
                                                   'value': u'+1732-02-22T00:00:00Z'}]},
                                           u'dewiki': u'George Washington',
                                           u'eswiki': u'George Washington',
                                           'labels': {
                                               'de': u'George Washington',
                                               'en': u'George Washington',
                                               'fr': u'George Washington',
                                               'es': u'George Washington'},
                                           u'place of birth': {
                                               'url': 'https://www.wikidata.org/wiki/Property:P19',
                                               'values': [{
                                                   'url': u'https://www.wikidata.org/wiki/Q495645',
                                                   'labels': {
                                                       'de': u'Westmoreland County',
                                                       'en': u'Westmoreland County',
                                                       'fr': u'comt\xe9 de Westmoreland',
                                                       'es': u'Condado de Westmoreland'},
                                                   'claim_id': u'Q23$ca56ecac-bad6-4d4c-ad29-36a26244955a'}]},
                                           u'enwiki': u'George Washington',
                                           'descriptions': {
                                               'de': u'erster Pr\xe4sident der Vereinigten Staaten von Amerika',
                                               'en': u'first President of the United States',
                                               'fr': u"premier pr\xe9sident des \xc9tats-Unis d'Am\xe9rique",
                                               'es': u'primer presidente de los Estados Unidos de Am\xe9rica'},
                                           'wikidata_id': u'Q23', 'country': {
            'url': 'https://www.wikidata.org/wiki/Property:P17', 'values': [
                {'url': u'https://www.wikidata.org/wiki/Q30',
                 'labels': {'de': u'Vereinigte Staaten',
                            'en': u'United States of America',
                            'fr': u'\xc9tats-Unis', 'es': u'Estados Unidos'},
                 'claim_id': u'Q23@q495645$A10AFE59-9C11-40BC-87A5-567221D430AA'}]},
                                           'aliases': {'de': [
                                               u'Pr\xe4sident Washington',
                                               u'G. Washington'],
                                               'en': [u'Washington',
                                                      u'President Washington',
                                                      u'G. Washington',
                                                      u'Father of the United States']}}}

GW_snapshot_wikipedia_result = {
    'url': u'https://en.wikipedia.org/wiki/George_Washington',
    'timestamp': u'2018-10-04T05:06:49Z',
    'title': u'George Washington',
    'language': 'en',
    'summary': u'George Washington (February 22, 1732 \u2013 December 14, 1799) was '
               u'one of the Founding Fathers of the United States and served as '
               u'the nation\u2019s first President (1789\u20131797). In the '
               u'American Revolutionary War, he commanded Patriot forces to '
               u'victory against the British and their allies. He presided over '
               u'the Constitutional Convention of 1787 which established the new '
               u'federal government, and he has been called the "Father of His '
               u'Country".\nWashington was born to a moderately prosperous '
               u'Virginian family of colonial planters and slaveholders. He '
               u'had early educational opportunities, learned mathematics, '
               u'and soon launched a successful career as a surveyor which '
               u'enabled him to make significant land investments. He then '
               u'joined the Virginia militia and fought in the French and Indian '
               u'War. He was appointed commander-in-chief of the Continental Army '
               u'during the Revolutionary War, leading an allied campaign to '
               u'victory at the Siege of Yorktown which ended the war. His '
               u'devotion to Republicanism and revulsion for tyrannical power '
               u'impelled him to decline further authority after victory, and '
               u'he resigned as commander-in-chief in 1783.\nAs one of the '
               u'country\u2019s premier statesmen, Washington was unanimously '
               u'elected President by the Electoral College in the first two '
               u'national elections. He promoted and oversaw implementation of '
               u'a strong, well-financed national government. He remained '
               u'impartial in the fierce rivalry between cabinet secretaries '
               u'Thomas Jefferson and Alexander Hamilton, although he adopted '
               u'Hamilton\'s economic plans. When the French Revolution plunged '
               u'Europe into war, Washington assumed a policy of neutrality to '
               u'protect American ships\u2014although the controversial Jay '
               u'Treaty of 1795 normalized trade relations with Great Britain. '
               u'He set precedents still in use today, such as the Cabinet '
               u'advisory system, the inaugural address, the title "Mr. '
               u'President", and the concept of a two-term office limit. His '
               u'Farewell Address strongly warned against political partisanship, '
               u'sectionalism, and involvement in foreign wars.\nWashington '
               u'inherited slaves at age 11 and officially supported other '
               u'slaveholders as late as 1793. He eventually became troubled '
               u'with slavery, however, and he freed all his slaves in his will '
               u'in 1799. He is widely known for his religious toleration while '
               u'his religious beliefs have been thoroughly debated by '
               u'historians. Upon his death, Washington was famously eulogized as '
               u'"first in war, first in peace, and first in the hearts of his '
               u'countrymen". He has been widely memorialized by monuments, art, '
               u'places, stamps, and currency, and has been consistently ranked '
               u'by scholars among the top American presidents.'}

sitelink_cache = {
    'en': {'George Washington': u'https://www.wikidata.org/wiki/Q23'}}

# mock_enrich = mock.Mock()
# mock_enrich.return_value = (el for el in [GW_snapshot_wikipedia_result])

def batch_enrich_mock(title, language):
    print(title
          )
    assert (language, title) == ('en', u'George Washington')
    return ((GW_snapshot_wikipedia_result,))


@mock.patch(
    target='eWRT.ws.wikidata.bundle_wikipedia_requests.wikipedia_page_info_from_title',
    new=batch_enrich_mock)
def test_batch_enrich_from_wikipedia():
    """
    Using a mock for wikipedia_page_info_from_title, this test runs fully
    offline."""
    enrichment_result = batch_enrich_from_wikipedia(
        wikipedia_pages=sitelink_cache['en'],
        entities_cache=GW_snapshot_wikidata_result,
        language='en',
    )
    merge_result = enrichment_result.next()
    assert_basic_structure_as_expected(merge_result)
    assert merge_result['enwiki'] == GW_snapshot_wikipedia_result


def test_collect_multiple_from_wikipedia():
    global sitelink_cache
    enrichment_result = collect_multiple_from_wikipedia(
        sitelinks_cache=sitelink_cache,
        entities_cache=GW_snapshot_wikidata_result
    ).next()

    try:
        modified_sitelink_cache = {'de': {}}
        enrichment_result = collect_multiple_from_wikipedia(
            sitelinks_cache=modified_sitelink_cache,
            entities_cache=GW_snapshot_wikidata_result
        ).next()
        raise ValueError
    except StopIteration:
        pass



def test_enrich_from_wikipedia_offline():
    """
    No mock, real call to Wikipedia API, basic structure should still be
    the same but literal equivalence between merge_result['enwiki'] and
    cached snapshot is not expected
    """
    with mock.patch(target='eWRT.ws.wikidata.bundle_wikipedia_requests.wikipedia_page_info_from_title',
            new=batch_enrich_mock):
        enrichment_result = batch_enrich_from_wikipedia(
            wikipedia_pages=sitelink_cache['en'],
            entities_cache=GW_snapshot_wikidata_result,
            language='en',
        ).next()
    assert_basic_structure_as_expected(enrichment_result)
    assert GW_snapshot_wikipedia_result['timestamp'] == enrichment_result['enwiki']['timestamp']


def assert_basic_structure_as_expected(merged_result):
    """
    Check whether the basic structure and keys included are as expected.
    :param merged_result:
    :return:
    """
    assert isinstance(merged_result, dict)
    assert merged_result['language'] == 'en'
    other_language_wikis = ('dewiki', 'frwiki', 'eswiki')
    # assert all([key not in merged_result for key in other_language_wikis])
    assert merged_result['labels'] == 'George Washington'
    assert all([key in merged_result['enwiki'] for key in
                GW_snapshot_wikipedia_result])
    assert isinstance(merged_result['enwiki'], dict)
    wiki_timestamp = merged_result['enwiki']['timestamp']
    try:
        datetime.datetime.strptime(wiki_timestamp, u'%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        raise ValueError('Timestamp doesn\'t appear to be a valid time. '
                         'Timestamp returned was: {}, expected format  {}'.format(
            wiki_timestamp,
            datetime.datetime.now().strftime(u'%Y-%m-%dT%H:%M:%SZ')))
    assert u'2018-10-04T05:06:49Z' <= merged_result['enwiki'][
        'timestamp'] < datetime.datetime.now().strftime(u'%Y-%m-%dT%H:%M:%SZ')
    # todo: add test for similarity of retrieved summary with snapshot?

def mock_batch_enrich(*args, **kwargs):
    for i in range(20): yield {}
@mock.patch(
    target='eWRT.ws.wikidata.bundle_wikipedia_requests.batch_enrich_from_wikipedia',
    new=mock_batch_enrich)
@pytest.mark.skip
def test_wikipedia_request_dispatcher():
    sitelink_cache = {'en': {str(i): i for i in range(100)}}
    results = wikipedia_request_dispatcher(sitelinks_cache=sitelink_cache,
                                           entity_cache=GW_snapshot_wikidata_result,
                                           languages=['en'])

    returned = [result for result in results]
    assert returned
    assert len(returned) == 100

