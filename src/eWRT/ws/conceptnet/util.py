#!/usr/bin/env python

"""
::package eWRT.ws.conceptnet.util
Provides utils and shortcuts for using ConceptNet

::author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
"""

from eWRT.ws.conceptnet.lookup_result import LookupResult


def ground_term(term, input_context, pos_tag = None):
    '''
    Grounds the given term to a ConceptNet url

    ::param term: the input term ground
    ::param input_context: a list of context terms used for the grounding
    ::param pos_tag: an optional pos_tag

    ::return: the ConceptNet url for the given input term
    '''
    lookup_result = LookupResult(term=term, pos_tag=pos_tag)
    for sense in lookup_result.get_senses():
        print sense   



