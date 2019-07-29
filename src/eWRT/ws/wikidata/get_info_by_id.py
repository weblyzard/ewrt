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


if __name__ == '__main__':
    try:
        item = pywikibot.ItemPage(repo, sys.argv[1])
    except IndexError:
        print('Required command line argument: QXXX-id of the entity.')
        exit()
    item.get()
    claims = {}
    if item.claims:
        for claim in item.claims:
            if claim in CLAIMS_OF_INTEREST:
                targets = [(value, value.getTarget())
                           for value in item.claims[claim]]
                claims[name_or_id(claim)] = data = []
                for container, value in targets:
                    value_data = {}
                    try:
                        try:
                            value_data['value'] = value.text['labels']['en']
                        except TypeError:
                            value_data['value'] = value.text

                    except AttributeError:
                        value_data['value'] = value
                    if container.qualifiers:
                        value_data['qualifiers'] = {q: container.qualifiers[q][0].target for q in
                                                    container.qualifiers}
                    data.append(value_data)
        pprint(claims)

# exemplary output with command line argument Q42 (Douglas Adams):
#
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
