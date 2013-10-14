#!/usr/bin/env python

"""
::package eWRT.ws.conceptnet.util
Provides utils and shortcuts for using ConceptNet

::author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
"""
from logging import getLogger, FileHandler, Formatter, INFO
from time import strftime
from operator import itemgetter

from eWRT.util.cache import MemoryCached
from eWRT.stat.language import STOPWORD_DICT
from eWRT.stat.string import VectorSpaceModel
from eWRT.ws.conceptnet import CONCEPTNET_BASE_URL
from eWRT.ws.conceptnet.lookup_result import LookupResult


LOGGER = getLogger("eWRT.ws.conceptnet.util")
LOGGER.setLevel(INFO)

hdlr = FileHandler("eWRT.ws.conceptnet.util.%s.log" % (strftime("%Y-%m-%d_%H%M")))
hdlr.setFormatter(Formatter('%(asctime)s %(levelname)s %(message)s'))
LOGGER.addHandler(hdlr)

VALID_LANGUAGES = ('en', )
# only allow hypernym, hyponym and synonym relations for senses
VALID_SENSE_FILTER = [(u'rel', u'/r/IsA'), (u'rel', u'/r/Synonym'), (u'rel', u'/r/InstanceOf')]
# requires at least 4 levels to describe the sense 
# (e.g. /c/en/senes/x while /c/en/dog would fail this criteria)
MIN_SENSE_SPECIFICITY = 3

#MAX_CONTEXT_COUNT_SENSES = 100

def ground_term(term, input_context, pos_tag = None, stopword_list=STOPWORD_DICT['en'], limit=1):
    '''
    Grounds the given term to a ConceptNet url

    ::param term: the input term ground
    ::param input_context: a list of context terms used for the grounding
    ::param pos_tag: an optional pos_tag
    ::param limit: maximum number of concepts to return

    ::return: the ConceptNet url for the given input term
    '''
    context_vector = VectorSpaceModel(input_context)
    lookup_result = LookupResult(term=term, pos_tag=pos_tag)
    lookup_result.apply_language_filter(VALID_LANGUAGES)
    lookup_result.apply_edge_filter(VALID_SENSE_FILTER)
    
    senses = lookup_result.get_senses()
    LOGGER.info("Disambiguating senses for term '%s'" % (term.encode("utf8")))

    result = []
    for no, sense in enumerate(senses):
        if sense.specificity() < MIN_SENSE_SPECIFICITY:
            LOGGER.warn('Scipping sense #%d for %s: %s - to low specificity' % (no, term, sense.url.encode("utf8")))
            continue 

        sense_context = get_textual_data(sense, VALID_LANGUAGES, stopword_list)
        #if '/c/en/look_at' in sense.url:
        #    print context_result.edges
        #    print sense, "&", ", ".join(sense_context.keys())

        try:
            current_sim_score = context_vector * VectorSpaceModel(sense_context)
        except ZeroDivisionError:
            # ignore empty contexts (e.g. due to words removed by the stopword_list)
            continue
        
        result.append( (sense, current_sim_score) )

    return sorted(result, key=itemgetter(1), reverse=True)[:limit]


@MemoryCached(10000)
def get_textual_data(sense, valid_languages, stopword_list):
    '''
    ::returns: a vector space representation of the given concept
    '''
    context_result = LookupResult(conceptnet_url=CONCEPTNET_BASE_URL+"/"+sense.url.encode("utf8"), strict=True)
    context_result.apply_language_filter(valid_languages) 
    LOGGER.info("Found %d assertions for sense '%s'." % (len(context_result.edges), sense) )
    return context_result.get_vsm(stopword_list)


if __name__ == '__main__':
    ground_term('lord', ['hallo'])
