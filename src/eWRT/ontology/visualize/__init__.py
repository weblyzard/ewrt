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

NS_RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
NS_WL   = Namespace("http://www.weblyzard.com/2005/03/31/wl#")

RELATION_PREDICATES = ('rdfs:subClassOf', 'wl:isRelatedTo', 'wl:modifierOf','wl:social', 'wl:deleted')


class Output(object):
    """ abstract webLyzard ontology visualization superclass """
    
    def __init__(self, ontology):
        self.ontology = ontology if isinstance( ontology, Graph ) else Graph().parse( ontology)
        
    @staticmethod
    def _buildSparqlQuery():
        constraints = [ "{ ?c1 %s ?c2; ?p ?c2; rdfs:label ?s. ?c2 rdfs:label ?o. }" % p for p in RELATION_PREDICATES ]
        return "SELECT ?s ?p ?o WHERE { %s }" % " UNION ".join( constraints )
    
    @staticmethod
    def _getFilename(fname, ext):
        """ returns a filename with the new extension
            @param[in] fname original fname
            @param[in] ext - new extension
        """
        return splitext(fname)[0]+"."+ext if "." in fname else fname+"."+ext
        

    def getOntologyStatements(self):
        """ @param[in] ontology
            @returns A list of type [(s,p,o), (s,p,o)] for all statements in the ontology
        """
        q = Output._buildSparqlQuery()
        return [ (s,p,o) for s,p,o in self.ontology.query( q, initNs=dict(rdfs=NS_RDFS, wl=NS_WL) ) ]
    
    def __str__(self):
        """ returns the visualization in the given format """
        raise NotImplemented
    
class SubjectObjectPairOutput(Output):
    
    def __str__(self):
        return "\n".join( ["%s,%s" % (s,o) for s,p,o in self.getOntologyStatements() ] )    


class GraphvizVisualize(Output):
    """ Provides graphviz visualizations of webLyzard ontology """
    
    WL_PREDICATE_MAPPING = {u'subClassOf': "[]",
                            u'isRelatedTo': '[style="dashed", dir="none", label="r"]',
                            u'modifierOf':  '[style="dashed", label="m"]',
                            u'deleted'   :  '[style="dotted", arrowhead="invempty"]',
                            u'social'    :  '[style="bold", dir="none"]'
                            }
    GRAPHVIZ_HEADER = """
        rotate="90"
        size="10.8,7.4"
        center=""
        overlap=false
        splines=true
        minsep="1.5"
    """
    
    def mapPredicate(self, p):
        """ maps a predicate to a graphviz link label
            @param[in] p
            @returns the link label [...]
        """
        wl_predicate_type = p.split("#")[1]
        return GraphvizVisualize.WL_PREDICATE_MAPPING[ wl_predicate_type ]
    
        
    def __str__(self):
        stmts = self.getOntologyStatements()
        conceptDefinitions  = [ '"%s" [ label="%s" ]' % (c,c) 
                               for c in set( chain( map(itemgetter(0), stmts), map(itemgetter(2), stmts) ) ) ]
        relationDefinitions = ['"%s" -> "%s" %s' % (s,o,self.mapPredicate(p)) for s,p,o in stmts ]
        
        return "digraph G{%s\n%s\n\n%s\n}" % (GraphvizVisualize.GRAPHVIZ_HEADER,
                                               "\n".join(conceptDefinitions), "\n".join(relationDefinitions) )

    def createImage(self, fname, format):
        """ creates an image based on the ontology 
            @param[in] fname  ... output file name 
            @param[in] format ... image format (such as eps, png) to use
        """
        open(Output._getFilename(fname, "dot"), "w").write( str(self) )
        getoutput('fdp -T%s %s.dot -Elen=0.1 -Eweight=3  -Gmindist=0.05 -Nmargin="0.0,0.0" -Nfontname="Helvetica" -Nheight=0.6 -Nwidth=1.1 -Nfontsize=15 -Goverlap="4:" -Goutputorder="edgesfirst" -Gsplines="true" -Gratio=0.7 -o%s.%s' % (format, fname, fname, format) )


class TestVisualizationClass(object):

    def testGetFname(self):
        assert Output._getFilename("test", "rdf") == "test.rdf"
        assert Output._getFilename("test.rdf", "dot") == "test.dot"


if __name__ == '__main__':
    g = GraphvizVisualize('./test/test.rdf')
    g.createImage( "test.rdf", "png" )

