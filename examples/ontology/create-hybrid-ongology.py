#!/usr/bin/env python

""" create-hybrid-ontology.py

    input: (a) source ontologies
           (b) important concept list

    output: an ontology containing all relations between the
            important concepts which have been found in the 
            source ontology.
"""

from glob import glob
from os import path
from bz2 import BZ2File

from eWRT.input.conv.cxl import XCL2RDF
# ontology cleanup
from eWRT.input.clean.text import *
from eWRT.stat.string.spelling import SpellSuggestion

from rdflib import Namespace, ConjunctiveGraph, Literal
from collections import defaultdict
from itertools import izip_longest
from operator import itemgetter
from csv import writer

# a directory containing all cxl ontology files
ONTOLOGY_DIR            = "/home/albert/data/ac/research/inwork/pakdd2011-ontology-evaluation/data/ontologies/risk/week8"
IMPORTANT_CONCEPTS_LIST = "top-terms.text"

# required namespaces
NS_RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
NS_WL   = Namespace("http://www.weblyzard.com/2005/03/31/wl#")

# cleanup pipeline
CUSTOM_RISK_CORPUS = "risk-corpus.text.bz2"
s = SpellSuggestion()
s.verbose=True
s.train( SpellSuggestion.words( BZ2File( CUSTOM_RISK_CORPUS ).read() ) )

# compile cleanup queue

strCleanupPipe = (lambda s:s.replace(u'\xd7', " "), unicode.lower, RemovePossessive(), FixDashSpace() )
phrCleanupPipe = (SplitEnumerations(), SplitMultiTerms(), SplitBracketExplanations() )
fs = FixSpelling(s)
wrdCleanupPipe = (fs, RemovePunctationAndBrackets(),)
phraseCleanup = PhraseCleanup(strCleanupPipe, phrCleanupPipe, wrdCleanupPipe )


def extractSPO(rdfOntology):
    """ extracts a set of all relations present in the given ontology
        @param[in] rdfOntology    the rdflib.Graph object representing the ontology
        @returns a set of all triples present in the given ontology 
    """
    q = "SELECT ?s ?p ?o WHERE { ?cs ?cp ?co. ?cs rdfs:label ?s. ?co rdfs:label ?o. ?cp rdfs:label ?p. }"
    rel = set()
    for ss, pp, oo in rdfOntology.query( q, initNs=dict(rdfs=NS_RDFS, wl=NS_WL) ):
        rel = rel.union( [ (s, p, o) for s in phraseCleanup.clean(ss) for p in phraseCleanup.clean(pp) for o in phraseCleanup.clean(oo) ] )
    return rel

def extractConceptSet(rdfOntology):
    """ extracts a set of all concepts present in the given ontology
        @param[in] rdfOntology    the rdflib.Graph object representing the ontology
        @returns a set of all concepts present in the given ontology 
    """
    concepts = set()
    concepts = concepts.union( [ s for s, p, o in extractSPO(rdfOntology) ] )
    concepts = concepts.union( [ o for s, p, o in extractSPO(rdfOntology) ] )
    return concepts

def extractRelationSet(rdfOntology):
    """ extracts a set of all relations present in the given ontology
        @param[in] rdfOntology    the rdflib.Graph object representing the ontology
        @returns a set of all relations present in the given ontology 
    """
    return set( [ p for s, p, o in extractSPO(rdfOntology) ] )

getUrl = lambda x: NS_WL[ x.replace(" ", "_").replace("?", "").replace("&", "&amp;") or "xxx" ]

def computeHybridOntology( ff, topConcepts ):
    """ computes the hybrid ontology
        @param[in] ff list of input ontologies
        @param[in] topConcepts concepts which are required to participate in
                               every hybrid ontology relation
        @returns a hybrid ontology which contains all relations found in the
                 ontologies ff between concepts listed in the topConcept list
    """
    g = ConjunctiveGraph()

    allTopConcepts = set( topConcepts )
    usedTopConcepts = set()

    for f in ff:
       for s, p, o in extractSPO( XCL2RDF.toRDF(open(f).read() ) ):
          if s in allTopConcepts and o in allTopConcepts:
              g.add( (getUrl(s), NS_RDFS['label'], Literal(s)) )
              g.add( (getUrl(p), NS_RDFS['label'], Literal(p)) )
              g.add( (getUrl(o), NS_RDFS['label'], Literal(o)) )
              g.add( (getUrl(s), getUrl(p), getUrl(o)) )
              usedTopConcepts.add( s )
              usedTopConcepts.add( o )

    _addUseCaseSpecificUnusedConcepts(g)
    with open("hybrid-graph.rdf", "w") as f:
        f.write( g.serialize() )

    unusedConcepts = allTopConcepts.difference( usedTopConcepts )
    print "# of unused concepts: %d" % len( unusedConcepts ) 
    print ", ".join( list(unusedConcepts) )


def _addUseCaseSpecificUnusedConcepts( g ):
    """ adds the four missing concepts from the risk management
        use case """
    g.add( (getUrl("mond indices"), NS_RDFS['label'], Literal("Mond indices")) )
    g.add( (getUrl("dow indices"), NS_RDFS['label'], Literal("DOW indices")) )
    g.add( (getUrl("flixborough"), NS_RDFS['label'], Literal("Flixborough")) )
    g.add( (getUrl("piper alpha"), NS_RDFS['label'], Literal("Piper Alpha")) )

    g.add( (getUrl("quantitative"), getUrl("related"), getUrl("mond indices")) ) 
    g.add( (getUrl("quantitative"), getUrl("related"), getUrl("dow indices")) )  
    g.add( (getUrl("events"), getUrl("related"), getUrl("flixborough")) )
    g.add( (getUrl("events"), getUrl("related"), getUrl("piper alpha")) )

# main
topConcepts = map(None, map(str.strip, open( IMPORTANT_CONCEPTS_LIST )) )
computeHybridOntology( glob(ONTOLOGY_DIR +"/*.cxl"), topConcepts )

