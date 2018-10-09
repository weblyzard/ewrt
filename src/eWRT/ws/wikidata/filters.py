#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on October 05, 2018

@author: jakob <jakob.steixner@modul.ac.at>
'''

import copy

def filter_result(language, raw_result, literals=('labels', 'descriptions', 'aliases')):
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
        if key[2:] == 'wiki' or wikibot_result[key] is None:
            continue
        elif isinstance(wikibot_result[key], (basestring)) or wikibot_result[key] is None:
            output_formatted_entity[key] = wikibot_result[key]
        elif isinstance(wikibot_result[key], dict):
            if key in literals:
                output_formatted_entity[key] = wikibot_result[key][language]
            elif 'values' in wikibot_result[key]:
                output_formatted_entity[key] = filter_language_values(
                    wikibot_result[key]['values'], language)
            else:
                output_formatted_entity[key] = wikibot_result[key]

        else:
            output_formatted_entity[key] = wikibot_result[key]

    return output_formatted_entity


def filter_language_values(value_list, language):
    values = copy.deepcopy(value_list)
    for value in values:
        if 'qualifiers' in value:
            value['qualifiers'] = filter_language_values(value['qualifiers'],
                                                         language)
        if 'labels' in value:
            value['labels'] = value['labels'].get(language, None)
    return values
