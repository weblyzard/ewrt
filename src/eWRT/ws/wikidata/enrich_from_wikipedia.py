#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on September 13, 2018

@author: Jakob Steixner, <jakob.steixner@modul.ac.at

Starting with a wikidata ID, retrieve additional information from Wikipedia'''

import ujson
import warnings
from urllib2 import urlopen

import wikipedia
import wikipedia_wl

RELEVANT_LANGUAGES = ['en', 'de', 'fr', 'es']


def wikipedia_page_info_from_sitelinks(wikipage_title, language, wikidata_id):
    language_page = {'language': language}
    wikipedia.set_lang(language)

    try:
        wikipage = wikipedia_wl.page(wikipage_title, auto_suggest=False, redirect=False)
    except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
        warnings.warn('No wikipedia page found in language {language} for '
                      'entity {entity}!.'.format(language=language, entity=wikidata_id))
    language_page['revision'] = wikipage.revision_id
    language_page['summary'] = wikipage.summary
    language_page['url'] = wikipage.url
    language_page['title'] = wikipage.title
    try:
        language_page['timestamp'] = wikipage.revision_timestamp
    except KeyError:
        language_page['timestamp'] = None
    has_page = True
    return language_page


def get_sitelinks_from_wd_id(wikidata_id, languages):
    page = urlopen(
        url=("https://www.wikidata.org/w/api.php?action=wbgetentities&"
             "format=json&props=sitelinks&ids={}&sitefilter={}".format(
            wikidata_id, '|'.join([language + 'wiki' for language in languages]))
        )
    )

    page_content = ujson.loads(page.read())
    sitelinks = page_content['entities'][wikidata_id]
    return sitelinks


def wp_summary_from_wdid(wikidata_id, languages=None, sitelinks=None):
    """
    :param wikidata_id: Qxxx-ID of the entity in Wikidata's ontology
    :type wikidata_id: str
    :param languages: list of language ISO codes, in order of preference
    :type languages
    :param sitelinks: dict of language:title for the wikipedia titles,
        if None, will retrieve them
    :return: list with one dictionary per language for which a Wikipedia
    page about this entity exists, each containing the link, summary, title,
    revision id and revision timestamp
    """
    if not languages:
        languages = RELEVANT_LANGUAGES
    wikipedia_data = []
    if not sitelinks:
        sitelinks = get_sitelinks_from_wd_id(wikidata_id, languages=languages)
    for language in languages:
        try:
            wikipage_title = sitelinks[language + 'wiki']
            wikipedia_page = wikipedia_page_info_from_sitelinks(wikipage_title, language,
                                                                wikidata_id)
            if wikipedia_page:
                wikipedia_data.append(wikipedia_page)
        except KeyError:
            pass

    if wikipedia_data:
        return wikipedia_data
    else:
        warnings.warn('No Wikipedia page found in any of the requested languages for '
                      'item {}!'.format(wikidata_id))
        return None
