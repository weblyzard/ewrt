#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
This module builds heavily on the get_keyword_ideas.py file by Google:
https://github.com/googleads/googleads-python-lib/blob/master/examples/
adwords/v201809/optimization/get_keyword_ideas.py

The config file must follow the google ads config yaml:
https://github.com/googleads/googleads-python-lib/blob/master/googleads.yaml
'''

from collections import OrderedDict

import logging

import time

from googleads import adwords
from googleads.errors import GoogleAdsServerFault
from googleads.oauth2 import GoogleRefreshTokenClient

import zeep

logger = logging.getLogger(__name__)


class GoogleAdWordsKeywordStatistics(object):

    # The ID can be found in the documentation:
    # https://developers.google.com/adwords/api/docs/appendix/languagecodes
    LANGUAGE_MAPPING = {
        'de': '1001',
        'en': '1000',
        'fr': '1002'
    }
    PAGE_SIZE = 1000
    STATS_DEFAULT_ATTRIBUTES = {
        'KEYWORD_TEXT': lambda x: x,
        'SEARCH_VOLUME': lambda x: x,
        'AVERAGE_CPC': lambda x: zeep.helpers.serialize_object(x)['microAmount'],
        'COMPETITION': lambda x: x,
        # 'CATEGORY_PRODUCTS_AND_SERVICES': lambda x: x,
    }
    MAX_RETRIES = 3

    def __init__(self, adwords_client):
        self.client = adwords_client

    @classmethod
    def from_config_parameters(cls, developer_token, client_id, client_secret,
                               client_customer_id, refresh_token,
                               user_agent='unknown', timeout=3600):
        oauth2_client = GoogleRefreshTokenClient(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token)
        client = adwords.AdWordsClient(
            developer_token=developer_token,
            oauth2_client=oauth2_client,
            user_agent=user_agent,
            timeout=timeout,
        client_customer_id=client_customer_id)
        return cls(adwords_client=client)

    @classmethod
    def from_config_file(cls, config_file=None):
        '''
        :param config_file: The path to the yaml file containing the Google \
                Adwords configuration.
        :type config_file: str
        '''
        client = adwords.AdWordsClient.LoadFromStorage(config_file)
        return cls(adwords_client=client)

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
            attributes = self.STATS_DEFAULT_ATTRIBUTES
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
            'languages': [{'id': self.LANGUAGE_MAPPING[language.lower()]}]
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
        num_retries = 0
        while more_pages:
            try:
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
            except GoogleAdsServerFault as exc:
                logger.warning(exc)
                if (len(exc.errors) == 1
                    and exc.errors[0]['errorString'] ==
                        'RateExceededError.RATE_EXCEEDED'
                   ):
                    if num_retries > self.MAX_RETRIES:
                        break
                    seconds = exc.errors[0]['retryAfterSeconds']
                    num_retries += 1
                    logger.error("Hitted Google Adwords rate limit, "
                                "retrying in %s seconds",
                                seconds)
                    time.sleep(seconds)
        return results

    def get_traffic_estimates(self, keywords, attributes=None, language='de'):
        '''
        Get traffic estimates for keywords from Google Ads.

        :param keywords: A list of keywords for which to fetch statistics.
        :type keywords: list
        :param attributes: The traffic estimates attributes to fetch together \
                with a mapping to use to compile the result. If None set to \
                DEFAULT_ATTRIBUTES.
        :type attributes: dict
        :param language: two-letter language code to fetch. Currently only \
                de, en and fr supported.
        :returns: A mapping of keyword to a dict containing the attribute \
                values.
        :rtype: dict
        '''
        traffic_estimator_service = self.client.GetService(
            'TrafficEstimatorService', version='v201809')
        keyword_estimate_requests = [
            {
                'keyword': {
                    'xsi_type': 'Keyword',
                    'text': kw,
                    'matchType': 'EXACT'
                }
            }
            for kw in keywords
        ]

        # Create ad group estimate requests.
        adgroup_estimate_requests = [{
            'keywordEstimateRequests': keyword_estimate_requests,
            'maxCpc': {
                'xsi_type': 'Money',
                'microAmount': '1000000'
            }
        }]

        # Create campaign estimate requests.
        campaign_estimate_requests = [{
            'adGroupEstimateRequests': adgroup_estimate_requests,
            'criteria': [
                #{
                #    'xsi_type': 'Location',
                #    'id': '2840'  # United States.
                #},
                {
                    'xsi_type': 'Language',
                    'id': self.LANGUAGE_MAPPING[language]
                }
            ],
        }]

        # Create the selector.
        selector = {
            'campaignEstimateRequests': campaign_estimate_requests,
        }

        estimates = traffic_estimator_service.get(selector)
        mapped_estimates = {
            k:v for k, v in zip(
                keywords,
                zeep.helpers.serialize_object(
                    estimates['campaignEstimates'][0]
                ).get(
                    'adGroupEstimates', [{}]
                )[0].get(
                    'keywordEstimates', []
                )
            )
        }
        results = {}
        for keyword, value in mapped_estimates.items():
            max_dict = value['max']
            min_dict = value['min']
            results[keyword] = {}
            for k in max_dict:
                if k in ('totalCost', 'averageCpc'):
                    results[keyword][k] = (
                        max_dict[k]['microAmount'] + min_dict[k]['microAmount']
                    ) / 2000000.0
                else:
                    results[keyword][k] = (max_dict[k] + min_dict[k]) / 2.0
        return results


if __name__ == '__main__':
    client = GoogleAdWordsKeywordStatistics.from_config_file(
        config_file='./googleads.yaml')
    keyword_statistics = client.get_traffic_estimates(
        keywords=['donald trump', 'brexit'],
        language='en')
    from pprint import pprint
    pprint(keyword_statistics)
