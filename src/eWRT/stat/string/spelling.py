#!/usr/bin/env python
"""
 @package eWRT.ws.stat.string.spelling
 suggests spelling corrections for arbitrary terms
"""

# (C)opyrights 2010 by Albert Weichselbraun <albert@weichselbraun.net>
#                   and others (as outlined in the functions.
#
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

import re, collections
from string import ascii_lowercase
from bz2 import BZ2File
from cPickle import dump, load
from os.path import dirname, join as pjoin

from logging import getLogger
log = getLogger(__name__)

DEFAULT_MODEL = pjoin(dirname(__file__), "eWRT.stat.string.spelling.data.bz2")
valid_word_characters = ascii_lowercase+"-"

class SpellSuggestion(object):
    """
    @class SpellSuggestion
    learns a vocabulary and returns spelling suggestions for
    deviating words.

    This code is based on code presented in a tutorial written by 
    Peter Norvig <http://norvig.com/spell-correct.html>.
    """

    model = collections.defaultdict(lambda :1)

    def __init__(self, serializedModel=DEFAULT_MODEL, verbose=False):
        """
        @param[in] filename of the cPickle dump of the model
        """
        if serializedModel:
            self.model.update( load(BZ2File(serializedModel)) )

        self.verbose = verbose

    def serializeModel(self, serializedModel):
        """
        Writes the learned model to a compressed file.
        @param[in] serializedModel file name for the serialized model
        """
        f = BZ2File(serializedModel, "w")
        dump(dict(self.model), f)
        f.close()

    @staticmethod
    def words(text): return re.findall('[a-z]+', text.lower()) 

    def train(self, features):
        """ @param[in] features a list of terms to consider as correct
                                for the spell checking (including repetitions as
                                they increase a words probability to get selected
                                as spelling suggestion.
        """
        for f in features:
            self.model[f] += 1

    @staticmethod
    def edits1(word):
       splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
       deletes    = [a + b[1:] for a, b in splits if b]
       transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
       replaces   = [a + c + b[1:] for a, b in splits for c in valid_word_characters if b]
       inserts    = [a + c + b     for a, b in splits for c in valid_word_characters ]
       return set(deletes + transposes + replaces + inserts)

    def known_edits2(self, word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.model)

    def known(self, words): return set(w for w in words if w in self.model)

    def correct(self, word):
        """
        Determines whether the spelling is correct (i.e. known) and
        suggests the most likely candidate otherwise
        @param[in] word the word to check
        @returns (correct, suggestion) a tuple indicating whether the spelling is correct
                  and a suggestion for the correct spelling
        """

        # we found the word in the dictionary
        # or ignore words containing "/" and numbers
        if word in self.model:
            return (True, word)
        elif "/" in word or not word.isalpha():
            return (False, word)

        candidates = self.known(self.edits1(word)) or self.known_edits2(word) or [word]
        suggestion = max(candidates, key=self.model.get)
        if self.verbose and word != suggestion:
            log.debug("Replacing '%s' with '%s'" % (word, suggestion) )
        return (False,  suggestion)


class TestSpellSuggestion(object):
    
    def __init__(self):
        self.s = SpellSuggestion()

    def testSpellSuggestion(self):
        assert self.s.correct("determinned") == (False, "determined")
        assert self.s.correct("teh") == (False, "the")
        assert self.s.correct("runnign") == (False, "running")

        # return the same term for correct word
        assert self.s.correct("environment") == (True, "environment")

        # return the original term if we cannot find a better suggestion
        assert self.s.correct("weichselbraun") == (False, "weichselbraun")
        assert self.s.correct("rangersdorf") == (False, "rangersdorf")

    def testExceptions(self):
        assert self.s.correct("co2") == (False, "co2")
        assert self.s.correct("i/o") == (False, "i/o")



if __name__ == '__main__':
    pass
    # s = SpellSuggestion(DEFAULT_MODEL)
    #s.train( SpellSuggestion.words( BZ2File('spell-training-corpus.text.bz2').read() ) )
    #s.serializeModel(DEFAULT_MODEL)


