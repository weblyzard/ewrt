#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on October 05, 2018

@author: jakob <jakob.steixner@modul.ac.at>

Filter multilingual result to produce monolingual documents by rejecting
labels etc. in the non-required languages.
'''

from past.builtins import basestring
import copy


def filter_result(language, raw_result,
                  literals=['labels', 'descriptions', 'aliases']):
    """

    :param language: language iso code
    :type language: basestring
    :param raw_result: dict with metadata about entity
    :type raw_result: dict
    :param literals: iterable of literal attributes
    :type literals: list
    :return: dict with all language-unspecific data + data in selected
        language, discarding data in other languages
    :rtype dict
    """
    output_formatted_entity = {}
    wikibot_result = raw_result

    for key in wikibot_result:
        # if key in DEFAULT_LITERALS:
        #     continue
        if key == language + 'wiki' and isinstance(wikibot_result[key], dict):
            output_formatted_entity[key] = wikibot_result[key]
        # elif key.endswith('wiki') or wikibot_result[key] is None:
        #     continue
        elif isinstance(wikibot_result[key], basestring) or wikibot_result[
            key] is None:
            output_formatted_entity[key] = wikibot_result[key]
        elif isinstance(wikibot_result[key], dict):
            if key in literals:
                try:
                    output_formatted_entity[key] = wikibot_result[key][language]
                except KeyError:
                    pass
            elif 'values' in wikibot_result[key]:
                output_formatted_entity[key] = {
                input_key: wikibot_result[key][input_key] for input_key in
                wikibot_result[key] if input_key not in ('values', 'preferred')}

                output_formatted_entity[key]['values'] = filter_language_values(
                    wikibot_result[key]['values'], language)

            else:
                output_formatted_entity[key] = wikibot_result[key]
            if (key in output_formatted_entity and
                    'preferred' in output_formatted_entity[key]):
                output_formatted_entity[key]['preferred'] = \
                    filter_language_values(
                        [wikibot_result[key]['preferred']], language
                    )[0]

        else:
            output_formatted_entity[key] = wikibot_result[key]

    return output_formatted_entity


def filter_language_values(value_list, language):
    """
    Filter attribute labels for language, recursively apply to qualifiers of
    attributes.
    :param value_list: Attribute values (list of dicts with
        'labels': {<language1>: 'label, <language2: 'label'}
    :param language: Output language
    :return: list of of dicts with {'labels': label_in_language}
    """
    values = copy.deepcopy(value_list)
    for value in values:
        if 'qualifiers' in value:
            value['qualifiers'] = filter_language_values(value['qualifiers'],
                                                         language)
        if 'labels' in value:
            value['labels'] = value['labels'].get(language, None)
    return values
