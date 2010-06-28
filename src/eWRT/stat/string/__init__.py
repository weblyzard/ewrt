#!/usr/bin/env python
"""
 @package eWRT.ws.stat.string
 String statistics
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
#
import math
from operator import mul
from collections import defaultdict

# define some basic mathematical functions
dot=lambda x,y: map(mul, x, y)

def lev(s1, s2):
    """ Levenshtein string edit distance
        source: 
        http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python
    """
    if len(s1) < len(s2):
        return lev(s2, s1)
    if not s1:
        return len(s2)
 
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]


class VectorSpaceModel:
    """ a class used for vector space representations """

    def __init__(self, tokens, binary=False):
        if not binary:
            self.v = self._addTokens(tokens)
        else:
            self.v = self._binaryAddTokens(tokens)
        
    def _addTokens(self, tokens):
        """ adds the tokens to a vsm representation """
        v = defaultdict(int)
        for t in tokens:
            v[t] +=1
        return v
    
    def _binaryAddTokens(self, tokens):
        """ adds tokens to a binary vsm representation """
        v = defaultdict(int)
        for t in tokens:
            v[t] =1
        return v

    @staticmethod
    def createVSMRepresntation(v1, v2):
        """ creates the VSM representation for the two vectors
            to compare """
        common_token_list = set( v1.keys() + v2.keys() )

        vsm1 = [ v1[k] for k in common_token_list ]
        vsm2 = [ v2[k] for k in common_token_list ]
        return vsm1, vsm2

    def __mul__(self, o):
        """ returns the dot-product of two vectors """
        v1, v2 = self.createVSMRepresntation(self.v, o.v)        
        return float(sum(dot(v1, v2) )) / float( math.sqrt(sum(dot(v1,v1))) * math.sqrt(sum(dot(v2,v2))) ) 
        


# unittests

def testLevenshteinDistance():    
    assert lev("anton", "ana") == 3
    assert lev("anna", "ana") == 1
    assert lev("alfred", "alfred") == 0
    assert lev("tothi", "alfredKurz") == 10
    assert lev("maria", "marion") == 2
    assert lev("safety measures", "safety measures") == 0
    
from unittest import TestCase

class TestVSM(TestCase):

    def testVSM(self):
        v1 = VectorSpaceModel( ('albert', 'jasna', 'perth') )
        v2 = VectorSpaceModel( ('perth', 'jasna', 'parik') )
        self.assertAlmostEqual(v1 * v1, 1.0)
        self.assertAlmostEqual(v2 * v2, 1.0)

        print "***",v1 * v2
        self.assertAlmostEqual(v1 * v2, 2/3.)

    def testBinaryVersusStandardVSM(self):
        v1 = VectorSpaceModel( ('perth', 'perth', 'jasna'), binary=False)
        v2 = VectorSpaceModel( ('perth', 'jasna', 'jasna'), binary=False )
        v3 = VectorSpaceModel( ('perth', 'perth', 'jasna'), binary=True)
        v4 = VectorSpaceModel( ('perth', 'jasna', 'jasna'), binary=True )

        self.assertAlmostEqual(v1*v2, 4/5.)
        self.assertAlmostEqual(v3*v4, 1.0)
        

        
