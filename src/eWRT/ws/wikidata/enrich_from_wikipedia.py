#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on September 13, 2018

@author: Jakob Steixner, <jakob.steixner@modul.ac.at

Starting with a wikidata ID, retrieve additional information from Wikipedia'''

import sys
import ujson
import warnings

import requests
import wikipedia

if sys.version_info.major == 3:
    from urllib.request import urlopen
else:
    from urllib2 import urlopen

RELEVANT_LANGUAGES = ['en', 'de', 'fr', 'es']

# setup = '''
#
# import wikipedia, requests
# from eWRT.ws.wikidata import wikipedia_wl
# wikipedia.set_lang('en')
USER_AGENT = 'weblyzard (https://www.weblyzard.com/privacy-policy/)'


def wikipedia_page_info_from_title(wikipage_title, language, redirect=False):
    """
    Retreive selected meta info about a specific Wikipedia page, identified by
    its exact title and language.
    :param wikipage_title:
    :param language:
    :return: dict of meta info about individual Wikipedia page
        (language, id and timestamp of last revision, title, link,
        summary)
    """
    # language_page = {'language': language}
    API_URL = u'http://' + language.lower() + u'.wikipedia.org/w/api.php'
    wikipedia.set_lang(language)
    params = {'titles': wikipage_title,
              'prop': 'info|extracts|pageprops',
              'explaintext': '',
              'exintro': '',
              'ppprop': 'disambiguation',
              'redirects': '',
              'inprop': 'url',
              'action': 'query',
              'format': 'json'
              }

    headers = {
        'User-Agent': USER_AGENT
    }
    query_result = requests.get(API_URL, params=params,
                                headers=headers).json()
    flagged_as_redirect = set()
    if 'redirects' in query_result['query']:
        flagged_as_redirect = set([page_redirect['to'] for page_redirect in
                                   query_result['query']['redirects']])
    for page in query_result['query']['pages'].values():
        title = page['title']
        if 'missing' in page:
            continue
        elif title in flagged_as_redirect and redirect is False:
            continue
        elif 'pageprops' in page and 'disambiguation' in page['pageprops']:
            continue
        language_page = {'language': language}
        summary = page['extract']
        if not summary:
            continue
        language_page['summary'] = summary
        language_page['url'] = page['canonicalurl']
        language_page['title'] = title
        language_page['timestamp'] = page['touched']
        yield language_page


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
    sitelinks = {}
    for lang_version in site_versions:
        try:
            sitelinks[lang_version] = \
                page_content['entities'][wikidata_id]['sitelinks'][
                    lang_version]['title']
        except KeyError:
            pass

    return sitelinks if sitelinks else None


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
            try:
                wikipedia_page = wikipedia_page_info_from_title(wikipage_title,
                                                                language).next()
                wikipedia_data.append(wikipedia_page)
            except ValueError:
                warnings.warn('No Wikipedia page or page with empty summary '
                              'found in language {lang} '
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

# print(wp_summary_from_wdid('Q42'))
