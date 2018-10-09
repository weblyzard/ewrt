#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on September 13, 2018

@author: Jakob Steixner, <jakob.steixner@modul.ac.at

Loop

'''

import sys
import ujson
import requests
import pywikibot.pagegenerators

from collections import OrderedDict
from bz2file import BZ2File
from lxml import etree as et
from wikipedia import RedirectError, DisambiguationError
from eWRT.ws.wikidata.enrich_from_wikipedia import wp_summary_from_wdid
from eWRT.ws.wikidata.wikibot_parse_item import ParseItemPage

ENTITY_TYPE_IDENTIFIERS = {
    'person': 'Q5',
    'organization': 'Q43229',
    'geo': 'Q2221906',

}

ENTITY_TYPES = ['organization', 'person', 'geo']

QUERY = """SELECT ?item WHERE{
  ?item wdt:P31|wdt:P279* wd:%s .
 }
"""

WIKIDATA_SITE = pywikibot.Site("wikidata", "wikidata")


def get_wikidata_timestamp(item_page):
    # ItemPages come in two slightly different formats depending on how
    # they were created (probably a bug in pywikibot). We want to be able to
    # deal with both:
    try:
        timestamp = item_page['timestamp']
    except:
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
    if isinstance(itempage, dict):
        import mock
        new_itempage = mock.Mock()
        new_itempage.id = itempage['id']
        new_itempage.timestamp = itempage['timestamp']
        new_itempage.sitelinks = itempage['sitelinks']
        new_itempage.claims = itempage['claims']
        new_itempage.text = itempage
        itempage = new_itempage
    timestamp = get_wikidata_timestamp(itempage)
    #
    # itempage.get()
    # collect summaries and meta-info from the Wikipedia pages in the relevant
    # languages:
    wikipedia_data = []
    if include_wikipedia:
        try:
            sitelinks = itempage.text['sitelinks']
        except (KeyError):
            sitelinks = itempage.sitelinks
        except AttributeError:
            sitelinks = itempage['sitelinks']
        relevant_sitelinks = [wiki for wiki in sitelinks if
                              any([lang + 'wiki' == wiki for lang in
                                   languages])]
        try:
            sitelinks = [wiki['title'] for wiki in relevant_sitelinks]
        except TypeError:
            pass

        if delay_wikipedia_retrieval:
            wikipedia_data = {wiki: sitelinks[wiki] for wiki in
                              relevant_sitelinks}
            try:
                wikipedia_data = {wiki: wikipedia_data[wiki]['title'] for wiki
                                  in wikipedia_data}
            except TypeError:
                pass
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
    elif include_wikipedia:
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

    def __init__(self, top_level_categories=None, lazy_load_subclasses=True):
        # todo: enable to iterate over a single file (dump mode) once
        # while sorting the entities into their different entity types
        if not top_level_categories:
            top_level_categories = self.type_root_identifiers
        elif isinstance(top_level_categories, dict):
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
        elif set(self.entity_types) == set(('person')):
            self.relevant_categories = {'person': 'Q5'}

    def get_relevant_category_ids(self, top_level_categories=None):
        """
        Get a complete up to date
        :param top_level_categories: dictionary of top level categories by their
            English label, and their Qxxx identifier
        :return: set of categories that are (transitively) defined as subclasses
            of either of the top level categories in 'top_level_categories'
        :rtype: frozenset
        """
        if not self.entity_types:
            self.entity_types = top_level_categories
            self.all_relevant_categories = self.get_relevant_category_ids(
                top_level_categories)
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
        SUBCLASS_QUERY = """SELECT ?item WHERE {
          ?item wdt:P279* wd:%s .
          }"""
        try:
            res = pywikibot.pagegenerators.WikidataSPARQLPageGenerator(
                query=SUBCLASS_QUERY % self.type_root_identifiers[
                    parent_class_label])
        except KeyError:
            raise KeyError(
                'Undefined parent type label, needs to be one of {}'.format(
                    [name for name in self.type_root_identifiers]))
        res = list([item.id for item in res])
        return res

    def collect_entities_from_dump(self, limit_per_query,
                                   wd_parameters,
                                   include_literals, languages,
                                   raise_on_missing_wikipedias=False,
                                   include_attribute_labels=True,
                                   require_country=True,
                                   include_wikipedia=True,
                                   delay_wikipedia_retrieval=True,
                                   dump_path='/home/jakob/Downloads/wikidatawiki-latest-pages-articles.xml.bz2',
                                   entity_type=None,
                                   n_queries=None
                                   # no effect, for consistent API only
                                   ):
        """
        iteratively parse a xml-dump (with embedded json entities) for entities
        of interest, using bz2file.
        Note: the pure JSON does not contain all relevant meta-info (e. g.
        timestamps and revision IDs)
        :param dump_path: path to the local copy of the incremental dump
        :type dump_path: str
        :param limit: maximum items to be read in (for debugging/testing)
        :type limit: int
        :return: list of entities to be updated
        :rtype: list
        """
        limit = limit_per_query
        if not self.all_relevant_categories:
            self.all_relevant_categories = self.get_relevant_category_ids(
                self.entity_types)
        relevant_entities_counter = 0
        to_be_remirrored = []
        counter_all = 0

        with BZ2File(dump_path) as xml_file:

            parser = et.iterparse(xml_file, events=('end',))

            for events, elem in parser:
                #     pass
                if limit and relevant_entities_counter > limit:
                    break
                # if t == 'item':
                if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}timestamp':
                    timestamp = elem.text
                if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}text':
                    counter_all += 1

                    if not elem.text:
                        continue
                    try:
                        elem_content = ujson.loads(elem.text)

                        elem_content['timestamp'] = timestamp
                        category = self.determine_relevant_category(
                            elem_content)
                        if category:
                            relevant_entities_counter += 1
                            try:
                                entity = collect_attributes_from_wp_and_wd(
                                    elem_content,
                                    languages=languages,
                                    wd_parameters=wd_parameters,
                                    include_literals=include_literals,
                                    include_attribute_labels=include_attribute_labels,
                                    require_country=require_country,
                                    include_wikipedia=include_wikipedia,
                                    delay_wikipedia_retrieval=delay_wikipedia_retrieval)
                                entity['category'] = category
                                yield entity
                            except ValueError as e:  # this probably means no Wikipedia p:
                                # age in
                                # any of our languages. We have no use for such entities.
                                if raise_on_missing_wikipedias:
                                    raise ValueError(
                                        'No information about this entity found!')
                                continue

                    except ValueError:
                        del elem
                        del events
                        continue

        # raise NotImplementedError

    def determine_relevant_category(self, elem_content):

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
                                   wd_parameters,
                                   include_literals, languages,
                                   raise_on_missing_wikipedias=False,
                                   id_only=False,
                                   include_attribute_labels=True,
                                   require_country=True,
                                   include_wikipedia=True,
                                   delay_wikipedia_retrieval=True
                                   ):
        """Get a list of entities with pywikibot.pagegenerators
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
        for entity_type in self.entity_types:
            for i in range(n_queries):
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
                        result = collect_attributes_from_wp_and_wd(
                            entity_raw,
                            languages=languages,
                            wd_parameters=wd_parameters,
                            include_literals=include_literals,
                            include_attribute_labels=include_attribute_labels,
                            require_country=require_country,
                            include_wikipedia=include_wikipedia,
                            delay_wikipedia_retrieval=delay_wikipedia_retrieval)

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
