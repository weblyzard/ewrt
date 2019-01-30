#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
This module builds heavily on the get_keyword_ideas.py file by Google:
https://github.com/googleads/googleads-python-lib/blob/master/examples/
adwords/v201809/optimization/get_keyword_ideas.py
'''


from googleads import adwords

import zeep


class GoogleAdWordsKeywordStatistics(object):

    # The ID can be found in the documentation:
    # https://developers.google.com/adwords/api/docs/appendix/languagecodes
    LANGUAGE_MAPPING = {
        'de': '1001',
        'en': '1000',
        'fr': '1002'
    }
    PAGE_SIZE = 1000
    DEFAULT_ATTRIBUTES = {
        'KEYWORD_TEXT': lambda x: x,
        'SEARCH_VOLUME': lambda x: x,
        'AVERAGE_CPC': lambda x: zeep.helpers.serialize_object(x)['microAmount'],
        'COMPETITION': lambda x: x,
        # 'CATEGORY_PRODUCTS_AND_SERVICES': lambda x: x,
    }

    def __init__(self, config_file=None):
        '''
        :param config_file: The path to the yaml file containing the Google \
                Adwords configuration.
        :type config_file: str
        '''
        self.client = adwords.AdWordsClient.LoadFromStorage(config_file)

    def get_keyword_stats(self, keywords, attributes=None, language='de'):
        '''
        Get statistics about keywords from Google Ads.

        :param keywords: A list of keywords for which to fetch statistics.
        :type keywords: list
        :param attributes: The statistics attributes to fetch together with a \
                mapping to use to compile the result. If None set to \
                DEFAULT_ATTRIBUTES.
        :type attributes: dict
        :param language: two-letter language code to fetch. Currently only \
                de, en and fr supported.
        :returns: A mapping of keyword to a dict containing the attribute \
                values.
        :rtype: dict
        '''
        targeting_idea_service = self.client.GetService(
            'TargetingIdeaService', version='v201809')

        # Construct selector object and retrieve related keywords.
        selector = {
            'ideaType': 'KEYWORD',
            'requestType': 'STATS'
        }
        if attributes is None:
            attributes = self.DEFAULT_ATTRIBUTES
        elif 'KEYWORD_TEXT' not in attributes:
            attributes['KEYWORD_TEXT'] = None
        selector['requestedAttributeTypes'] = attributes.keys()

        offset = 0

        selector['paging'] = {
            'startIndex': str(offset),
            'numberResults': str(self.PAGE_SIZE)
        }
        selector['searchParameters'] = [{
            'xsi_type': 'RelatedToQuerySearchParameter',
            'queries': keywords
        }]
        # Language setting (optional).
        selector['searchParameters'].append({
            'xsi_type': 'LanguageSearchParameter',
            'languages': [{'id': self.LANGUAGE_MAPPING[language]}]
        })

        # Network search parameter (optional)
        selector['searchParameters'].append({
            'xsi_type': 'NetworkSearchParameter',
            'networkSetting': {
                'targetGoogleSearch': True,
                'targetSearchNetwork': False,
                'targetContentNetwork': False,
                'targetPartnerSearchNetwork': False
            }
        })
        results = {}
        more_pages = True
        while more_pages:
            page = targeting_idea_service.get(selector)
            # Display results.
            if 'entries' in page:
                for result in page['entries']:
                    attribute_results = {}
                    for attribute_result in result['data']:
                        attribute_results[attribute_result['key']] = getattr(
                            attribute_result['value'], 'value', '0')
                    keyword = attribute_results.get('KEYWORD_TEXT')
                    if keyword is None:
                        continue
                    results[keyword] = {
                        attribute: mapping(attribute_results[attribute])
                        for attribute, mapping in attributes.items()
                        if attribute != 'KEYWORD_TEXT'
                    }
            else:
                print('No related keywords were found.')
            offset += self.PAGE_SIZE
            selector['paging']['startIndex'] = str(offset)
            more_pages = offset < int(page['totalNumEntries'])
        return results

if __name__ == '__main__':
    client = GoogleAdWordsKeywordStatistics(
        config_file='./googleads.yaml')
    keyword_statistics = client.get_keyword_stats(
        keywords=['donald trump', 'brexit'],
        language='de')
    from pprint import pprint
    pprint(keyword_statistics)
