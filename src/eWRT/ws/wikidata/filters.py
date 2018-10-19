#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on October 05, 2018

@author: jakob <jakob.steixner@modul.ac.at>
'''

import copy


def filter_result(language, raw_result,
                  literals=('labels', 'descriptions', 'aliases')):
    """

    :param language:
    :param raw_result:
    :param literals:
    :return:
    """
    output_formatted_entity = {}
    wikibot_result = raw_result

    # replace wikidata link as url with first encountered
    # wikipedia link (assumes languages in order of preference.
    # for key in DEFAULT_LITERALS:
    #     if key in wikibot_result:
    #         output_formatted_entity[key] = wikibot_result[key][language]

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
                output_formatted_entity[key] = wikibot_result[key][language]
            elif 'values' in wikibot_result[key]:
                output_formatted_entity[key] = {
                input_key: wikibot_result[key][input_key] for input_key in
                wikibot_result[key] if input_key not in ('values', 'preferred')}

                output_formatted_entity[key]['values'] = filter_language_values(
                    wikibot_result[key]['values'], language)

            else:
                output_formatted_entity[key] = wikibot_result[key]
            if 'preferred' in output_formatted_entity[key]:
                output_formatted_entity[key]['preferred'] = \
                    filter_language_values(
                        [wikibot_result[key]['preferred']], language
                    )[0]

        else:
            output_formatted_entity[key] = wikibot_result[key]

    return output_formatted_entity


def filter_language_values(value_list, language):
    """

    :param value_list:
    :param language:
    :return:
    """
    values = copy.deepcopy(value_list)
    for value in values:
        if 'qualifiers' in value:
            value['qualifiers'] = filter_language_values(value['qualifiers'],
                                                         language)
        if 'labels' in value:
            value['labels'] = value['labels'].get(language, None)
    return values
