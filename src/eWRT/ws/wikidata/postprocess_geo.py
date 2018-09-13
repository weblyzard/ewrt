#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on September 13, 2018

@author: Jakob Steixner, <jakob.steixner@modul.ac.at

Retrieve Wikidata's image based on (exact) Wikipedia
article in any language. Also allows to retrieve other
types of images (e.g. flags, coats of arms, etc.) where given.

'''

import warnings

import pywikibot
from eWRT.ws.wikidata.definitions import local_attributes
from eWRT.ws.wikidata.extract_meta import collect_wikidata_attributes, WIKIDATA_SITE, \
    RELEVANT_LANGUAGES, ParseItemPage
from eWRT.ws.wikidata.wp_to_wd import get_country_from_location
from eWRT.ws.wikidata.wp_to_wd import wikidata_from_wptitle


def get_country_from_any(itempage, local_attributes=local_attributes):
    """
    When an country
    :param itempage:
    :return:
    """
    itempage.get()
    for location_type in local_attributes:
        if location_type in itempage.claims:
            for location in itempage.claims[location_type]:
                try:
                    return get_country_from_location(location.target)
                except ValueError:
                    pass
    raise ValueError


def extract_country_or_none(entity_extract):
    """Enrich a processed item in dict form (output of
    eWRT.ws.wikidata.extract_meta.collect_wikidata_attributes)
    with country information usingg"""
    entity_id = entity_extract['wikidata_id']
    entity = pywikibot.ItemPage(WIKIDATA_SITE, title=entity_id)
    try:
        source_geo = get_country_from_any(entity)
    except ValueError:
        source_geo = None
        warnings.warn('Unable to determine source geo for entity {}!'.format(entity_id))
    return source_geo[0]


if __name__ == '__main__':
    
    freud = wikidata_from_wptitle('Sigmund Freud')
    # country = extract_best_country(freud)
    freud_parsed = collect_wikidata_attributes(freud, ['en'])
    source_geo = extract_country_or_none(freud_parsed)

    freud_parsed['country'] = ParseItemPage.extract_literal_properties(source_geo, RELEVANT_LANGUAGES)[
        'labels']['en']

    assert freud_parsed['country'] == 'Czech Republic'

