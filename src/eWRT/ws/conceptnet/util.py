#!/usr/bin/env python

"""
::package eWRT.ws.conceptnet.util
Provides utils and shortcuts for using ConceptNet

::author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
"""
from eWRT.stat.language import STOPWORD_DICT
from eWRT.stat.string import VectorSpaceModel
from eWRT.ws.conceptnet import CONCEPTNET_BASE_URL
from eWRT.ws.conceptnet.lookup_result import LookupResult

VALID_LANGUAGES = ('en', )

def ground_term(term, input_context, pos_tag = None, stopword_list=STOPWORD_DICT['en']):
    '''
    Grounds the given term to a ConceptNet url

    ::param term: the input term ground
    ::param input_context: a list of context terms used for the grounding
    ::param pos_tag: an optional pos_tag

    ::return: the ConceptNet url for the given input term
    '''
    context_vector = VectorSpaceModel(input_context)
    lookup_result = LookupResult(term=term, pos_tag=pos_tag)
    lookup_result.apply_language_filter(VALID_LANGUAGES)
    
    best_matching_sense, best_matching_sense_sim_score = None, 0.

    for sense in lookup_result.get_senses():
        context_result = LookupResult(conceptnet_url=CONCEPTNET_BASE_URL+"/"+sense.url, strict=True)
        context_result.apply_language_filter(VALID_LANGUAGES) 
        sense_context = context_result.get_vsm(stopword_list)
        print sense, "&", ", ".join(sense_context.keys())

        current_sim_score = context_vector * VectorSpaceModel(sense_context)
        if current_sim_score >= best_matching_sense_sim_score:
            best_matching_sense_sim_score = current_sim_score
            best_matching_sense = sense

    return best_matching_sense



