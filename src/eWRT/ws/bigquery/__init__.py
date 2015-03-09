#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@package eWRT.ws.bigquery

Created on 25.02.2015

@author: Christian Junker
"""
import json
import unittest

from eWRT.config import BIG_QUERY_PROJECT_ID
from eWRT.access.http import Retrieve
from eWRT.ws.WebDataSource import WebDataSource
from eWRT.ws.bigquery import jwt_session


API_URL = 'https://www.googleapis.com/bigquery/v2/projects/%s/queries' % BIG_QUERY_PROJECT_ID
JOB_API_URL = 'https://www.googleapis.com/bigquery/v2/projects/%s/queries/%s'
MODULE = 'bigqueryWS'


class BigQuery(WebDataSource):
    def __int__(self):
        super(BigQuery, self).__init__()

    @jwt_session.inject
    def search(self, search_terms, page_size=None, session=None):
        assert session is not None
        auth_key, auth_value = session.get_header_item()
        headers = {
            auth_key: auth_value,
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        payload = self._build_query_payload(search_terms, page_size)
        return self._retrieve_paged(payload, headers, page_size)

    @staticmethod
    def _build_query_payload(query, page_size):
        # TODO optional params
        payload = {
            'kind': 'bigquery#queryRequest',
            'query': query
        }
        if page_size is not None:
            payload['maxResults'] = page_size
        return json.dumps(payload)

    @staticmethod
    def _retrieve_simple(url, payload, headers):
        with Retrieve(MODULE) as retrieve:
            response = retrieve.open(url, payload, headers)
        return json.loads(response.read())

    @staticmethod
    def _build_page_endpoint(project_id, job_id):
        return JOB_API_URL % (project_id, job_id)

    @staticmethod
    def _build_page_query(endpoint, page_token, page_size):
        return endpoint + '?pageToken=%s&maxResults=%d' % (page_token, page_size)

    @staticmethod
    def _retrieve_paged(payload, headers, page_size):
        # TODO error handling
        result = BigQuery._retrieve_simple(API_URL, payload, headers)
        project_id = result['jobReference']['projectId']
        job_id = result['jobReference']['jobId']
        page_token = result.get('pageToken')
        while page_token:  # todo incorporate jobComplete
            page_endpoint = BigQuery._build_page_endpoint(project_id, job_id)
            page_query = BigQuery._build_page_query(page_endpoint, page_token, page_size)
            page = BigQuery._retrieve_simple(page_query, None, headers)
            result['rows'] += page['rows']
            page_token = page.get('pageToken')
            project_id = result['jobReference']['projectId']
            job_id = result['jobReference']['jobId']
        result['jobComplete'] = True
        return result


class BigQueryTest(unittest.TestCase):
    def setUp(self):
        self._bq = BigQuery()

    def test_main(self):
        test_query = """
            SELECT Actor1CountryCode, e1, Actor2CountryCode, Year, COUNT(*) c, RANK() OVER(PARTITION BY YEAR ORDER BY c DESC) rank
            FROM (SELECT Actor1CountryCode, EventCode e1, Actor2CountryCode, Year FROM [gdelt-bq:gdeltv2.events] WHERE Actor1CountryCode < Actor2CountryCode AND MonthYear < 201503),
                 (SELECT Actor2CountryCode Actor1CountryCode, EventCode e2, Actor1CountryCode Actor2CountryCode, Year FROM [gdelt-bq:gdeltv2.events] WHERE Actor1CountryCode > Actor2CountryCode),
            WHERE Actor1CountryCode IS NOT null AND
                  Actor2CountryCode IS NOT null AND
                  e1 in ("190", "191", "192", "193", "194", "1951", "1952", "196")
            GROUP EACH BY 1, 2, 3, 4
            HAVING c > 50;"""
        result = self._bq.search(test_query, page_size=20)
        self.assertIsNotNone(result)
        self.assertEqual(len(result['rows']), 46)
        print result


if __name__ == '__main__':
    unittest.main()
    bq = BigQuery()
