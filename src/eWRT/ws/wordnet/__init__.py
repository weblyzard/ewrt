#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@package: eWRT.ws.wordnet

Convenience functions to access the NLTK WordNet interface
@author: Albert Weichselbraun

Definitions:
 (a) Term - a (potentially ambiguous) n-gram representing a unit of meaning.
 (b) Synset - a concept with a well defined meaning
 (c) Lemma - a grounded list of terms representing a certain synset
'''

from itertools import chain

from nltk.corpus.reader.wordnet import Synset
from nltk.corpus import wordnet

def get_synonmys(term):
    ''' ::return: all synonyms for the given term 
                  and all its senses. '''
    return list( _get_lemmas(term) )


def get_antonyms(term):
    ''' ::return: all antonyms for the given term and 
                  all its senses.
    '''
    return [ a for a in chain(*[ lemma.antonyms() for lemma in _get_lemmas(term) ] ) if a  ]

def get_terms( lemma_list ):
    '''
    ::return: a set of strings representing the given list of lemmas
    '''
    return set( [ lemma.name for lemma in lemma_list ] )


def _get_lemmas(term):
    ''' ::return: all lemmas for the given term '''
    if isinstance(term, Synset):
        synsets = [ term ]
    else: 
        synsets = wordnet.synsets(term)

    return ( lemma for synset in synsets for lemma in synset.lemmas )

