#!/usr/bin/env python

""" import cxl files into the rdf format """
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

__version__ = "$Header$"

from xml.dom.minidom import parseString
from collections import defaultdict

from rdflib.Graph import Graph
from rdflib import Namespace, Literal

NS_WL   = Namespace("http://www.weblyzard.com/2005/03/31/wl#")
NS_RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")


class XCL2RDF(object):
    """ converts XCL  to RDF 

        @warning
        XCL2RDF will _ignore_ statements with empty s, o or p.
    """
    
    @staticmethod
    def _createResourceDictionary(dom):
        """ @param[in] dom ... dom tree to parse
            @returns a dictionary with all resource names """
        
        concepts =  [ (c.getAttribute('id'), c.getAttribute('label')) for c in dom.getElementsByTagName("concept") ]
        return dict(concepts)
        
    @staticmethod
    def _createPropertyDictionary(dom):
        """ @param[in] dom ... dom tree to parse
           @returns a dictionary with all property names """

        properties =  [ (c.getAttribute('id'), c.getAttribute('label')) for c in dom.getElementsByTagName("linking-phrase") ] 
        return dict( properties )

    @staticmethod
    def _getIdentifier(s):
        """ returns the identifier (= String in camel case) for
            the given string """
        res = "".join( [ w.capitalize() for w in s.split() ] )
        return res[0].lower()+res[1:] 

    @staticmethod
    def _addOntologyStatement( ontology, s, p, o ):
        """ adds the given statement to the ontology using the
            wl-syntax 
        """
        # ignore statements with empty s, p, or o.
        if not p or not s or not o:
            return
        
        # returns the resource's identifier
        rid = lambda r: NS_WL[ XCL2RDF._getIdentifier(r)] 
        
        # define labels
        ontology.add( (rid(s), NS_RDFS['label'], Literal(s)) )
        ontology.add( (rid(o), NS_RDFS['label'], Literal(o)) )
        ontology.add( (rid(p), NS_RDFS['label'], Literal(p)) )
    
        # add relation(
        ontology.add( (rid(s), rid(p), rid(o)) )
    
    @staticmethod
    def toRDF(text):
        """ performs the conversion and returns RDF triples """
        dom = parseString(text)
        resourceDictionary = XCL2RDF._createResourceDictionary(dom)
        propertyDictionary = XCL2RDF._createPropertyDictionary(dom)
        
        incomingConnections = defaultdict( list )
        outgoingConnections = defaultdict( list )
        for c in dom.getElementsByTagName("connection"):
            c1, c2 =  c.getAttribute('to-id'), c.getAttribute('from-id')
            if c1 in resourceDictionary:
                incomingConnections[c2].append(c1)
            else:
                outgoingConnections[c1].append(c2)
        
        rdfGraph = Graph()
        for p, s_list in incomingConnections.items():
            for s in s_list:
                for o in outgoingConnections[p]:
                    XCL2RDF._addOntologyStatement(rdfGraph, 
                                                  resourceDictionary[s],
                                                  propertyDictionary[p],
                                                  resourceDictionary[o])
                    
        return rdfGraph  
                
        
        
# unit tests    
        
def testXCL2RDF():
        """ tests the XCL2RDF class """
        txt = open("./test/test.cxl").read()
        rdfGraph = XCL2RDF.toRDF(txt)
        open("./test/result.rdf", "w").write( rdfGraph.serialize() )
    
def testGetIdentifier():
    """ tests the creation of identifiers """
    assert XCL2RDF._getIdentifier("is true") == "isTrue"
    assert XCL2RDF._getIdentifier("IS") == "is" 

def testEmptyPredicates():
    """ tests whether we are able to translate unnamed predicates """
    txt = open("./test/test_empty_concepts.cxl").read()
    rdfGraph = XCL2RDF.toRDF(txt)
    open("./test/result2.rdf", "w").write( rdfGraph.serialize() )

