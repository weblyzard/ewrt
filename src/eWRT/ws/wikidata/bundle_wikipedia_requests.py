#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on October 09, 2018

@author: jakob <jakob.steixner@modul.ac.at>

Add Wikipedia information to a batch of skeleton entities with with Wikidata
metadata and literals only.
'''

import warnings

from eWRT.ws.wikidata.enrich_from_wikipedia import \
    wikipedia_page_info_from_titles
from eWRT.ws.wikidata.language_filters import filter_result


def collect_multiple_from_wikipedia(sitelinks_cache, entities_cache,
                                    batchsize=20, return_type='merged'):
    """Request details about a list of titles from Wikipedia and
    update the cached entities with the result.
    :param batchsize: number of titles to be queried from Wikipedia, per query.
    :type batchsize: int
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
        Wikidata IDs.
    :type entities_cache: dict
    :returns: iterator with wikipedia info about entities (dicts)"""
    wikipedia_sitelinks_to_retrieve = sitelinks_cache
    for entry in wikipedia_request_dispatcher(
            wikipedia_sitelinks_to_retrieve,
            entity_cache=entities_cache,
            batch_size=batchsize,
            return_type=return_type):
        yield entry


def batch_enrich_from_wikipedia(wikipedia_pages, language, entities_cache,
                                return_type='merged'):
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
    :return: iterator of Wikipedia-enriched entities in a single language
    :rtype: Iterator[dict]
    """
    batch = wikipedia_pages
    titles = '|'.join(batch.keys())
    try:
        retrieved_pages = list(wikipedia_page_info_from_titles(titles,
                                                               language))
    except StopIteration:
        raise IndexError

    try:
        assert retrieved_pages
    except AssertionError:
        raise IndexError(
            'No Wikipedia pages to retrieve in language {}!'.format(
                language))
    for page in retrieved_pages:

        try:
            title = page['title']
            wikidata_url = wikipedia_pages[title]
            wikibot_result = entities_cache[wikidata_url]
            if return_type == 'merged':
                yield (merge_wikipedia_and_wikidata(wikibot_result=wikibot_result,
                                                    wikipedia_result=page,
                                                    language=language))

            elif return_type == 'keep_raw_results':
                yield {'wikidata': wikibot_result, language + 'wiki': page}

        except ValueError as e:
            warnings.warn('Failed to map retrieved Wikipedia info back '
                          'to cached entity: {}'.format(e)
                          )


def merge_wikipedia_and_wikidata(wikibot_result, wikipedia_result, language):
        title = wikipedia_result['title']
        assert wikibot_result[language + 'wiki'] == title

        output_formatted_entity = {'language': language}
        output_formatted_entity.update(
            filter_result(language, wikibot_result))

        output_formatted_entity[
            language + 'wiki'] = wikipedia_result
        return output_formatted_entity


def wikipedia_request_dispatcher(sitelinks_cache, entity_cache, languages=None,
                                 batch_size=20, return_type='merged'):
    """
    Split a large dict of Wikipedia sitelinks to pages about entities about
    which information has been retrieved from Wikidata into smaller chunks
    to be handled as batch queries to Wikipedia.

    :param sitelinks_cache: dict of format {<language0>: {<wikipedia title in
        language1>: <wikidata url of entity>}}
    :type sitelinks_cache: dict
    :param entity_cache: dict of format {<wikidata url of entity>: <parsed content>}
    :type entity_cache: dict
    :param languages: If left blank, the sitelinks cache is assumed to already
        contain all and only the languages needed. If stated explicitly, 0
        results in any of the the requested languages leads to a ValueError.
    :type languages: list
    :param batch_size: The number of titles that will be included in Wikipedia
        query. The maximum is 50, but queries with more than ~20 titles will
        usually contain truncated results (e. g. without abstracts) for a number
        of titles and require a second call anyway.
    :type batch_size: int
    :returns: Iterator of monolingual entity dicts with Wikidata and Wikipedia
        data combined.
    :rtype: Iterator[dict]
    """
    if not languages:
        languages = [l for l in sitelinks_cache]

    if return_type == 'keep_raw_results':
        output = {}
    for language in languages:
        print('processing ' + language)
        counter_retrieved = 0
        try:
            assert language in sitelinks_cache and sitelinks_cache[language]
        except AssertionError:
            continue
        total_sitelinks = sitelinks_cache[language]
        sitelink_list = total_sitelinks.keys()
        n_sitelinks = len(total_sitelinks)
        print('{} links in language {}'.format(n_sitelinks, language))
        steps = (n_sitelinks - 1) // batch_size + 1
        for step in range(steps):
            lower_limit, upperlimit = batch_size * step, batch_size * (step + 1)
            batch = {key: total_sitelinks[key] for key in
                     sitelink_list[lower_limit:upperlimit]}
            for result in batch_enrich_from_wikipedia(
                    wikipedia_pages=batch,
                    language=language,
                    entities_cache=entity_cache,
                    return_type=return_type):
                if return_type == 'merged':
                    result['language'] = language
                    yield result
                elif return_type == 'keep_raw_results':
                    target_key = result['wikidata']['wikidata_id']
                    try:

                        output[target_key][language + 'wiki'] = \
                            result[language + 'wiki']
                    except KeyError:
                        output[target_key] = result
                counter_retrieved += 1
        print('successfully_retrieved {} entries in language {}.'.format(
            counter_retrieved, language
        ))
        if not counter_retrieved:
            warnings.warn(
                'Failed to map any Wikipedia page infos in language {}'
                ' back to Wikidata entities, encoding issue?'.format(language))

    if return_type == 'keep_raw_results':
        for wikidata_id, unmerged_result in output.items():
            yield unmerged_result
