#!/usr/bin/env python
'''
 @package eWRT.ws.stat.string
 String statistics such as
  * word similarity
  * levenshtein distance
  * soundex
  * ...
'''

# (C)opyrights 2010 by Albert Weichselbraun <albert@weichselbraun.net>
#                   and others (as outlined in the functions).
#
# The code published in this module is either under the GNU General
# Public License (see below) or under the license specified in the 
# function. 
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
from itertools import izip_longest
from operator import mul, itemgetter
from collections import Counter
from numpy import vdot
from numpy.linalg import norm

from eWRT.util.cache import MemoryCached
from eWRT.lib.thirdparty.advas.phonetics import caverphone, metaphone, nysiis

def wordSimilarity(s1, s2, similarityMeasure):
    ''' computes the given similarity metric on a strings
        words.
        e.g. wordSimilarity("nuclear energy", "energy nuclear", lev) = 0
        
        missing words are replaced by ""
        e.g. wordSimilarity("as you thought", "you thought") ==
               wordSimilarity("as you thought", "you thought", "") 
        
    '''
    wordList = list( izip_longest(s1.split(), s2.split(), fillvalue="") )
    words1, words2 = map(itemgetter(0), wordList), map(itemgetter(1), wordList)
    assert len(words1) == len(words2)
    
    score = float(sum([min([similarityMeasure(w1, w2) for w1 in words1]) 
                 for w2 in words2])) / len(words1)
    return score
    
@MemoryCached
def lev(s1, s2):
    ''' Levenshtein string edit distance
        source: 
        http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python
    '''
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

@MemoryCached
def damerauLev(seq1, seq2):
    '''
    Calculate the Damerau-Levenshtein distance between sequences.
    source : http://mwh.geek.nz/2009/04/26/python-damerau-levenshtein-distance/
    license: MIT license
    

    This distance is the number of additions, deletions, substitutions,
    and transpositions needed to transform the first sequence into the
    second. Although generally used with strings, any sequences of
    comparable objects will work.

    Transpositions are exchanges of *consecutive* characters; all other
    operations are self-explanatory.

    This implementation is O(N*M) time and O(M) space, for N and M the
    lengths of the two sequences.

    >>> dameraulevenshtein('ba', 'abc')
    2
    >>> dameraulevenshtein('fee', 'deed')
    2

    It works with arbitrary sequences too:
    >>> dameraulevenshtein('abcd', ['b', 'a', 'c', 'd', 'e'])
    2
    '''
    # codesnippet:D0DE4716-B6E6-4161-9219-2903BF8F547F
    # Conceptually, this is based on a len(seq1) + 1 * len(seq2) + 1 matrix.
    # However, only the current and two previous rows are needed at once,
    # so we only store those.
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        # Python lists wrap around for negative indices, so put the
        # leftmost column at the *end* of the list. This matches with
        # the zero-indexed strings and saves extra calculation.
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
            # This block deals with transpositions
            if (x > 0 and y > 0 and seq1[x] == seq2[y - 1]
                and seq1[x-1] == seq2[y] and seq1[x] != seq2[y]):
                thisrow[y] = min(thisrow[y], twoago[y - 2] + 1)
    return thisrow[len(seq2) - 1]

@MemoryCached
def soundex(name, length=4):
    ''' soundex module conforming to Knuth's algorithm
        implementation 2000-12-24 by Gregory Jorgensen

        source : http://code.activestate.com/recipes/52213-soundex-algorithm/
        license: public domain
    '''

    # digits holds the soundex values for the alphabet
    digits = '01230120022455012623010202'
    sndx = ''
    fc = ''

    # translate alpha chars in name to soundex digits
    for c in name.upper():
        if c.isalpha():
            if not fc: fc = c   # remember first letter
            d = digits[ord(c)-ord('A')]
            # duplicate consecutive soundex digits are skipped
            if not sndx or (d != sndx[-1]):
                sndx += d

    # replace first digit with first alpha character
    sndx = fc + sndx[1:]

    # remove all 0s from the soundex code
    sndx = sndx.replace('0','')

    # return soundex code padded to length characters
    return (sndx + (length * '0'))[:length]


class VectorSpaceModel:
    ''' a class used for vector space representations '''

    def __init__(self, tokens, binary=False):
        if not binary:
            self.v = self._addTokens(tokens)
        else:
            self.v = self._binaryAddTokens(tokens)
        
    def _addTokens(self, tokens):
        ''' adds the tokens to a vsm representation '''
        return Counter(tokens)
    
    def _binaryAddTokens(self, tokens):
        ''' adds tokens to a binary vsm representation '''
        return Counter(set(tokens))

    def __str__(self):
        return str(self.v)

    @staticmethod
    def createVSMRepresentation(v1, v2):
        ''' creates the VSM representation for the two vectors
            to compare '''
        complete_token_list = set(v1.keys() + v2.keys())
        vsm1 = [v1[k] for k in complete_token_list]
        vsm2 = [v2[k] for k in complete_token_list] 
        return vsm1, vsm2

    def __mul__(self, o):
        ''' returns the dot-product of two vectors '''
        v1, v2 = self.createVSMRepresentation(self.v, o.v)        
        return vdot(v1, v2) / (norm(v1) * norm(v2))

# --------------------------------------------------------------------
# UNITTESTS
# --------------------------------------------------------------------

from unittest import TestCase

def testMetaPhone():
    ''' compares output produced by the advas metaphone
        module with the postgres fuzzymatch functions
        @warning: the used metaphone implementation _does not_ correspond
                  to the one used in postgresql.
     '''
    from warnings import warn
    warn("the used metaphone implementation _does not_ correspond to the one use in postgres")
    print metaphone('Microprocessor')
    assert metaphone('Albert') == 'albrt'
    assert metaphone('John') == 'jhn'
    assert metaphone('Microprocessor') == 'mkrprksr'
    
def testNysiis():
    ''' tests the New York State Identification and Intelligence
        Algorithm (NYSIIS) code for the given term '''
    print nysiis("Microprocessor")
    assert nysiis("Albert").lower() == 'albard'
    
def testCaverphone():
    ''' tests the caverphone algorithm '''
    print caverphone("Albert")
    assert caverphone("Albert") == "APT1111111"
     

def testSoundex():
    ''' compares the output of the soundex algorithm with
        the output provided by postgres '''
    assert soundex("Knuth") == "K530"
    assert soundex("Weichselbraun") == "W224"
    assert soundex("Smith") == "S530"
    assert soundex("Albert") == "A416"

    assert soundex("Weichselbraun",8) == "W2241650"
    

def testWordSimilarity():
    ''' tests the per word similarity '''
    assert wordSimilarity("Ana Toth", "Toth Ana", lev) == 0
    assert wordSimilarity("Anna Toth", "Toth Ana", lev) == 0.5

    assert wordSimilarity("Anna Toth", "Toht Ana", lev) == 3./2
    assert wordSimilarity("Anna Toth", "Toht Ana", damerauLev) == 1.0


def testLevenshteinDistance():    
    assert lev("anton", "ana") == 3
    assert lev("anna", "ana") == 1
    assert lev("alfred", "alfred") == 0
    assert lev("tothi", "alfredKurz") == 10
    assert lev("maria", "marion") == 2
    assert lev("safety measures", "safety measures") == 0
    
def testDamerauLev():
    ''' tests the Damerau-Levenshtein distance
        http://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance 
    '''
    assert damerauLev("jump", "jupm") == 1
    assert damerauLev("julius", "julius") == 0
    assert damerauLev("the city of perth", "") == len("the city of perth")
    assert damerauLev("the city of perth", "teh city of perht") == 2


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
        

        
