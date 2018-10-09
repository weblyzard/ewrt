#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on October 09, 2018

@author: jakob <jakob.steixner@modul.ac.at>
'''

import warnings

from eWRT.ws.wikidata.enrich_from_wikipedia import \
    wikipedia_page_info_from_title
from eWRT.ws.wikidata.filters import filter_result


def collect_multiple_from_wikipedia(sitelinks_cache, entities_cache,
                                    batchsize=20):
    """Request details about a list of titles from Wikipedia and
    update the cached entities with the result.
    :param sitelinks_cache: a dictionary of the format
        {
            language1: {
                        wikipedia_page_title1: wikidata_ID,
                        wikipedia_page_title2: wikidata_ID
                    }
            language2: {}
            #...
        }
    :param entities_cache: a dictionary of retrieved entities' meta_information,
        not including the data from Wikipedia yet to be collected. Keys are
        Wikidata IDs."""
    wikipedia_sitelinks_to_retrieve = sitelinks_cache
    for entry in wikipedia_request_dispatcher(
            wikipedia_sitelinks_to_retrieve,
            entity_cache=entities_cache,
            batch_size=batchsize):
        yield entry


def batch_enrich_from_wikipedia(wikipedia_pages, language, entities_cache):
    """
    Postprocess Wikidata results by complementing them with Wikipedia data.

    :param wikipedia_pages: dictionary of Wikipedia page titles in a
        particular language and the Wikidata entities' IDs they're about.
    :type wikipedia_pages: dict
    :param language: language ISO code
    :type language: str
    :param entities_cache: Stored entities with their info as retrieved from
        Wikidata to be supplemented with Wikipedia info.
    :type entities_cache: dict
    :param batchsize:
    :return:
    """
    batch = wikipedia_pages
    titles = '|'.join(batch.keys())
    try:
        retrieved_pages = wikipedia_page_info_from_title(titles,
                                                         language)
    except StopIteration:
        raise IndexError

    try:
        assert retrieved_pages
    except AssertionError:
        raise IndexError(
            'No Wikipedia pages to retrieve in language {}!'.format(
                language))
    counter_retrieved = 0
    for page in retrieved_pages:
        try:
            output_formatted_entity = {'language': language}
            title = page['title']
            wikidata_url = wikipedia_pages[title]
            wikibot_result = entities_cache[wikidata_url]
            assert wikibot_result[language + 'wiki'] == title
            output_formatted_entity.update(
                filter_result(language, entities_cache[wikidata_url]))

            output_formatted_entity[
                language + 'wiki'] = page
            counter_retrieved += 1
            yield output_formatted_entity
        except (KeyError, AssertionError) as e:
            warnings.warn('Failed to map retrieved Wikipedia info back '
                          'to cached entity: {}'.format(e)
                          )
    if not counter_retrieved:
        raise IndexError(
            'Failed to map any Wikipedia page infos in language {}'
            ' back to Wikidata entities, encoding issue?'.format(language))


def wikipedia_request_dispatcher(sitelinks_cache, entity_cache, languages=None,
                                 batch_size=20):
    """
    Split a large dict of Wikipedia sitelinks to pages about entities about
    which information has been retrieved from Wikidata into smaller chunks
    to be handled as batch queries to Wikipedia.

    :param sitelinks_cache:
    :param entity_cache:
    :param languages: If left blank, the sitelinks cache is assumed to already
        contain all and only the languages needed. If stated explicitly, 0
        results in any of the the requested languages leads to a ValueError.
    :param batch_size: The number of titles that will be included in Wikipedia
        query. The maximum is 50, but queries with more than ~20 titles will
        usually contain truncated results (e. g. without abstracts) for a number
        of titles and require a second call anyway.
    :
    : None
    """
    if not languages:
        languages = [l for l in sitelinks_cache]
    for language in languages:
        print('processing ' + language)
        try:
            assert language in sitelinks_cache and sitelinks_cache[language]
        except AssertionError:
            raise StopIteration(
                'No sitelinks found for language {}.'.format(language))
        total_sitelinks = sitelinks_cache[language]
        sitelink_list = total_sitelinks.keys()
        n_sitelinks = len(total_sitelinks)
        print('{} links in language {}'.format(n_sitelinks, language))
        steps = n_sitelinks // batch_size
        if not steps:
            steps = 1
        for step in range(steps):
            lower_limit, upperlimit = batch_size * step, batch_size * (step + 1)
            batch = {key: total_sitelinks[key] for key in
                     sitelink_list[lower_limit:upperlimit]}
            for result in batch_enrich_from_wikipedia(wikipedia_pages=batch,
                                                      language=language,
                                                      entities_cache=entity_cache):
                yield result
