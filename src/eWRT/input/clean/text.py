#!/usr/bin/env python
"""
 @package eWRT.input.clean.text
 cleans up text phrases
"""

# (C)opyrights 2010 by Albert Weichselbraun <albert@weichselbraun.net>
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

from eWRT.stat.string.spelling import SpellSuggestion
import re

class PhraseCleanup(object):
    """
    @class PhraseCleanup
    takes an input phrase and returns a list of "elementary" phrases.
    (e.g. quick/speedy output -> ["quick output", "speedy output"])
    """
    def __init__(self, strCleanupModules, phraseCleanupModules, wordCleanupModules):
        """ @param[in] the list of cleanupModules to apply to the input """
        self.strCleanupModules    = strCleanupModules
        self.phraseCleanupModules = phraseCleanupModules
        self.wordCleanupModules    = wordCleanupModules

    @staticmethod
    def getFullCleanupProfile():
        """ returns the full cleanup profile using all cleanup modules """
        strCleanupPipe = (unicode.lower, RemoveEnumerations(), RemovePossessive(), FixDashSpace(), RemovePunctationAndBrakets(), )
        phrCleanupPipe = (SplitMultiTerms(), )
        wrdCleanupPipe = (FixSpeeling(), )
        return PhraseCleanup(strCleanupPipe, phrCleanupPipe, wrdCleanupPipe )

    def clean(self, phrase):
        """ @param[in] the input phrase to clean 
            @returns a list of elementary cleaned phrases """

        for m in self.strCleanupModules:
            phrase = m(phrase)

        phrase = [phrase]
        for m in self.phraseCleanupModules:
            phrase = m(phrase)

        result = []
        for atomicPhrase in phrase:
            outWords = atomicPhrase.split()
            for m in self.wordCleanupModules:
                outWords = m(outWords)

            result.append(" ".join(outWords) )

        return result




class StringCleanupModule(object):
    """ @class CleanupPipeEntry
        abstract class for all string based cleanup modules
    """
    def __call__(self, s):
        """ cleans the following list of words
            @param[in] s the string to clean
        """
        raise NotImplemented

class RemovePunctationAndBrakets(StringCleanupModule):
    def __call__(self, s):
        return s.replace(")", "").replace("(","").replace(".", "") 

class RemovePossessive(StringCleanupModule):
    """ @class RemovePossessive
        removes the possessive as indicated by 's """
    def __call__(self, s):
        return s.replace("'s", "")

class FixDashSpace(StringCleanupModule):
    """ @class FixDashSpace
        fixes spaces before/after dashes
        e.g. "semi- automatically" -> "semi-automatically"
             "semi -quantitative" -> "semi-quantitative"
    """
    RE_DASH = re.compile("(\w)(?:\s-\s?|-\s)(\w)")
    def __call__(self, s):
        return FixDashSpace.RE_DASH.sub(r"\1-\2", s)

class RemoveEnumerations(StringCleanupModule):
    """ @class RemoveEnumerations
        removes enumerations such as
         a) first, b) second, ... 
    """
    RE_ENUM = re.compile("\(?[1-9a-h*][).] ")
    def __call__(self,s):
        return RemoveEnumerations.RE_ENUM.sub("",s)


class PhraseCleanupModule(object):
    """ @cleanup PhraseCleanup
    """
    def __class__(self, ph):
        """ @param[in] ph a list of phrases to cleanup """
        raise NotImplemented

class SplitMultiTerms(PhraseCleanupModule):
    """ @class SplitMultiTerms
        splits multiple meanings into single phrases """

    RE_CHOICES = re.compile("(\w{2,})\s*/\s*(\w{2,})\s*(.*)")

    def __call__(self, l):
        result = []
        for p in l:
            for pp in p.split(", "):
                if "/" in p:
                    m = SplitMultiTerms.RE_CHOICES.search(pp)
                    if m:
                        result.append("%s %s" % (m.group(1), m.group(3)) )
                        result.append("%s %s" % (m.group(2), m.group(3)) )
                        continue

                result.append(pp)
        return result

class WordCleanupModule(object):
    """ @cleanup WordCleanupModule
    """
    def __call__(self, l):
        """ cleans the following list of words
            @param[in] l the list of words to clean
        """
        raise NotImplemented

class FixSpeeling(WordCleanupModule):
    """ @class FixSpeeling 
        fixes spelling mistakes """
    def __init__(self):
        self.s = SpellSuggestion()

    def __call__(self, l):
        return [ self.s.correct(w)[1] for w in l ]



class TestPhraseCleanup(object):

    def __init__(self):
        self.p = PhraseCleanup.getFullCleanupProfile()

    def testAtomicPhrases(self):
        """ verifies that input phrases which contain multiple
            meanings get split"""
        assert self.p.clean(u"quick/speedy output") == [u"quick output", u"speedy output"]
        assert self.p.clean(u"i/o error") == [u"i/o error",]
        assert self.p.clean(u"planning/design") == [u"planning", u"design"]

    def testFixSpellingErrors(self):
        print self.p.clean(u"determine mening")
        assert self.p.clean(u"deterrmin mening") == [u"determine meaning", ]

    def testFixDashSpace(self):
        assert self.p.clean(u"semi -automatically and semi- quick") == [u"semi-automatically and semi-quick"]
        assert self.p.clean(u"run-/config") == [u"run-/config"]

    def testRemoveEnumerations(self):
        print self.p.clean(u"1. fix it, 2. do it")
        assert self.p.clean(u"1. fix it, 2. do it") == [u"fix it", u"do it"]
        assert self.p.clean(u"1) fix it, 2) do it") == [u"fix it", u"do it"]
        assert self.p.clean(u"(1) fix it, (2) do it") == [u"fix it", u"do it"]
        assert self.p.clean(u"(*) fix it, (*) do it") == [u"fix it", u"do it"]
        assert self.p.clean(u"a) fix it, b) do it") == [u"fix it", u"do it"]

