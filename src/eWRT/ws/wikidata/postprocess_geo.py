#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on September 13, 2018

@author: Jakob Steixner, <jakob.steixner@modul.ac.at

Extract country information from any geo attribute (location,
place of birth, citizenship, headquarters location, located in
the administrative unit,...) as may be present, depending on
entity type.

Usage as CLI: python postprocess_geo.py <title> [<language>]
language defaults to 'en'

'''

import sys
import warnings

import pywikibot
from eWRT.ws.wikidata.definitions import local_attributes, COUNTRY_ISO2_CODES_DICT
from eWRT.ws.wikidata.enrich_from_wikipedia import RELEVANT_LANGUAGES
from eWRT.ws.wikidata.extract_meta import WIKIDATA_SITE
from eWRT.ws.wikidata.wikibot_parse_item import ParseItemPage
from eWRT.ws.wikidata.wp_to_wd import wikidata_from_wptitle
from eWRT.ws.wikidata.preferred_claim_value import attribute_preferred_value


def extract_country_or_none(entity_extract, location_attributes=None):
    """Enrich a processed item in dict form (output of
    eWRT.ws.wikidata.extract_meta.collect_attributes_from_wp_and_wd)
    with country information using whatever local attribute is available
    :param entity_extract: input dict with attribute:value pairs"""
    if location_attributes is None:
        location_attributes = local_attributes

    try:
        entity_id = entity_extract['wikidata_id']
    except TypeError:
        entity_id = entity_extract.id
    entity = pywikibot.ItemPage(WIKIDATA_SITE, title=entity_id)
    try:
        countries_found = ParseItemPage.get_country_from_any(
            entity,
            local_attributes=location_attributes,
            languages=RELEVANT_LANGUAGES)
        if len(countries_found) > 1:
            warnings.warn(
                'More than one country found for entity {}'.format(entity_id))
        return countries_found
    except ValueError:
        warnings.warn(
            'Unable to determine country for entity {}!'.format(entity_id))
        return None


def item_with_country(wikipedia_title, language=['en'], location_attributes=local_attributes,return_type='label'):
    itempage = wikidata_from_wptitle(wikipedia_title, language=language)
    country = extract_country_or_none(itempage,location_attributes=location_attributes)
    country = attribute_preferred_value(country)
    if return_type == 'labels':
        return country[0]['labels'][language]
    elif return_type == 'iso':
        return country[0]['url']


if __name__ == '__main__':
    try:
        wikipedia_title = sys.argv[1]
    except IndexError:
        raise ValueError('Required argument: exact page title.')
    try:
        language = sys.argv[2]
    except IndexError:
        print('No language specified, assuming English (\'en\').')
        language = 'en'
    print(item_with_country(wikipedia_title, language))
