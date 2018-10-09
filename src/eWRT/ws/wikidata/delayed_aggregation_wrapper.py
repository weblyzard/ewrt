#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on October 09, 2018

@author: jakob <jakob.steixner@modul.ac.at>


'''

import datetime
import logging

from collections import OrderedDict
from eWRT.ws.wikidata.bundle_wikipedia_requests import \
    collect_multiple_from_wikipedia
from eWRT.ws.wikidata.extract_meta import WikidataEntityIterator

logger = logging.Logger(name='wp_bundler')


def collect_entities_delayed(entity_types,
                             retrieval_mode,
                             num_queries=1,
                             languages=['en'],
                             limit_per_query=None,
                             include_literals=True,
                             wikidata_fields=None,
                             delay_wikipedia_retrieval=True,
                             include_attribute_labels=False,
                             require_country=False,
                             include_wikipedia=True,
                             debug=False,
                             memory_saving_limit=500):
    """

    :param entity_types: dict/Ordered dict of entity types
    :param retrieval_mode: read entities from API or dumped file.
    :param num_queries: number of subsequent queries, with automatic offset
        (only used with retrieval mode API)
    :param languages: list of languages (ISO code)
    :param limit_per_query: limit
    :param include_literals:
    :param wikidata_fields:
    :param delay_wikipedia_retrieval:
    :param include_attribute_labels:
    :param require_country:
    :param include_wikipedia:
    :param debug:
    :param memory_saving_limit:
    :return:
    """
    relevant_entity_types = OrderedDict(
        [(entity_type, entity_types[entity_type]) for entity_type in
         entity_types])
    iterator = WikidataEntityIterator(relevant_entity_types)
    if retrieval_mode == 'API':
        collect_entities_iterative = iterator.collect_entities_iterative
    elif retrieval_mode == 'bz_dump':
        collect_entities_iterative = iterator.collect_entities_from_dump
        num_queries = 1  # starting a query with an offset is undefined for
        # dump mode, multiple queries would thus just produce the same
        # result over again.
    elif retrieval_mode == 'expanded_dump':
        raise NotImplementedError('Please use the uninflated dump (.bz2)!')
    else:
        raise NotImplementedError('Supported modes are: API and bz_dump!')
    for n in range(num_queries):
        wikipedia_sitelinks_to_retrieve = {lang: {} for lang in languages}
        entities_retrieved = {}
        for idx, entity_data in enumerate(collect_entities_iterative(
                limit_per_query=limit_per_query,
                n_queries=num_queries,
                wd_parameters=wikidata_fields,
                include_literals=include_literals,
                languages=languages,
                delay_wikipedia_retrieval=delay_wikipedia_retrieval,
                include_attribute_labels=include_attribute_labels,
                require_country=require_country,
                include_wikipedia=include_wikipedia)):
            if delay_wikipedia_retrieval and include_wikipedia:
                for lang in languages:
                    try:
                        wikipedia_sitelinks_to_retrieve[lang][
                            entity_data[lang + 'wiki']] = entity_data['url']
                    except KeyError:
                        pass
                entities_retrieved[entity_data['url']] = entity_data
            if delay_wikipedia_retrieval and include_wikipedia and (
                    idx + 1) % memory_saving_limit == 0:
                if debug:
                    logger.debug(datetime.datetime.now().isoformat())
                    logger.debug('retrieving data from wikipedia')
                    logger.debug(
                        '; '.join(['{} entries in language {}'.format(language,
                                                                      len(
                                                                          wikipedia_sitelinks_to_retrieve[
                                                                              language]))
                                   for language in
                                   wikipedia_sitelinks_to_retrieve])
                    )
                for merged_result in collect_multiple_from_wikipedia(
                        wikipedia_sitelinks_to_retrieve,
                        entities_retrieved):
                    yield merged_result
                    continue
            elif not delay_wikipedia_retrieval:
                yield entity_data

        for merged_result in collect_multiple_from_wikipedia(
                wikipedia_sitelinks_to_retrieve,
                entities_retrieved):
            yield merged_result
