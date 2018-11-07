#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on September 13, 2018

@author: Jakob Steixner, <jakob.steixner@modul.ac.at

Loop through the entities of a relevant type either directly through the
API with pywikibot.pagegenerators, or using a dump file (faster).

'''

import sys
import ujson
import warnings
from collections import OrderedDict

import pywikibot.pagegenerators
import requests
from bz2file import BZ2File
from eWRT.ws.wikidata.enrich_from_wikipedia import wp_summary_from_wdid
from eWRT.ws.wikidata.language_filters import filter_result
from eWRT.ws.wikidata.wikibot_parse_item import (ParseItemPage,
                                                 get_wikidata_timestamp,
                                                 DoesNotMatchFilterError)
from lxml import etree as et
from wikipedia import RedirectError, DisambiguationError

ENTITY_TYPES = ['organization', 'person', 'geo']

QUERY = """SELECT ?item WHERE{
  ?item wdt:P31|wdt:P279* wd:%s .
 }
"""

WIKIDATA_SITE = pywikibot.Site("wikidata", "wikidata")


def merge_with_wikipedia_by_language(entity, languages=['en']):
    for language in languages:
        if language + 'wiki' in entity:
            monolingual_result = filter_result(
                language=language,
                raw_result=entity)
            monolingual_result[
                'language'] = language
            yield monolingual_result


def collect_attributes_from_wp_and_wd(itempage, languages,
                                      include_wikipedia=False,
                                      raise_on_no_wikipage=False,
                                      delay_wikipedia_retrieval=False,
                                      entity_type=None,
                                      **kwargs):
    """

    :param itempage: ItemPage from which to collect information
    :param languages: list of languages in which to include literals
            and Wikipedia information (2-character{} ISO codes).
    :param raise_on_no_wikipage: Controls whether an error is raised when
            no Wikipedia page in any of the requested languages can be
            identified for this entity. If True (default), no further meta-
            data about such entities is collected from WikiData. If False,
            meta-data is still collected.
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

    if hasattr(itempage, 'text'):
        id = itempage.id
        try:
            timestamp = get_wikidata_timestamp(itempage)
        except AttributeError:
            pass
        itempage = itempage.text
        itempage.update({'id': id, 'timestamp': timestamp})

    wikipedia_data = []
    if include_wikipedia:
        sitelinks = itempage['sitelinks']
        relevant_sitelinks = [wiki for wiki in sitelinks if
                              any([lang + 'wiki' == wiki for lang in
                                   languages])]
        try:
            sitelinks = [wiki['title'] for wiki in relevant_sitelinks]
        except TypeError:
            pass

        if not sitelinks:
            if raise_on_no_wikipage:
                raise ValueError
            else:
                pass

        if delay_wikipedia_retrieval:
            wikipedia_data = {wiki: sitelinks[wiki] for wiki in
                              relevant_sitelinks}
            try:
                wikipedia_data = {wiki: wikipedia_data[wiki]['title'] for wiki
                                  in wikipedia_data}
            except TypeError:
                pass

        elif sitelinks:
            try:
                wikipedia_data = wp_summary_from_wdid(itempage['id'],
                                                      languages=languages,
                                                      sitelinks=sitelinks)

            except (RedirectError, DisambiguationError):
                raise ValueError
            except requests.exceptions.ConnectionError:
                warnings.warn('Failed to get info about entity {} from '
                              'Wikipedia API!'.format(itempage['id']))

    try:
        entity_extracted_details = {'url': wikipedia_data[0]['url']}
    except (KeyError, IndexError):
        # fallback to Wikidata ID if no Wikipedia page has been retrieved (yet)
        entity_extracted_details = {
            'url': 'https://www.wikidata.org/wiki/' + itempage['id']}
    if delay_wikipedia_retrieval:
        entity_extracted_details.update(wikipedia_data)
    elif include_wikipedia:
        for language in wikipedia_data:
            entity_extracted_details[language['language'] + 'wiki'] = language

    try:
        entity = ParseItemPage(
            itempage, languages=languages, entity_type=entity_type,
            **kwargs)
    except AssertionError:
        raise ValueError(
            'No attributes of interest identified for entity{}'.format(
                itempage['id']))
    except DoesNotMatchFilterError:
        raise DoesNotMatchFilterError(
            'entity {} does not match filter criteria'.format(
                itempage['id']
            ))
    entity_extracted_details.update(entity.details)
    if include_wikipedia and not delay_wikipedia_retrieval:
        for language_result in merge_with_wikipedia_by_language(
                entity=entity_extracted_details,
                languages=languages):
            yield language_result
    else:
        yield entity_extracted_details


class WikidataEntityIterator:
    """
    Iterates over a collection of Wikidata entities either from dump (xml
    with embedded json) or as a pywikikibot.pagegenerator.
    """
    type_root_identifiers = {
        'event': 'Q1190554',  # labelled 'occurence' in WikiData
        'geo': 'Q2221906',
        'organization': 'Q43229',
        'person': 'Q5'
    }

    def __init__(self, top_level_categories=None, lazy_load_subclasses=True,
                 dump_path=None):
        """
        :param top_level_categories: dict
        :param lazy_load_subclasses: Do (not) load subclass-to-superclass
            mappings until needed
        :param dump_path:
        """

        self.dump_path = dump_path

        if not top_level_categories:
            top_level_categories = self.type_root_identifiers
        elif isinstance(top_level_categories, (dict, OrderedDict)):
            pass
        else:
            try:
                top_level_categories = {cat: self.type_root_identifiers[cat] for
                                        cat in top_level_categories}
            except KeyError as e:
                raise ValueError(
                    'Category with undefined defaults: {}'.format(e))
        self.entity_types = top_level_categories
        self.all_relevant_categories = []
        if not lazy_load_subclasses:

            self.all_relevant_categories = self.get_relevant_category_ids(
                top_level_categories)
        elif self.entity_types.keys() == ['person']:
            self.relevant_categories = {'person': 'Q5'}
            self.all_relevant_categories = self.relevant_categories

    def get_relevant_category_ids(self, top_level_categories=None):
        """
        Get a complete up to date
        :param top_level_categories: dictionary of top level categories by their
            English label, and their Qxxx identifier. If None, use the class
            defaults
        :type top_level_categories: dict
        :return: set of categories that are (transitively) defined as subclasses
            of either of the top level categories in 'top_level_categories'
        :rtype: frozenset
        """
        if not self.entity_types:
            self.entity_types = top_level_categories
            self.all_relevant_categories = self.get_relevant_category_ids(
                self.entity_types)
        if top_level_categories is None:
            top_level_categories = self.type_root_identifiers
        all_relevant_categories = frozenset()
        self.relevant_categories = OrderedDict()
        for label in top_level_categories:
            try:
                subclasses = self.type_subclasses(label)
                all_relevant_categories = all_relevant_categories | frozenset(
                    subclasses)
                self.relevant_categories[label] = subclasses
            except KeyError as e:
                raise ValueError(
                    'Nothing found for category {}: {}'.format(label, e))

        # all_relevant_categories = (
        #         frozenset(type_subclasses('event')) |
        #         frozenset(type_subclasses('human')) |
        #         frozenset(type_subclasses('geographical location')) |
        #         frozenset(type_subclasses('organization')))
        return all_relevant_categories

    def type_subclasses(self, parent_class_label):
        """
        :param parent_class_label: English label of the parent class (needs to
            defined in type_root_identifiers)
        :type parent_class_label: basestring
        :return: list of ids of parent class's subclasses
        :rtype: list
        """
        subclass_query = """SELECT ?item WHERE {
          ?item wdt:P279* wd:%s .
          }"""
        try:
            res = pywikibot.pagegenerators.WikidataSPARQLPageGenerator(
                query=subclass_query % self.entity_types[
                    parent_class_label])
        except KeyError:
            raise KeyError(
                'Undefined parent type label, needs to be one of {}'.format(
                    [name for name in self.type_root_identifiers]))
        res = list([item.id for item in res])
        return res

    def collect_entities_from_dump(self,
                                   limit_per_query,  # for consistent API
                                   n_queries=None,
                                   # no effect, for consistent API only

                                   include_wikipedia=True,
                                   delay_wikipedia_retrieval=True,
                                   pre_filter=None,
                                   return_type=None,
                                   **kwargs
                                   ):
        """
        iteratively parse a xml-dump (with embedded json entities) for entities
        of interest, using bz2file.
        Note: the pure JSON does not contain all relevant meta-info (e. g.
        timestamps and revision IDs)
        :param pre_filter:
        :param n_queries:
        :param limit_per_query: maximum items to be read in (for debugging/testing)
        :type limit_per_query: int
        :return: list of entities to be updated
        :rtype: list
        """
        if self.dump_path is None:
            raise ValueError('Dump path required!')

        if pre_filter is None:
            pre_filter = [(lambda entity, entity_type: True, {})]

        def best_guess_open(file_name):
            """
            Use bz2file to iterate over a compressed file,
            regular open otherwise."""
            if file_name.endswith('.bz2'):
                return BZ2File(file_name)
            else:
                return open(file_name)

        dump_path = self.dump_path
        if not self.all_relevant_categories:
            self.all_relevant_categories = self.get_relevant_category_ids(
                self.entity_types)
        with best_guess_open(dump_path) as xml_file:

            parser = et.iterparse(xml_file, events=('end',))
            try:
                for events, elem in parser:
                    if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}timestamp':
                        timestamp = elem.text
                    elif elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}text':

                        if not elem.text:
                            del elem
                            del events
                            continue

                        try:
                            elem_content = ujson.loads(elem.text)
                            assert isinstance(elem_content, dict)
                        except (ValueError, AssertionError):
                            del elem
                            del events
                            continue
                        try:
                            elem_content['timestamp'] = timestamp
                            del timestamp
                        except NameError:
                            warnings.warn('Item {} cannot be assigned a '
                                          'timestamp!'.format(
                                elem_content['id']
                            ))
                        try:
                            category = self.determine_relevant_category(
                                elem_content)
                            assert category
                        except (ValueError,  # if the JSON is empty
                                AssertionError
                                # if the entity doesn't fit search categories
                                ):
                            del elem
                            del events
                            continue
                        pre_filter_result = all(
                            [filter_function(entity=elem_content, entity_type=category,  **filter_params)
                             for filter_function, filter_params in pre_filter]
                        )
                        if pre_filter_result:
                            try:
                                for entity in collect_attributes_from_wp_and_wd(
                                        elem_content,
                                        include_wikipedia=include_wikipedia,
                                        delay_wikipedia_retrieval=True,
                                        entity_type=category,
                                        **kwargs):
                                    entity['category'] = category
                                    if include_wikipedia and not delay_wikipedia_retrieval:
                                        for language_result in merge_with_wikipedia_by_language(
                                                entity=entity,
                                                languages=kwargs['languages']):
                                            yield language_result
                                    else:
                                        yield entity

                            except (DoesNotMatchFilterError, ValueError) as e:
                                # this probably means no
                                # Wikipedia page in any of our languages, or
                                # failute to mach filter criteria
                                # have no use for such entities.
                                del elem
                                del events
                                continue

                    del elem
                    del events
            except (EOFError, IOError) as e:
                warnings.warn('Error parsing file {}: {}'.format(dump_path, e))


    def determine_relevant_category(self, elem_content):
        """
        Determine whether and which category we are after a detected entity
        belongs to. The categories are stored in an ordered dict, so if an
        entity belongs to several categories, it will be parsed as only one,
        the first one. Example: geo-political entities are both organizations
        and locations, but parsed only as one or the other depending on
        the order self.relevant_categories.
        :param elem_content: A raw entity dict as retrieved from Wikidata's JSON
        :type elem_content: dict
        :return: boolean whether entity fits any of the searched for categories
        :rtype: bool
        :raises ValueError (if JSON is parsed as (empty) list
        """
        try:
            try:
                types = elem_content['claims']['P31']
                for entity_type in self.relevant_categories:
                    categories = [
                        category['mainsnak']['datavalue']['value']['id'] for
                        category in types]
                    if any([category in self.relevant_categories[entity_type]
                            for category in categories]):
                        return entity_type
                return None
            except TypeError:
                # print(type(elem_content))
                del elem_content
                raise ValueError

        except KeyError as e:
            # this probably means that we're dealing with an
            # abstract entity/category that may be a 'subclass' but
            # not an 'instance of' anything else
            raise ValueError('Does not appear to be a correctly '
                             'formatted entity!')

    def collect_entities_iterative(self, limit_per_query, n_queries,
                                   raise_on_missing_wikipedias=False,
                                   id_only=False,
                                   **kwargs):
        """Get a list of entities with pywikibot.pagegenerators

        :param raise_on_missing_wikipedias: raise ValueError
        :param id_only: option to retrieve only ID without parsing entity
        :type id_only: bool
        :param limit_per_query: LIMIT set in the SPARQL query
        :type limit_per_query: int
        :param n_queries: maximum number of subsequent queries
        :type n_queries: int
        """
        for entity_type in self.entity_types:
            for i in range(n_queries + 1):
                wikidata_site = WIKIDATA_SITE
                query = QUERY % (self.entity_types[entity_type])
                if limit_per_query:
                    query = query + '\nLIMIT {}\nOFFSET{}'.format(
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
                        for result in collect_attributes_from_wp_and_wd(
                                entity_raw, **kwargs):
                            result['category'] = entity_type
                            yield result

                    except ValueError:  # this probably means no Wikipedia page in
                        # any of our languages. We have no use for such entities.
                        if raise_on_missing_wikipedias:
                            raise ValueError(
                                'No information about this entity found!')
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
