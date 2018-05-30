#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on May 29, 2018

@author: Max Göbel <goebel@weblyzard.com>
'''
import httplib2
import unittest
import datetime

from time import sleep
from datetime import date
from apiclient.discovery import build

from oauth2client.client import OAuth2Credentials


class GAnalyticsClient():

    VERSION = 'v3'  # needed by apiclient
    SERVICE_NAME = 'analytics'  # needed by apiclient

    QUERY_THROTTLE_SECS = 1  # sleep interval between queries in seconds
    MAX_RESULTS = '25'

    metrics = ['ga:visitors', 'ga:newVisits', 'ga:percentNewVisits',
               'ga:sessions', 'ga:bounces', 'ga:entranceBounceRate',
               'ga:bounceRate', 'ga:sessionDuration', 'ga:avgSessionDuration',
               ]

    def __init__(self, credentials, check_new=False):
        ''' '''
        self.service = None
        self.credentials = credentials
        self.source_group_name = 'ganalytics'
        self.webproperties = None

        if not self.service:
            self.service = self.init_service(self.credentials)

        # update DB
        if check_new:
            self.update_profile_db()

    @classmethod
    def init_service(cls, credentials):
        ''' '''
        http = httplib2.Http()

        cred = OAuth2Credentials(access_token=credentials['access_token'],
                                 client_id=credentials['client_id'],
                                 client_secret=credentials['client_secret'],
                                 refresh_token=credentials['refresh_token'],
                                 token_expiry=credentials['token_expiry'],
                                 token_uri=credentials['token_uri'],
                                 user_agent=credentials['user_agent'])

        http = cred.authorize(http)

        # Construct and return the authorized Analytics Service Object
        return build(cls.SERVICE_NAME, cls.VERSION, http=http)

    def get_webproperty_details(self, account_id, webproperty_id):
        ''' '''
        profiles = self.service.management().profiles().list(
            accountId=account_id,
            webPropertyId=webproperty_id).execute()

        for profile in profiles.get('items'):
            yield profile.get('id')

    def get_metrics(self, profile_id, start_date=None, end_date=None):
        '''
            Executes and returns core metrics from the 
            Google Core Reporting API.
            Args:
                optional start and end date
            Returns:
                The response returned from the Core Reporting API.
        '''
        metrics = ','.join(self.metrics)
        if not start_date:
            start_date = datetime.date.today().strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.date.today().strftime("%Y-%m-%d")
        if isinstance(start_date, date):
            start_date = start_date.strftime("%Y-%m-%d")
        if isinstance(end_date, date):
            end_date = end_date.strftime("%Y-%m-%d")
        return self.service.data().ga().get(ids='ga:' + profile_id,
                                            start_date=start_date,
                                            end_date=end_date,
                                            metrics=metrics).execute()

    def get_country_split(self, profile_id, start_date=None, end_date=None):
        '''
            Executes and returns geo metrics from the 
            Google Core Reporting API.
            Args:
                optional start and end date
            Returns:
                The response returned from the Core Reporting API.
        '''
        if not start_date:
            start_date = datetime.date.today().strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.date.today().strftime("%Y-%m-%d")
        if isinstance(start_date, date):
            start_date = start_date.strftime("%Y-%m-%d")
        if isinstance(end_date, date):
            end_date = end_date.strftime("%Y-%m-%d")
        return self.service.data().ga().get(ids='ga:' + profile_id,
                                            start_date=start_date,
                                            end_date=end_date,
                                            metrics='ga:visits',
                                            dimensions='ga:country',
                                            sort='-ga:visits',
                                            filters='ga:medium==organic',
                                            start_index='1',
                                            max_results=self.MAX_RESULTS).execute()

    def get_top_keywords(self, profile_id, start_date=None, end_date=None):
        '''
            Executes and returns keyword metrics from the 
            Google Core Reporting API.
            Args:
                optional start and end date
            Returns:
                The response returned from the Core Reporting API.
        '''
        if not start_date:
            start_date = datetime.date.today().strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.date.today().strftime("%Y-%m-%d")
        if isinstance(start_date, date):
            start_date = start_date.strftime("%Y-%m-%d")
        if isinstance(end_date, date):
            end_date = end_date.strftime("%Y-%m-%d")
        return self.service.data().ga().get(ids='ga:' + profile_id,
                                            start_date=start_date,
                                            end_date=end_date,
                                            metrics='ga:visits',
                                            dimensions='ga:keyword',
                                            sort='-ga:visits',
                                            filters='ga:medium==organic',
                                            start_index='1',
                                            max_results='25').execute()

    def get_page_track(self, profile_id, start_date=None, end_date=None):
        '''
            Executes and returns page track metrics from the 
            Google Core Reporting API.
            Args:
                optional start and end date
            Returns:
                The response returned from the Core Reporting API.
        '''
        if not start_date:
            start_date = datetime.date.today().strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.date.today().strftime("%Y-%m-%d")
        if isinstance(start_date, date):
            start_date = start_date.strftime("%Y-%m-%d")
        if isinstance(end_date, date):
            end_date = end_date.strftime("%Y-%m-%d")
        return self.service.data().ga().get(ids='ga:' + profile_id,
                                            start_date=start_date,
                                            end_date=end_date,
                                            metrics='ga:visits',
                                            dimensions='ga:hostname,ga:pagePath',
                                            sort='-ga:visits',
                                            filters='ga:medium==organic',
                                            start_index='1',
                                            max_results='25').execute()

    def get_social_media(self, profile_id, start_date=None, end_date=None):
        '''
            Executes and returns social media metrics from the 
            Google Core Reporting API.
            Args:
                optional start and end date
            Returns:
                The response returned from the Core Reporting API.
        '''
        if not start_date:
            start_date = datetime.date.today().strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.date.today().strftime("%Y-%m-%d")
        if isinstance(start_date, date):
            start_date = start_date.strftime("%Y-%m-%d")
        if isinstance(end_date, date):
            end_date = end_date.strftime("%Y-%m-%d")
        return self.service.data().ga().get(ids='ga:' + profile_id,
                                            start_date=start_date,
                                            end_date=end_date,
                                            metrics='ga:visits',
                                            dimensions='ga:socialNetwork',
                                            sort='-ga:visits',
                                            filters='ga:medium==organic',
                                            start_index='1',
                                            max_results='25').execute()

    def get_top_referers(self, profile_id, start_date=None, end_date=None):
        '''
            Executes and returns referer metrics from the 
            Google Core Reporting API.
            Args:
                optional start and end date
            Returns:
                The response returned from the Core Reporting API.
        '''
        if not start_date:
            start_date = datetime.date.today().strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.date.today().strftime("%Y-%m-%d")
        if isinstance(start_date, date):
            start_date = start_date.strftime("%Y-%m-%d")
        if isinstance(end_date, date):
            end_date = end_date.strftime("%Y-%m-%d")
        return self.service.data().ga().get(ids='ga:' + profile_id,
                                            start_date=start_date,
                                            end_date=end_date,
                                            dimensions='ga:source',
                                            metrics='ga:pageviews,ga:sessionDuration,ga:exits',
                                            filters='ga:medium==referral',
                                            sort='-ga:pageviews',
                                            start_index='1',
                                            max_results='25').execute()

    def get_accounts(self):
        ''' '''
        return self.service.management().accounts().list().execute().get('items')

    def get_profiles(self, account_id):
        ''' Get active profiles configured for a Google Analytics account. '''
        result = []
        webproperties = self.service.management().webproperties().list(
            accountId=account_id).execute()

        for item in webproperties.get('items'):
            for pid in self.get_webproperty_details(self.service,
                                                    account_id,
                                                    item.get('id')):
                result.append((account_id, pid))
        return result

    def process_profile(self, profile_id, account_id, start_date=None, end_date=None):
        ''' 
        Process a single google analytics profile by id
        '''
        # set start and end date if None
        if not start_date:
            start_date = datetime.date.today().strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.date.today().strftime("%Y-%m-%d")

        result = {}

        # query top country split
        countries = self.get_country_split(profile_id=profile_id,
                                           start_date=start_date,
                                           end_date=end_date)

        str_arr = []
        if 'rows' in countries:
            for row in countries['rows']:
                str_arr.append(row[0] + ':' + row[1])
        result['ga:countries'] = ','.join(str_arr)

        # query top search keywords
        sleep(self.QUERY_THROTTLE_SECS)
        keywords = self.get_top_keywords(profile_id=profile_id,
                                         start_date=start_date,
                                         end_date=end_date)
        str_arr = []
        if 'rows' in keywords:
            for row in keywords['rows']:
                str_arr.append(row[0] + ':' + row[1])
        result['ga:keywords'] = ','.join(str_arr)

        # query top referers
        sleep(self.QUERY_THROTTLE_SECS)
        referers = self.get_top_referers(profile_id=profile_id,
                                         start_date=start_date,
                                         end_date=end_date)
        str_arr = []
        if 'rows' in referers:
            for row in referers['rows']:
                str_arr.append(row[0] + ':' + row[1])
        result['ga:referers'] = ','.join(str_arr)

        sleep(self.QUERY_THROTTLE_SECS)
        soc_media = self.get_social_media(profile_id=profile_id,
                                          start_date=start_date,
                                          end_date=end_date)
        str_arr = []
        if 'rows' in soc_media:
            for row in soc_media['rows']:
                if row[0] and row[0] != '(not set)':
                    str_arr.append(row[0] + ':' + row[1])
        result['ga:social_media'] = ','.join(str_arr)

        sleep(self.QUERY_THROTTLE_SECS)
        page_track = self.get_page_track(profile_id=profile_id,
                                         start_date=start_date,
                                         end_date=end_date)
        page_arr = []
        if 'rows' in page_track:
            for row in page_track['rows']:
                if row[1] and row[1] != '(not set)':
                    page_arr.append(row[1] + ':' + row[2])
        result['ga:page_track'] = ','.join(page_arr)

        # get metrics defined in params
        sleep(self.QUERY_THROTTLE_SECS)
        response = {}
        webproperties = self.service.management().webproperties().list(
            accountId=account_id).execute()
        for item in webproperties.get('items'):
            sleep(self.QUERY_THROTTLE_SECS)
            for pid in self.get_webproperty_details(service=self.service,
                                                    account_id=account_id,
                                                    webproperty_id=item.get('id')):
                if pid == profile_id:
                    response = self.get_metrics(profile_id=profile_id,
                                                start_date=start_date,
                                                end_date=end_date)
                    break
        i = 0
        if response.get('columnHeaders'):
            for key in response.get('columnHeaders'):
                if 'rows' in response:
                    value = response.get('rows')[0][i]
                key_str = key.get('name')
                i = i + 1
                result[key_str] = value
        return result


class GanalyticsTest(unittest.TestCase):

    def test_ganalytics(self):

        # Get stored credentials or run the Auth Flow if none are found
        metrics = ['ga:visitors', 'ga:newVisits', 'ga:percentNewVisits',
                   'ga:sessions', 'ga:bounces', 'ga:entranceBounceRate',
                   'ga:bounceRate', 'ga:sessionDuration', 'ga:avgSessionDuration',
                   ]

        client = GAnalyticsClient()
        result = client.run(",".join(metrics))
        print result


if __name__ == "__main__":
    unittest.main()
