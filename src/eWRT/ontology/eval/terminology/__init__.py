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

import sys

from rdflib.Graph import Graph

class CoherenceEvaluator(object):

    def getWeakConcepts(self, ontologyFile):
        """ returns a list of weak concepts according to the given coherence measure 
            @param[in] ontologyFile ... a rdf file containing the concepts 
            @returns a list of "weak" concepts
        """
        rdf = Graph().parse( ontologyFile )
        for s,p,o in rdf:
            print s, "->", o



class TestTermEval(object):

    TEST_ONTOLOGY = './test/test.rdf'
    
    def __init__(self):
        pass

    def testEvaluateTerminology(self):
        """ tests an ontology (file) and returns a list of 
            weak concepts """

        t = CoherenceEvaluator( )
        assert isinstance( t.getWeakConcepts( self.TEST_ONTOLOGY ), list )
        

if __name__ == '__main__':
    t = CoherenceEvaluator()
    t.getWeakConcepts( "./test/test.rdf" )


