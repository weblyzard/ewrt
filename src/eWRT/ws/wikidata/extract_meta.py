#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on September 13, 2018

@author: Jakob Steixner, <jakob.steixner@modul.ac.at

Loop

'''

import sys

import pywikibot.pagegenerators
from eWRT.ws.wikidata.enrich_from_wikipedia import wp_summary_from_wdid
from eWRT.ws.wikidata.wikibot_parse_item import ParseItemPage

ENTITY_TYPE_IDENTIFIERS = {
    'person': 'Q5',
    'organization': 'Q43229',
    'geo': 'Q2221906'
}

ENTITY_TYPES = ['organization', 'person', 'geo']

QUERY = """SELECT ?item WHERE{
  ?item wdt:P31|wdt:P279* wd:%s .
 }
LIMIT %s
OFFSET %s
"""

WIKIDATA_SITE = pywikibot.Site("wikidata", "wikidata")


def collect_attributes_from_wd_and_wd(itempage, languages, wd_parameters,
                                      include_literals=True):
    """

    :param itempage: ItemPage from which to collect information
    :param languages: list of languages in which to include literals
            and Wikipedia information
    :param wd_parameters: list of wikidata properties (Pxxx codes) to be
            included, if present
    :param include_literals: Include properties and alternate names. If
            false, only labels are
            included.
    :returns: a dictionary of the collected details about this entity from
            both Wikipedia and Wikidata.
    """
    # with open('wd_dump.json', 'w') as dump:
    # itempage.get()
    wikipedia_data = wp_summary_from_wdid(itempage.id, languages=languages,
                                          sitelinks=itempage.sitelinks)
    if not wikipedia_data:
        raise ValueError
    
    # use the Wikipedia article in the first language found as the entity's
    # unique preferred `url`.
    entity_extracted_details = {'url': wikipedia_data[0]['url']}
    for language in wikipedia_data:
        entity_extracted_details[language['language'] + 'wiki'] = language
    
    entity = ParseItemPage(itempage, include_literals=include_literals,
                           claims_of_interest=wd_parameters,
                           languages=languages)
    entity_extracted_details.update(entity.details)
    entity_extracted_details['wikidata_id'] = itempage.id
    
    return entity_extracted_details


def collect_entities_iterative(limit_per_query, n_queries, wd_parameters,
                               include_literals, entity_type, languages):
    """Get a list of entities
    :param languages: list if languages (ISO codes); the order determines
        which one's Wikipedia page will be used for the preferred `url`.
    :param entity_type: type of entity ('person', 'organization' or 'geo')
    :param include_literals: include 'aliases' and 'descriptions' (bool)
    :type include_literals: bool
    :param wd_parameters: list of wikidata properties to include in result
    :type wd_parameters: list
    :param limit_per_query: LIMIT set in the SPARQL query
    :type limit_per_query: int
    :param n_queries: maximum number of subsequent queries
    :type n_queries: int
    """
    
    for i in range(n_queries):
        wikidata_site = WIKIDATA_SITE
        query = QUERY % (ENTITY_TYPE_IDENTIFIERS[entity_type],
                         limit_per_query,
                         limit_per_query * i)
        # logger.debug('Query is\n' + query)
        generator = pywikibot.pagegenerators.WikidataSPARQLPageGenerator(
            query, site=wikidata_site)
        if not generator:
            break
        # parsed_entities = []
        for j in range(limit_per_query):
            try:
                if sys.version_info.major == 3:
                    entity_raw = next(generator)
                else:
                    entity_raw = generator.next()
                entity_raw.get()
            
            except StopIteration:
                break
            
            try:
                yield collect_attributes_from_wd_and_wd(
                    entity_raw,
                    languages=languages,
                    wd_parameters=wd_parameters,
                    include_literals=include_literals)
            except ValueError:
                continue


if __name__ == '__main__':
    import pprint
    from eWRT.ws.wikidata.wp_to_wd import wikidata_from_wptitle
    
    obama = wikidata_from_wptitle('Barack Obama')
    wd_parameters = [
        'P18',  # image
        'P17',  # country
        'P19',  # place of birth
        'P39',  # position held
        'P569',  # date of birth
        'P570',  # date of death
        'P1411'  # nominated for
    ]
    pprint.pprint(collect_attributes_from_wd_and_wd(obama,
                                                    languages=['de', 'en',
                                                               'hr'],
                                                    wd_parameters=wd_parameters,
                                                    include_literals=False))
