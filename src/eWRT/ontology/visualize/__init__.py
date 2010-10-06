#!/usr/bin/env python
"""
 @package eWRT.ontology.visualize
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

#from eWRT.stat.coherence import Coherence, DiceCoherence, PMICoherence
from rdflib.Graph import Graph
from rdflib import Namespace

from commands import getoutput
from itertools import chain
from operator import itemgetter
from os.path import splitext

from tempfile import NamedTemporaryFile


NS_RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
NS_WL   = Namespace("http://www.weblyzard.com/2005/03/31/wl#")

RELATION_PREDICATES = ('rdfs:subClassOf', 'wl:isRelatedTo', 'wl:modifierOf', 'wl:social', 'wl:deleted')

# ontology cleanup
from eWRT.input.clean.text import *

strCleanupPipe = (lambda s:s.replace(u'\xd7', " "), RemovePossessive(), FixDashSpace() )
phrCleanupPipe = (SplitEnumerations(), SplitMultiTerms(), SplitBracketExplanations() )
wrdCleanupPipe = (RemovePunctationAndBrackets(),)
phraseCleanup = PhraseCleanup(strCleanupPipe, phrCleanupPipe, wrdCleanupPipe )

class OutputQueries(object):
    """ @class OutputQueries
        static class which collects all supported sparql queries
        for the ontology visualization """

    @staticmethod
    def _webLyzardSparqlQuery():
        constraints = [ "{ ?c1 %s ?c2; ?p ?c2; rdfs:label ?s. ?c2 rdfs:label ?o. }" % p for p in RELATION_PREDICATES ]
        return "SELECT ?s ?p ?o WHERE { %s }" % " UNION ".join( constraints )

    @staticmethod
    def _labeledGraphSparqlQuery():
        return "SELECT ?s ?p ?o WHERE { ?cs ?cp ?co. ?cs rdfs:label ?s. ?co rdfs:label ?o. ?cp rdfs:label ?p. }"


class Output(object):
    """ abstract webLyzard ontology visualization superclass """
    
    def __init__(self, ontology, sparqlQuery=OutputQueries._webLyzardSparqlQuery):
        """ @param[in] ontology    ... the ontology to visualize
            @param[in] sparqlQuery ... returns the sparqlQuery required to select the node names
          
            @see OutputQueries for possible sparqlQueries
        """
        self.ontology    = ontology if isinstance( ontology, Graph ) else Graph().parse( ontology)
        self.sparqlQuery = sparqlQuery
        
    def getOntologyStatements(self):
        """ @param[in] ontology
            @returns A list of type [(s,p,o), (s,p,o)] for all statements in the ontology
        """
        q = self.sparqlQuery()
        rel = set()
        for ss, pp, oo in self.ontology.query( q, initNs=dict(rdfs=NS_RDFS, wl=NS_WL) ):
            rel = rel.union( [ (s, p, o) for s in phraseCleanup.clean(ss) for p in phraseCleanup.clean(pp) for o in phraseCleanup.clean(oo) ] )
        return rel
    
    def __str__(self):
        """ returns the visualization in the given format """
        raise NotImplementedError
    
class SubjectObjectPairOutput(Output):
    
    def __str__(self):
        return "\n".join( ["%s,%s" % (s,o) for s,_,o in self.getOntologyStatements() ] )    


class GraphvizVisualize(Output):
    """ Provides graphviz visualizations of webLyzard ontology """
    
    WL_PREDICATE_MAPPING = {u'subClassOf' : "[]",
                            u'isRelatedTo': '[style="dashed", dir="none", label="r"]',
                            u'modifierOf' :  '[style="dashed", label="m"]',
                            u'deleted'    :  '[style="dotted", arrowhead="invempty"]',
                            u'social'     :  '[style="bold", dir="none"]'
                            }
    GRAPHVIZ_HEADER = """
        rotate="90"
        size="10.8,7.4"
        center=""
        overlap=false
        splines=true
        minsep="1.5"
    """
    def __init__(self, ontology, sparqlQuery=OutputQueries._webLyzardSparqlQuery):
        self.graphTitle = ""
        Output.__init__(self, ontology, sparqlQuery)
   
    def mapPredicate(self, p):
        """ maps a predicate to a graphviz link label
            @param[in] p
            @returns the link label [...]
        """
        try:
            wl_predicate_type = p.split("#")[1]
            return GraphvizVisualize.WL_PREDICATE_MAPPING[ wl_predicate_type ]
        except IndexError:
            return u'[label="%s",dir="back"]' % p

    def getTitle(self):
        """ returns the graph's title, if a title has been set """
        if not self.graphTitle:
            return ""

        return '\ngraph [ fontsize=20, label="%s", size="6,6" ];\n ' % self.graphTitle

        
    def __str__(self):
        stmts = self.getOntologyStatements()
        conceptDefinitions  = [ '"%s" [ label="%s" ]' % (c,c) 
                               for c in set( chain( map(itemgetter(0), stmts), map(itemgetter(2), stmts) ) ) ]
        relationDefinitions = ['"%s" -> "%s" %s' % (s,o,self.mapPredicate(p)) for s,p,o in stmts ]
        
        return "digraph G{%s\n%s\n\n%s\n\n\n%s\n}" % (GraphvizVisualize.GRAPHVIZ_HEADER,
                                                      self.getTitle(),
                                                      "\n".join(conceptDefinitions), "\n".join(relationDefinitions) )

    def createImage(self, fname, imgFormat):
        """ creates an image based on the ontology 
            @param[in] fname     ... output file name 
            @param[in] imgFormat ... image format (such as eps, png) to use
        """
        dotFile = NamedTemporaryFile(suffix=".dot", delete=False)
        dotFile.write( str(self) )
        dotFile.flush()

        getoutput('fdp -T%s %s -Elen=0.1 -Eweight=3  -Gmindist=0.05 -Nmargin="0.0,0.0" -Nfontname="Helvetica" -Nheight=0.6 -Nwidth=1.1 -Nfontsize=15 -Goverlap="4:" -Goutputorder="edgesfirst" -Gsplines="true" -Gratio=0.7 -o%s.%s' % (imgFormat, dotFile.name, fname, imgFormat) )


class TestVisualizationClass(object):

    def __init__(self):
        pass

if __name__ == '__main__':
    g = GraphvizVisualize('./test/test.rdf')
    g.graphTitle="Test"
    g.createImage( "test.rdf", "png" )

