#!/usr/bin/env python

""" ontology-stats.py
    computes the top overlapping concepts of ontologies """
from __future__ import division
from builtins import map
from past.utils import old_div
from glob import glob
from os import path
from bz2 import BZ2File
from rdflib import Namespace
from collections import defaultdict
from itertools import zip_longest
from operator import itemgetter
from csv import writer

from eWRT.input.conv.cxl import XCL2RDF
from eWRT.input.clean.text import *
from eWRT.stat.string.spelling import SpellSuggestion


# a directory containing all cxl ontology files
# ONTOLOGY_DIR = "/home/albert/data/ac/research/inwork/pakdd2011-ontology-evaluation/data/ontologies/risk/week2"

# required namespaces
NS_RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
NS_WL   = Namespace("http://www.weblyzard.com/2005/03/31/wl#")

# cleanup pipeline
CUSTOM_RISK_CORPUS = "risk-corpus.text.bz2"
s = SpellSuggestion()
s.verbose=True
s.train( SpellSuggestion.words( BZ2File( CUSTOM_RISK_CORPUS ).read() ) )

# compile cleanup queue

strCleanupPipe = (lambda s:s.replace(u'\xd7', " "), str.lower, RemovePossessive(), FixDashSpace() )
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
    return conceptCounts, relationCounts


def computeOntologyStatistics( ff, cc, rc, ccCutOffCount, rcCutOffCount):
    """ computes per ontology statistics (R, P, F1)
        @param[in] ff list of ontology files
        @param[in] cc concept counts dictionary
        @param[in] rc relation counts dictionary
        @param[in] ccCutOffCount min cc required for a term to be considered
        @param[in] rcCutOffCount min cc required for a term to be considered
    """
    goldStandardConcepts  = set([ c for c, cnt in list(cc.items()) if cnt >= ccCutOffCount ])
    goldStandardRelations = set([ r for r, cnt in list(rc.items()) if cnt >= rcCutOffCount ])
    c = open("ontology-stats.csv", "w")
    w = writer(c) 
    w.writerow( ("ontology", "concept precision", "concept recall", "concept F1", 
                                "relation precision", "relation recall", "relation F1") )

    for f in ff:
       concepts  = set(map(str, extractConceptSet( XCL2RDF.toRDF(open(f).read() ))))
       relations = set(map(str, extractRelationSet(XCL2RDF.toRDF(open(f).read() ))))

       cPrecision = len(goldStandardConcepts.intersection( concepts ))/float( len(concepts) )
       cRecall    = len(goldStandardConcepts.intersection( concepts ))/float( len(goldStandardConcepts) )
       if (cPrecision + cRecall) == 0.:
           cF1 = "NaN"
       else:
           cF1        = old_div(2 * cPrecision * cRecall, (cPrecision + cRecall))

       rPrecision = len(goldStandardRelations.intersection( relations ))/float( len(relations) )
       rRecall    = len(goldStandardRelations.intersection( relations ))/float( len(goldStandardRelations) )
       if (rPrecision + rRecall) == 0.:
           rF1 = "NaN"
       else:
           rF1        = old_div(2 * rPrecision * rRecall, (rPrecision + rRecall))

       w.writerow( (path.basename(f), cPrecision, cRecall, cF1, rPrecision, rRecall, rF1) )

    c.close()

   
def csvOutput( termCnt, relCnt ):
    f = open("terminology-stats.csv", "w")
    w = writer(f) 

    w.writerow( ("terms", "termCnt", "relation", "relationCnt") )
    for row1, row2 in zip_longest( sorted( list(termCnt.items()), key=itemgetter(1), reverse=True ), \
                             sorted( list(relCnt.items()), key=itemgetter(1), reverse=True), fillvalue=('','')) :
        w.writerow( row1+row2 )


# main
if __name__ == '__main__':
    cc, rc = computeStatistics( glob(ONTOLOGY_DIR +"/*.cxl") )
    computeOntologyStatistics( glob(ONTOLOGY_DIR +"/*.cxl"), cc, rc, 
                               ccCutOffCount=4, rcCutOffCount=3 )
