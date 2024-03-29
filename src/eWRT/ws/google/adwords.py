#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
This module builds heavily on the get_keyword_ideas.py file by Google:
https://github.com/googleads/googleads-python-lib/blob/master/examples/
adwords/v201809/optimization/get_keyword_ideas.py

The config file must follow the google ads config yaml:
https://github.com/googleads/googleads-python-lib/blob/master/googleads.yaml
'''
from __future__ import print_function

from builtins import str
from builtins import zip
from builtins import object
from collections import OrderedDict

import logging

import time
import random

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
    # according to
    # https://developers.google.com/adwords/api/docs/appendix/limits
    TRAFFIC_KEYWORDS_LIMIT = 2500

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
        selector['requestedAttributeTypes'] = list(attributes.keys())

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
                            for attribute, mapping in list(attributes.items())
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
                    logger.error("Hit Google Adwords rate limit, "
                                 "retrying in %s seconds",
                                 seconds)
                    time.sleep(seconds)
        return results

    def get_traffic_estimates(self, keywords, attributes=None, language='de',
                              max_retries=MAX_RETRIES,
                              traffic_keywords_limit=TRAFFIC_KEYWORDS_LIMIT,
                              value_scale=1000000, seconds_limit_for_retry=60,
                              match_type='PHRASE', max_cpc=1):
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
        def get_sub_result(traffic_estimator_service,
                           keywords,
                           language):
            keyword_estimate_requests = [
                {
                    'keyword': {
                        'xsi_type': 'Keyword',
                        'text': kw,
                        'matchType': match_type
                    }
                }
                for kw in keywords
            ]

            # Create ad group estimate requests.
            adgroup_estimate_requests = [{
                'keywordEstimateRequests': keyword_estimate_requests,
                'maxCpc': {
                    'xsi_type': 'Money',
                    'microAmount': str(value_scale * max_cpc)
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

            num_retries = 0
            exc_count = 0
            faulty_values = 0
            while True:
                results = {}
                try:
                    estimates = traffic_estimator_service.get(selector)
                    mapped_estimates = {
                        k: v for k, v in zip(
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
                    for keyword, value in mapped_estimates.items():
                        max_dict = value['max']
                        min_dict = value['min']
                        results[keyword] = {}
                        faulty_values_per_kw = 0
                        for k in max_dict:
                            try:
                                if k in ('totalCost', 'averageCpc'):
                                    results[keyword][k] = (
                                        float(max_dict[k].get(
                                            'microAmount', 0.))
                                        + float(min_dict[k].get('microAmount', 0.))
                                    ) / (2 * value_scale)
                                else:
                                    results[keyword][k] = (
                                        max_dict[k] + min_dict[k]) / 2.0
                            except (AttributeError, TypeError):
                                results[keyword][k] = 0.
                                faulty_values_per_kw += 1
                        if faulty_values_per_kw > 2:
                            faulty_values += 1

                    return results, faulty_values

                except GoogleAdsServerFault as exc:
                    logger.error(exc)
                    # RATE EXCEEDED
                    if (len(exc.errors) == 1
                                and exc.errors[0]['errorString'] ==
                            'RateExceededError.RATE_EXCEEDED'
                            ):
                        # too many requests per minute
                        if exc.errors[0]['rateName'] == 'RequestsPerMinute':
                            seconds = exc.errors[0]['retryAfterSeconds']
                            if seconds <= seconds_limit_for_retry:
                                wait_seconds = seconds * \
                                    random.uniform(1.0, 2.0)
                                logger.error("Hit Google Adwords per minute rate limit, "
                                             "retrying in %s seconds",
                                             wait_seconds)
                                time.sleep(wait_seconds)
                            else:
                                break
                        # too many daily requests
                        if exc.errors[0]['rateName'] == 'OperationsPerDay':
                            logger.error(
                                "Hit Google Adwords daily rate limit (10 000/day).")
                            break
                    # retry for unspecified server fault error
                    else:
                        logger.error(exc)
                        if num_retries > max_retries:
                            logger.error(
                                f'Failed to retrieve keyword values for sub-'
                                         f'batch of {len(keywords)} keywords. '
                                f'Exception was {exc}', exc_info=True)
                            return results
                        num_retries += 1
                # log other exceptions and terminate if too many
                except Exception as e:
                    logger.error(e)
                    print(e)
                    if exc_count > len(keywords) / 2:
                        return {}
                    exc_count += 1


        traffic_estimator_service = self.client.GetService(
            'TrafficEstimatorService', version='v201809')
        result = {}
        lower = 0
        num_keywords = len(keywords)
        batch_count = 0
        while lower < num_keywords:
            batch_count += 1
            keywords_batch = keywords[lower:min(lower + traffic_keywords_limit,
                                            num_keywords)]
            sub_result, faulty_values = get_sub_result(
                traffic_estimator_service=traffic_estimator_service,
                keywords=keywords_batch,
                language=language)
            keywords_size = len(keywords_batch)
            fault_percentage = float(
                (float(faulty_values) / float(keywords_size)) * 100)
            logger.info("{0:.2f}% from batch {1:.0f}".format(
                fault_percentage, batch_count))
            if not sub_result:
                logger.error(
                    "Could not retrieve all results from Google Adwords. Updated partial results.")
                return {}
            else:
                result.update(sub_result)
                lower = min(num_keywords, lower + traffic_keywords_limit)
        logger.info("{} batches requested".format(str(batch_count)))
        return result


if __name__ == '__main__':
    client = GoogleAdWordsKeywordStatistics.from_config_file(
        config_file='./googleads.yaml')
    keyword_statistics = client.get_traffic_estimates(
        keywords=['donald trump', 'brexit'],
        language='en')
    from pprint import pprint
    pprint(keyword_statistics)
