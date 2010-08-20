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
        strCleanupPipe = (unicode.lower, RemovePossessive(), FixDashSpace() )
        phrCleanupPipe = (SplitEnumerations(), SplitMultiTerms(), SplitBracketExplanations() )
        wrdCleanupPipe = (FixSpelling(), RemovePunctationAndBrackets(),)
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


class CleanupPipeEntry(object):
    """ @interface CleanupPipeEntry
        an entry of the cleanup pipe """


class StringCleanupModule(CleanupPipeEntry):
    """ @interface StringCleanupModule
        abstract class for all string based cleanup modules
    """
    def __call__(self, s):
        """ cleans the following list of words
            @param[in] s the string to clean
        """
        raise NotImplemented

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


class PhraseCleanupModule(CleanupPipeEntry):
    """ @interface PhraseCleanupModule
    """
    def __call__(self, l):
        """ @param[in] l a list of phrases to cleanup """
        raise NotImplemented


class SplitEnumerations(PhraseCleanupModule):
    """ @class SplitEnumerations
        splits enumerations such as
         a) first, b) second, ...  -> ['first', 'second', ...  ]
    """
    RE_ENUM = re.compile("\(?[1-9a-h*][).] ")
    def __call__(self,l):
        result = []
        for p in l:
            result.extend( [ s.replace(",", "").strip() for s in SplitEnumerations.RE_ENUM.split(p) if s ] )

        return result

class SplitBracketExplanations(PhraseCleanupModule):
    """ @class SplitBracketExplanations
        removes additional information/explanations provided in brackets
        fire alert procedure (fap) -> ['fire alert procedure', 'fae' ]
    """
    RE_BRACKET = re.compile("(.+?)\(([^)]{2,})\)")
    def __call__(self, l):
        result = []
        for p in l:
            result.extend( [ s.strip() for s in SplitBracketExplanations.RE_BRACKET.split(p) if s ] )

        return result



class SplitMultiTerms(PhraseCleanupModule):
    """ @class SplitMultiTerms
        splits multiple meanings into single phrases """

    RE_CHOICES = re.compile("(.*?)(\w{2,}[^-])\s*/\s*(\w{2,})\s*(.*)")

    def __call__(self, l):
        result = []
        for p in l:
            for pp in p.split(", "):
                if "/" in p:
                    m = SplitMultiTerms.RE_CHOICES.search(pp)
                    if m:
                        result.append("%s%s %s" % (m.group(1), m.group(2), m.group(4)) )
                        result.append("%s%s %s" % (m.group(1), m.group(3), m.group(4)) )
                        continue

                result.append(pp)
        return result

class WordCleanupModule(CleanupPipeEntry):
    """ @cleanup WordCleanupModule
    """
    def __call__(self, l):
        """ cleans the following list of words
            @param[in] l the list of words to clean
        """
        raise NotImplemented

class FixSpelling(WordCleanupModule):
    """ @class FixSpelling 
        fixes spelling mistakes """

    def __init__(self, s=None):
        """ @param[in] s optional SpellSuggestion object to use
                         for the spell checking 
        """
        WordCleanupModule.__init__(self)

        if s==None:
            self.s = SpellSuggestion()
        else:
            self.s = s

    def __call__(self, l):
        return [ self.s.correct(w)[1] for w in l ]

    def numMistakesFixed(self, l):
        """ @returns the number of mistakes fixed by the
                     spelling module """
        return len( [ True for w in l if self.s.correct(w)[1] != w ] )


class RemovePunctationAndBrackets(WordCleanupModule):
    """ @class RemovePunctationAndBrackets
        this should be the last module to call, as it removes too much for
        many other modules to work correctly
    """
    def __call__(self, l):
        return [ s.replace(")", "").replace("(","").replace(".", "").replace("'", "").replace("!", "") for s in l ]


class TestPhraseCleanup(object):

    def __init__(self):
        self.p = PhraseCleanup.getFullCleanupProfile()

    def testAtomicPhrases(self):
        """ verifies that input phrases which contain multiple
            meanings get split"""
        assert self.p.clean(u"quick/speedy output") == [u"quick output", u"speedy output"]
        assert self.p.clean(u"i/o error") == [u"i/o error",]
        assert self.p.clean(u"planning/design") == [u"planning", u"design"]
        print self.p.clean(u'defective product/ services')
        assert self.p.clean(u'defective product/ services') == [u'defective product', u'defective services']

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

        # mistakes found in applications
        print self.p.clean(u"1. life cycle phase 2. risk management tasks 3. risk management activities")
        assert self.p.clean(u"1. life cycle phase 2. risk management tasks 3. risk management activities") == \
           [u"life cycle phase", u"risk management tasks", u"risk management activities"]

    def testSplitBracketExplanations(self):
        # mistakes found in applications
        ## cha -> ha; dow -> now due to the non risk-specific spell checking!
        assert self.p.clean(u'concept hazard analysis(cha)') == [ u'concept hazard analysis', u'ha' ] 
        print self.p.clean(u'dow fire and explosion index (f&ei)')
        assert self.p.clean(u'dow fire and explosion index (f&ei)') == [u'now fire and explosion index', u'f&ei']

    def testNumMistakesFixed(self):
        """ @test 
            returns the number of mistakes fixed in the given phrase 
        """
        s = FixSpelling()
        print s.numMistakesFixed(u'dow fire and explossion index (f&ei)'.split(" ")) 
        assert s.numMistakesFixed(u'dow fire and explossion index (f&ei)'.split(" ")) == 2

