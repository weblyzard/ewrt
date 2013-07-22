#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@package: eWRT.ws.wordnet

Convenience functions to access the NLTK WordNet interface
@author: Albert Weichselbraun
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


def _get_lemmas(term):
    ''' ::return: all lemmas for the given term '''
    if isinstance(term, Synset):
        synsets = [ term ]
    else: 
        synsets = wordnet.synsets(term)

    return ( lemma for synset in synsets for lemma in synset.lemmas )


# ------------------------------------------------------------------------------------
# Unit tests
# ------------------------------------------------------------------------------------

def test_get_antonyms():
    print get_antonyms('good') 
    
