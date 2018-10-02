#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on September 13, 2018

@author: Jakob Steixner, <jakob.steixner@modul.ac.at

Loop

'''

import sys

import pywikibot.pagegenerators
import requests
from eWRT.ws.wikidata.enrich_from_wikipedia import wp_summary_from_wdid
from eWRT.ws.wikidata.wikibot_parse_item import ParseItemPage
from wikipedia import RedirectError, DisambiguationError

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


def get_wikidata_timestamp(item_page):
    # ItemPages come in two slightly different formats depending on how
    # they were created (probably a bug in pywikibot). We want to be able to
    # deal with both:
    try:
        timestamp = item_page.timestamp
    except AttributeError:
        timestamp = item_page.latest_revision.timestamp.isoformat()
    return timestamp


def collect_attributes_from_wp_and_wd(itempage, languages, wd_parameters,
                                      include_literals=True,
                                      raise_on_no_wikipage=True,
                                      include_attribute_labels=True,
                                      require_country=True,
                                      include_wikipedia=True,
                                      delay_wikipedia_retrieval=False):
    """

    :param itempage: ItemPage from which to collect information
    :param languages: list of languages in which to include literals
            and Wikipedia information (2-character{} ISO codes).
    :param wd_parameters: list of wikidata properties (Pxxx codes) to be
            included, if present
    :param include_literals: Include properties and alternate names. If
            false, only labels are
            included.
    :param raise_on_no_wikipage: Controls whether an error is raised when
            no Wikipedia page in any of the requested languages can be
            identified for this entity. If True (default), no further meta-
            data about such entities is collected from WikiData. If False,
            meta-data is still collected.
    :param require_country: attempt to deduce country attribute from location
            attributes (requires additional API call(s))
    :param include_wikipedia: Include information from Wikipedia pages
            on entity (summary, revision id & timestamp, exact url)
    :param delay_wikipedia_retrieval: Return only the sitelinks of existing
            Wikipedia pages in the relevant languages (True) or make a call
            to the Wikipedia API directly (False). The default `False` makes
            for fairly expensive operations, where possible, True should be
            used.
    :returns: a dictionary of the collected details about this entity from
            both Wikipedia and Wikidata.
    """
    timestamp = get_wikidata_timestamp(itempage)

    itempage.get()
    # collect summaries and meta-info from the Wikipedia pages in the relevant
    # languages:
    wikipedia_data = []
    if include_wikipedia:
        try:
            sitelinks = itempage.text['sitelinks']
        except (KeyError, AttributeError):
            sitelinks = itempage.sitelinks
        if delay_wikipedia_retrieval:
            wikipedia_data = {title: sitelinks[title] for title in sitelinks if
                              any([title == lang + 'wiki' for lang in
                                   languages])}
        else:
            try:
                wikipedia_data = wp_summary_from_wdid(itempage.id,
                                                      languages=languages,
                                                      sitelinks=sitelinks)
            except (RedirectError, DisambiguationError):
                raise ValueError
            except requests.exceptions.ConnectionError:
                pass
        if not wikipedia_data:
            if raise_on_no_wikipage:
                raise ValueError
            else:
                pass

    # use the Wikipedia article in the first language found as the entity's
    # unique preferred `url` - the order of languages is meaningful!
    try:
        entity_extracted_details = {'url': wikipedia_data[0]['url']}
    except (KeyError, IndexError):
        # fallback to Wikidata ID if no Wikipedia page has been retrieved (yet)
        entity_extracted_details = {
            'url': 'https://www.wikidata.org/wiki/' + itempage.id}
    if delay_wikipedia_retrieval:
        entity_extracted_details.update(wikipedia_data)
    else:
        for language in wikipedia_data:
            entity_extracted_details[language['language'] + 'wiki'] = language

    # get selected attributes from WikiData
    entity = ParseItemPage(itempage, include_literals=include_literals,
                           claims_of_interest=wd_parameters,
                           languages=languages,
                           include_attribute_labels=include_attribute_labels,
                           require_country=require_country)
    entity_extracted_details.update(entity.details)
    entity_extracted_details['wikidata_id'] = itempage.id

    entity_extracted_details['wikidata_timestamp'] = timestamp

    return entity_extracted_details


def collect_entities_iterative(limit_per_query, n_queries, wd_parameters,
                               include_literals, entity_type, languages,
                               raise_on_missing_wikipedias=False,
                               id_only=False,
                               include_attribute_labels=True,
                               require_country=True,
                               include_wikipedia=True,
                               delay_wikipedia_retrieval=True
                               ):
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

            except StopIteration:
                break
            if id_only:
                yield entity_raw.id
                continue

            try:
                yield collect_attributes_from_wp_and_wd(
                    entity_raw,
                    languages=languages,
                    wd_parameters=wd_parameters,
                    include_literals=include_literals,
                    include_attribute_labels=include_attribute_labels,
                    require_country=require_country,
                    include_wikipedia=include_wikipedia,
                    delay_wikipedia_retrieval=delay_wikipedia_retrieval)
            except ValueError:  # this probably means no Wikipedia page in
                # any of our languages. We have no use for such entities.
                if raise_on_missing_wikipedias:
                    raise ValueError('No information about this entity found!')
                continue

# if __name__ == '__main__':
#     import pprint
#     from eWRT.ws.wikidata.wp_to_wd import wikidata_from_wptitle
#
#     obama = wikidata_from_wptitle('Barrack Obama')
#     wd_parameters = [
#         'P18',  # image
#         'P17',  # country
#         'P19',  # place of birth
#         'P39',  # position held
#         'P569',  # date of birth
#         'P570',  # date of death
#         'P1411'  # nominated for
#     ]
#     pprint.pprint(collect_attributes_from_wp_and_wd(obama,
#                                                     languages=['de', 'en',
#                                                                'hr'],
#                                                     wd_parameters=wd_parameters,
#                                                     include_literals=False))
