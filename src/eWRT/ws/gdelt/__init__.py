#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@package eWRT.ws.gdelt

Created on 28.02.2015

@author: Christian Junker
"""
import unittest
from datetime import date, datetime
from collections import defaultdict, namedtuple

from eWRT.ws.bigquery import BigQuery
from eWRT.ws.gdelt.constants import ACTOR_TYPES, LANGUAGES, UN_COUNTRY_CODES
from eWRT.ws.gdelt.query_blocks import (
    query_from_blocks, actor_type_block,
    language_block, location_block,
    since_day_block, limit_block, since_time_block)


class Gdelt(BigQuery):
    def __init__(self):
        super(Gdelt, self).__init__()

    def search(self, search_terms, page_size=None, session=None):
        '''
        perform a gdelt search with the specified search terms
        :param GdeltQueryBuilder search_terms: the builder object holding the query params
        :param int page_size: number of rows to fetch while paging through the results
        :param JWTSession session: the oauth session to use, is automatically injected
        :return:
        '''

        if not isinstance(search_terms, GdeltQueryBuilder):
            raise ValueError('please provide a %s object' % GdeltQueryBuilder.__name__)
        # todo tonality, etc.?
        return super(Gdelt, self).search(search_terms.build(),
                                         page_size=page_size,
                                         session=session)

    @staticmethod
    def builder():
        """
        :return: a gdelt query builder object
        :rtype: GdeltQueryBuilder
        """
        return GdeltQueryBuilder()

    Row = namedtuple('Row', ['date', 'actor1', 'code', 'actor2', 'url'])

    @classmethod
    def parse_row(cls, row):
        '''
        :param dict row: the row to parse
        :return: a dict containing the invo
        :rtype: Gdelt.Row
        '''
        f = lambda idx: row[u'f'][idx][u'v']
        return cls.Row(
            date=datetime.strptime(str(f(0)), '%Y%m%d%H%M%S'),
            actor1=f(1), code=f(2), actor2=f(3), url=f(4))


class GdeltQueryBuilder(object):
    '''
    A Gdelt query builder object used in conjunction with the Gdelt WS.
    '''

    class _Constraints(object):
        @staticmethod
        def precondition(value, type, choices=None, msg=None):
            '''
            check value pre condition, i.e. matching required type and
            optionally whether it's an element of a predefined set.

            :param value: the value to check
            :param class_or_type_or_tuple type: the expected type
            :param set choices: (optional) predefined set
            :return: True if conditions are met
            :rtype: bool
            '''
            assert choices is None or isinstance(choices, (set, dict))
            return isinstance(value, type) and (choices is None or value in choices)

        @staticmethod
        def get_field(field):
            '''
            :param str field: name of the field to return
            :return: the current value of the field (defaults to empty string)
            :raises KeyError: if the field is not supported
            '''

            def _closure(self):
                ''' simple attribute getter '''
                return self._fields.get(field)

            return _closure

        @staticmethod
        def set_field(field, type, choices, block, transform=lambda _: _):
            def _closure(self, value):
                ''' simple attribute setter checking precondition '''
                assert isinstance(field, str)
                if not self._Constraints.precondition(value, type, choices):
                    raise ValueError("%s must be of type %s and element of set %s" % (field, str(type), str(choices)))
                self._fields[field] = block(transform(value))

            return _closure

        @staticmethod
        def del_field(field):
            def _closure(self):
                self._fields[field]

            return _closure

        @classmethod
        def factory(cls, field, type, choices, block, doc, transform=lambda _: _):
            return property(cls.get_field(field),
                            cls.set_field(field, type, choices, block, transform=transform),
                            cls.del_field(field),
                            doc)

    actor_type = _Constraints.factory('actor_type', str, ACTOR_TYPES, actor_type_block,
                                      '''The types of actors to include.''')

    language = _Constraints.factory('language', str, LANGUAGES, language_block,
                                    '''Which event translation language to include''')

    location = _Constraints.factory('location', str, UN_COUNTRY_CODES, location_block,
                                    '''The location to include''',
                                    transform=lambda l: l.upper())

    since_day = _Constraints.factory('since_day', date, None, since_day_block,
                                     '''The earlieast event (granularity: days)''',
                                     transform=lambda d: int(d.isoformat().translate(None, '-')))

    since_time = _Constraints.factory('since_time', datetime, None, since_time_block,
                                      '''The earlieast event (granularity: seconds)''',
                                      transform=lambda d: int(d.isoformat()
                                                                  .translate(None, '-')
                                                                  .translate(None, ':')
                                                                  .translate(None, 'T')[:14]))

    limit = _Constraints.factory('limit', int, None, limit_block,
                                 '''
                                 Maximum number of documents to include (events are
                                 ordered by date in descending order)
                                 ''')

    def __init__(self):
        ''' init '''
        self._fields = defaultdict(lambda: '')

    def reset(self):
        '''
        reset all fields.
        :return: self
        '''
        self._fields = defaultdict(lambda: '')
        return self

    def build(self):
        '''
        build the required query format based on the set fields
        :return: the query in a service dependent format (currently str)
        '''
        return query_from_blocks(self._fields)


class GdeltTest(unittest.TestCase):
    def setUp(self):
        self.builder = GdeltQueryBuilder()

    def test_builder_errors(self):
        '''
        test the error conditions for the query builder fields
        '''
        self.assertRaises(ValueError, self.builder.actor_type, 'foobar')
        self.assertRaises(ValueError, self.builder.language, 'foobar')
        self.assertRaises(ValueError, self.builder.location, 'foobar')
        self.assertRaises(ValueError, self.builder.since_day, 'foobar')
        self.assertRaises(ValueError, self.builder.limit, 'foobar')

    def test_builder_empty(self):
        '''
        test whether an empty query is build correctly
        '''
        expected_empty = """
            SELECT DATEADDED, Actor1Name, EventCode, Actor2Name, SOURCEURL FROM [gdelt-bq:gdeltv2.events]
            WHERE GLOBALEVENTID IN (
              SELECT GLOBALEVENTID FROM [gdelt-bq:gdeltv2.eventmentions]
              GROUP BY GLOBALEVENTID)
              ORDER BY DATEADDED DESC"""
        self._assert_equal_no_whitespace(self.builder.build(), expected_empty)

    def test_builder_correct(self):
        '''
        test whether the query is build correctly
        '''
        since_date = datetime.strptime('20150302', '%Y%m%d').date()
        since_time = datetime.strptime('20150302121110999999', '%Y%m%d%H%M%S%f')
        expected_full = """
            SELECT DATEADDED, Actor1Name, EventCode, Actor2Name, SOURCEURL FROM [gdelt-bq:gdeltv2.events]
            WHERE GLOBALEVENTID IN (
              SELECT GLOBALEVENTID FROM [gdelt-bq:gdeltv2.eventmentions]
              WHERE MentionDocTranslationInfo CONTAINS 'srclc:deu'
              GROUP BY GLOBALEVENTID)
            AND (
              Actor1Type1Code == "ENV" OR
              Actor2Type1Code == "ENV")
            AND (
              Actor1CountryCode == "AUT" OR
              Actor2CountryCode == "AUT" )
            AND SQLDATE >= 20150302
            AND DATEADDED >= 20150302121110
            ORDER BY DATEADDED DESC
            LIMIT 100"""
        # todo optional params
        builder = self.builder
        builder.actor_type = 'ENV'
        builder.language = 'deu'
        builder.location = 'AUT'
        builder.since_day = since_date
        builder.since_time = since_time
        builder.limit = 100
        query = builder.build()
        self._assert_equal_no_whitespace(query, expected_full)

    def _assert_equal_no_whitespace(self, first, second):
        '''
        helper method to compare query strings
        :param first: first query
        :param second: second query
        :raises: AssertionError if the two strings don't match after all whitespaces are removed
        '''
        self.assertEqual("".join(first.split()), "".join(second.split()))

    def test_call_api(self):
        '''
        test an actual call to the api
        '''
        yesterday = datetime.strptime('20150201', '%Y%m%d').date()
        builder = self.builder
        builder.actor_type = 'ENV'
        builder.language = 'deu'
        builder.location = 'DEU'
        builder.since_day = yesterday
        gdelt = Gdelt()
        self.assertRaises(ValueError, gdelt.search, 'foobar')
        result = gdelt.search(builder)
        self.assertIsNotNone(result)
        self.assertGreater(len(result['rows']), 1)


if __name__ == '__main__':
    unittest.main()
