#!/usr/bin/env python
"""
 @package eWRT.ontology.eval.terminology
"""

# (C)opyrights 2010 by Albert Weichselbraun <albert@weichselbraun.net>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from eWRT.stat.coherence import Coherence, DiceCoherence, PMICoherence
from rdflib.Graph import Graph
from rdflib import Namespace

NS_RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
NS_WL   = Namespace("http://www.weblyzard.com/2005/03/31/wl#")

RELATION_PREDICATES = ('rdfs:subClassOf', 'wl:isRelatedTo', 'wl:modifierOf')

class CoherenceEvaluator(object):

    def __init__(self, metric):
        assert isinstance(metric, Coherence)
        self.metric = metric

    @staticmethod
    def _buildSparqlQuery():
        constraints = [ "{ ?c1 %s ?c2; rdfs:label ?s. ?c2 rdfs:label ?o. }" % p for p in RELATION_PREDICATES ]
        return "SELECT ?s ?o WHERE { %s }" % " UNION ".join( constraints )

    def getWeakConcepts(self, ontologyFile):
        """ returns a list of weak concepts according to the given coherence measure 
            @param[in] ontologyFile ... a rdf file containing the concepts 
            @returns a list of "weak" concepts
        """
        rdf = Graph().parse( ontologyFile )
        q   = CoherenceEvaluator._buildSparqlQuery()

        conceptEval = [ (self.metric.getTermCoherence(s,o), s, o) \
            for s, o in rdf.query( q, initNs=dict(rdfs=NS_RDFS, wl=NS_WL) ) ]

        conceptEval.sort()
        return conceptEval


class TestTermEval(object):

    TEST_ONTOLOGY = './test/test.rdf'
    
    def testSparqlQueryGeneration(self):
        """ tests the generation of Sparql queries """
        referenceQuery = "SELECT ?s ?o WHERE { { ?c1 rdfs:subClassOf ?c2; rdfs:label ?s. ?c2 rdfs:label ?o. } UNION { ?c1 wl:isRelatedTo ?c2; rdfs:label ?s. ?c2 rdfs:label ?o. } UNION { ?c1 wl:modifierOf ?c2; rdfs:label ?s. ?c2 rdfs:label ?o. } }"
        print referenceQuery
        print "--"
        print CoherenceEvaluator._buildSparqlQuery()
        assert( CoherenceEvaluator._buildSparqlQuery() == referenceQuery )

    def testEvaluateTerminology(self):
        """ tests an ontology (file) and returns a list of 
            weak concepts """

        t = CoherenceEvaluator( )
        # assert isinstance( t.getWeakConcepts( self.TEST_ONTOLOGY ), list )
        

if __name__ == '__main__':
    from eWRT.ws.yahoo import Yahoo
    # c = PMICoherence( dataSource = Yahoo() )
    c = DiceCoherence( dataSource = Yahoo() )
    t = CoherenceEvaluator( c )
    weak = t.getWeakConcepts( "./test/test.rdf" ) 
    print weak
    print "---"
    print "\n".join( ( str(w) for w in weak ) )


