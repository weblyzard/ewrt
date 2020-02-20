#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Modified on September 6

@author: jakob <jakob.steixner@modul.ac.at>

CLI to extract additional information from wikidata for a (person) entity with
a known id.
entity types.
Starting point is the
[pywikibot manual](https://www.mediawiki.org/wiki/Manual:Pywikibot/Wikidata)'''
from __future__ import print_function
import sys

from pprint import pprint

from eWRT.ws.wikidata.definitions import person_properties

try:
    import pywikibot
except RuntimeError:
    import os

    os.environ['PYWIKIBOT_NO_USER_CONFIG'] = '1'
    import pywikibot

# any site will work, this is just an example
site = pywikibot.Site('en', 'wikipedia')
repo = site.data_repository()  # this is a DataSite object

CLAIMS_OF_INTEREST = ["P19", 'P39', 'P106', 'P108', 'P102', 'P1411']


def name_or_id(claim_id):
    try:
        return person_properties[claim_id]
    except KeyError:
        return claim_id


def get_claim_values_by_id(entity_id, claims_of_interest, language='en',
                           human_readable_claims=True):
    """
    :param entity_id: Qxxx id of entity
    :param claims_of_interest: iterable of attributes with their Pxx identifiers
    :param language: language ISO code, e.g. 'en'
    :param human_readable_claims: map claims to their (English) label where
        possible (configured for persons only)
    :return: dictionary of attributres of entity given by entity_id, filtered
        by claims_of_interest
    """
    item = pywikibot.ItemPage(repo, entity_id)
    claims_of_interest = claims_of_interest or [c for c in CLAIMS_OF_INTEREST]
    item.get()
    claims = {}
    if item.claims:
        for claim in item.claims:
            if claim in claims_of_interest:
                claim_identifier = name_or_id(claim) if human_readable_claims else claim
                targets = [(value, value.getTarget())
                           for value in item.claims[claim]]
                claims[claim_identifier] = data = []
                for container, value in targets:
                    value_data = {}
                    try:
                        try:
                            value_data['value'] = value.text['labels'][language]
                        except TypeError:
                            value_data['value'] = value.text

                    except AttributeError:
                        value_data['value'] = value
                    if container.qualifiers:
                        value_data['qualifiers'] = {
                            q: container.qualifiers[q][0].target for q in
                            container.qualifiers}
                    data.append(value_data)
    return claims


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--item-id', dest='item_id', required=True)
    parser.add_argument('--claim-ids', dest='claim_ids',
                        default=CLAIMS_OF_INTEREST, required=False, nargs='*')
    parser.add_argument('--language', dest='language', default='en')
    parser.add_argument('--human-readable-claims', dest='human_readable',
                        default=False, required=False, action='store_true')
    args = parser.parse_args()
    pprint(get_claim_values_by_id(
        args.item_id, claims_of_interest=args.claim_ids,
        language=args.language,
        human_readable_claims=args.human_readable)
    )

# exemplary outputs for Q42 (Douglas Adams):
# $ get_info_by_id.py --item-id Q42 --claim-ids P106 # wikidata ids for claims,
# # only interested in P106=occupation
# {'P106': [{'value': 'playwright'},
#           {'value': 'screenwriter'},
#           {'value': 'novelist'},
#           {'value': "children's writer"},
#           {'value': 'science fiction writer'},
#           {'value': 'comedian'}]}
#
# $ get_info_by_id.py --item-id Q42 --human-readable-claims # default claims,
# # representation in human readable form
#     {u'P1411': [{'qualifiers': {u'P1686': ItemPage(Q3521267),
#                                 u'P585': WbTime(year=1979, month=0, day=0, hour=0, minute=0,
#                                                 second=0, precision=9, before=0, after=0,
#                                                 timezone=0,
#                                                 calendarmodel=http: // www.wikidata.org / entity / Q1985727)},
#     'value': u'Hugo Award for Best Dramatic Presentation'},
#     {'qualifiers': {u'P1686': ItemPage(Q721),
#                     u'P585': WbTime(year=1983, month=0, day=0, hour=0, minute=0, second=0,
#                                     precision=9, before=0, after=0, timezone=0,
#                                     calendarmodel=http: // www.wikidata.org / entity / Q1985727)},
#     'value': u'Locus Award for Best Science Fiction Novel'}],
#     u'employer': [{'value': u'BBC'}],
#     u'occupation': [{'value': u'playwright'},
#                                  {'value': u'screenwriter'},
#                                  {'value': u'novelist'},
#                                  {'value': u"children's writer"},
#                                  {'value': u'science fiction writer'},
#                                  {'value': u'comedian'},
#                                  {'value': u'dramaturge'}],
#                                 u'place of birth': [{'value': u'Cambridge'}]}
