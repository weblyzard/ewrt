#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 02.03.2015
@author: Christian Junker
"""
QUERY_TEMPLATE = """
SELECT DATEADDED, Actor1Name, EventCode, Actor2Name, SOURCEURL FROM [gdelt-bq:gdeltv2.events]
WHERE GLOBALEVENTID IN (
    SELECT GLOBALEVENTID FROM [gdelt-bq:gdeltv2.eventmentions]
    %(language)s
    GROUP BY GLOBALEVENTID
  )
%(actor_type)s
%(location)s
%(since_day)s
%(since_time)s
ORDER BY DATEADDED DESC
%(limit)s
"""


def query_from_blocks(blocks):
    return QUERY_TEMPLATE % blocks


LANGUAGE_BLOCK = """
WHERE MentionDocTranslationInfo CONTAINS 'srclc:%s'
"""

def language_block(value):
    return LANGUAGE_BLOCK % value


ACTOR_TYPE_BLOCK = """
AND (
    Actor1Type1Code == "%(actor_type)s" OR
    Actor2Type1Code == "%(actor_type)s")
"""


def actor_type_block(value):
    return ACTOR_TYPE_BLOCK % {'actor_type': value}


LOCATION_BLOCK = """
AND (
  Actor1CountryCode == "%(location)s" OR
  Actor2CountryCode == "%(location)s")
"""


def location_block(value):
    return LOCATION_BLOCK % {'location': value}


SINCE_DAY_BLOCK = """
AND SQLDATE >= %d
"""


def since_day_block(value):
    return SINCE_DAY_BLOCK % value


SINCE_TIME_BLOCK = """
AND DATEADDED >= %d
"""


def since_time_block(value):
    return SINCE_TIME_BLOCK % value


LIMIT_BLOCK = """
LIMIT %d
"""


def limit_block(value):
    return LIMIT_BLOCK % value
