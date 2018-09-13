#!/usr/bin/python
import datetime
import ujson
import warnings
from urllib2 import urlopen

import pywikibot.pagegenerators
import wikipedia
import wikipedia_wl
from eWRT.ws.wikidata.wikidata_attributes import ParseEntity

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

RELEVANT_LANGUAGES = ['en', 'de', 'fr', 'es']

WIKIDATA_SITE = pywikibot.Site("wikidata", "wikidata")

JONAS_TYPE = 'entity_matview'


def wp_summary_from_wdid(wikidata_id, languages=None):
    """
    :param wikidata_id: Qxxx-ID of the entity in Wikidata's ontology
    :type wikidata_id: str
    :param languages: list of language ISO codes, in order of preference
    :type languages
    :return: list with one dictionary per language for which a Wikipedia
    page about this entity exists, each containing the link, summary, title,
    revision id and revision timestamp
    """
    if not languages:
        languages = RELEVANT_LANGUAGES
    has_page = False
    wikipedia_data = []
    page = urlopen(
        url=("https://www.wikidata.org/w/api.php?action=wbgetentities&"
             "format=json&props=sitelinks&ids={}&sitefilter={}".format(
            wikidata_id, '|'.join([language + 'wiki' for language in languages]))
        )
    )

    page_content = ujson.loads(page.read())
    for language in languages:
        language_page = {'language': language}
        wikipedia.set_lang(language)

        try:
            wikipage_title = page_content['entities'][wikidata_id]['sitelinks'][language + 'wiki'][
                'title']

            try:
                wikipage = wikipedia_wl.page(wikipage_title, auto_suggest=False, redirect=False)
            except wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError:
                warnings.warn('No wikipedia page found in language {language} for '
                              'entity {entity}!.'.format(language=language, entity=wikidata_id))
                continue
            language_page['revision'] = wikipage.revision_id
            language_page['summary'] = wikipage.summary
            language_page['url'] = wikipage.url
            language_page['title'] = wikipage.title
            try:
                language_page['timestamp'] = wikipage.revision_timestamp
            except KeyError:
                language_page['timestamp'] = None
            has_page = True
            wikipedia_data.append(language_page)
            # logger.debug(u'Parsed entity {}\'s {}wiki site {}.'.format(wikidata_id, language,
            #                                                            wikipage_title))
        except KeyError:
            continue
    if has_page:
        return wikipedia_data
    else:
        warnings.warn('No Wikipedia page found in any of the requested languages for '
                      'item {}!'.format(wikidata_id))
        return None


def collect_entities_iterative(limit_per_query, n_queries, wd_parameters,
                               include_literals, entity_type, languages):
    """
    :param languages: list if languages (ISO codes)
    :param entity_type: type of entity ('person', 'organization' or 'geo')
    :param include_literals: include 'aliases' and 'descriptions' (bool)
    :type include_literals: bool
    :param wd_parameters: list of wikidata properties to include in result
    :param limit_per_query: LIMIT set in the SPARQL query
    :type limit_per_query: int
    :param n_queries: maximum number of subsequent queries
    :type n_queries: int
    :type wd_parameters: list
    :returns: RawDocument
    """

    for i in range(n_queries):
        wikidata_site = WIKIDATA_SITE
        query = QUERY % (ENTITY_TYPE_IDENTIFIERS[entity_type], limit_per_query, limit_per_query * i)
        # logger.debug('Query is\n' + query)
        generator = pywikibot.pagegenerators.WikidataSPARQLPageGenerator(query, site=wikidata_site)
        if not generator:
            continue
        # parsed_entities = []
        for j in range(limit_per_query):
            try:
                entity_raw = generator.next()

            except StopIteration:
                break
            wikipedia_data = wp_summary_from_wdid(entity_raw.id, languages=languages)
            if not wikipedia_data:
                continue
            entity_extracted_details = {'url': wikipedia_data[0]['url']}
            for language in wikipedia_data:
                entity_extracted_details[language['language'] + 'wiki'] = language

            entity = ParseEntity(entity_raw, claims_of_interest=wd_parameters,
                                 include_literals=include_literals, entity_type=entity_type)
            for key in entity.details:
                entity_extracted_details[key] = entity.details[key]
            entity_extracted_details['wikidata_id'] = entity_raw.id
            entity_extracted_details['entityType'] = entity_type.capitalize() + 'Entity'
            # parsed_entities.append(entity_extracted_details)

            yield entity_extracted_details
