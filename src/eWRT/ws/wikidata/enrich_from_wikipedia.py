#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on September 13, 2018

@author: Jakob Steixner, <jakob.steixner@modul.ac.at

Starting with a wikidata ID, retrieve additional information from Wikipedia'''

import sys
import ujson
import warnings

import wikipedia
from eWRT.ws.wikidata import wikipedia_wl

if sys.version_info.major == 3:
    from urllib.request import urlopen
else:
    from urllib2 import urlopen

RELEVANT_LANGUAGES = ['en', 'de', 'fr', 'es']


def wikipedia_page_info_from_title(wikipage_title, language):
    """
    Retreive selected meta info about a specific Wikipedia page, identified by
    its exact title and language.
    :param wikipage_title:
    :param language:
    :param wikidata_id:
    :return: dict of meta info about individual Wikipedia page
        (language, id and timestamp of last revision, title, link,
        summary).
    :raise wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError
    """
    language_page = {'language': language}
    wikipedia.set_lang(language)

    try:
        wikipage = wikipedia_wl.page(
            wikipage_title, auto_suggest=False, redirect=False)
    except (wikipedia.exceptions.PageError,
            wikipedia.exceptions.DisambiguationError) as e:
        raise e

    language_page['revision'] = wikipage.revision_id
    language_page['summary'] = wikipage.summary
    language_page['url'] = wikipage.url
    language_page['title'] = wikipage.title
    try:
        language_page['timestamp'] = wikipage.revision_timestamp
    except KeyError:
        language_page['timestamp'] = None
    return language_page


def get_sitelinks_from_wd_id(wikidata_id, languages):
    """
    Get the exact titles of Wikipedia pages about an entity (if they exist)
    in a number of languages. Sometimes produces false positives when a page
    exists but only as a redirect.
    :param wikidata_id: Qxx wikidata ID of an entity
    :param languages: list of language ISO codes.
    :return: dict {language: title}
    """
    site_versions = [language + 'wiki' for language in languages]
    page = urlopen(
        url=("https://www.wikidata.org/w/api.php?action=wbgetentities&"
             "format=json&props=sitelinks&ids={}&sitefilter={}".format(
            wikidata_id,
            '|'.join(site_versions))
        )
    )

    page_content = ujson.loads(page.read())
    sitelinks = {lang_version:
                     page_content['entities'][wikidata_id]['sitelinks'][
                         lang_version]['title'] for lang_version in
                 site_versions}
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
    if not sitelinks or sitelinks:
        sitelinks = get_sitelinks_from_wd_id(wikidata_id, languages=languages)
    for language in languages:
        try:
            wikipage_title = sitelinks[language + 'wiki']
            try:
                wikipedia_page = wikipedia_page_info_from_title(wikipage_title,
                                                                language)
                wikipedia_data.append(wikipedia_page)
            except (wikipedia.exceptions.PageError,
                    wikipedia.exceptions.DisambiguationError):
                warnings.warn('No Wikipedia page found in language {lang} '
                              'for entity {id}'.format(lang=language,
                                                       id=wikidata_id))
        except KeyError:
            pass

    if wikipedia_data:
        return wikipedia_data
    else:
        warnings.warn(
            'No Wikipedia page found in any of the requested languages for '
            'item {}!'.format(wikidata_id))

        return None
