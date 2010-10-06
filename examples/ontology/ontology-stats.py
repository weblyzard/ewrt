#!/usr/bin/env python

""" ontology-overlap.py
    computes the top overlapping concepts of ontologies """

import os.path
from glob import glob
from bz2 import BZ2File

from eWRT.input.conv.cxl import XCL2RDF
# ontology cleanup
from eWRT.input.clean.text import *
from eWRT.stat.string.spelling import SpellSuggestion

from rdflib.Graph import Graph
from rdflib import Namespace, Literal
from collections import defaultdict
from itertools import izip_longest, chain
from operator import itemgetter
from csv import writer

# a directory containing all cxl ontology files
ONTOLOGY_DIR = "/home/albert/data/ac/research/inwork/pakdd2011-ontology-evaluation/data/ontologies/risk/week8"

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


def computeStatistics( ff ):
    """ computes the statistics (number of times a concept is used; number of 
        times a relation name is used) based on the given list of ontologies 
        @param[in] ff   a list of files containing the ontologies to be analyzed
    """

    conceptCounts = defaultdict(int)
    relationCounts = defaultdict(int)
    for f in ff:
       concepts  = set(map(str, extractConceptSet( XCL2RDF.toRDF(open(f).read() ))))
       relations = set(map(str, extractRelationSet(XCL2RDF.toRDF(open(f).read() ))))

       for c in concepts:
           conceptCounts[c] += 1

       for r in relations:
           relationCounts[r] += 1

    csvOutput( conceptCounts, relationCounts )


def csvOutput( termCnt, relCnt ):
    f = open("terminology-stats.csv", "w")
    w = writer(f) 

    w.writerow( ("terms", "termCnt", "relation", "relationCnt") )
    for row1, row2 in izip_longest( sorted( termCnt.items(), key=itemgetter(1), reverse=True ), \
                             sorted( relCnt.items(), key=itemgetter(1), reverse=True), fillvalue=('','')) :
        w.writerow( row1+row2 )


# main
computeStatistics( glob(ONTOLOGY_DIR +"/*.cxl") )
