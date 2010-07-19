#!/usr/bin/env python
"""
 @package eWRT.ontology.compare.relationtypes
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

from nltk import WordNetLemmatizer, pos_tag
from eWRT.util.cache import MemoryCache, MemoryCached
from collections import defaultdict


class RelationTypes(object):

    SHORT_POS = { 
        'IN': 'p', 'TO': 'p', 'RB': 'p', 'RP': 'p',
        'VB': 'v', 'MD': 'v', 
        'NN': 'v'                   # map nouns to verbs as they are the default results
    }

    AUXILIARY_VERBS = ('be', 'have', 'may', 'should', 'can', 'do', 'might', 'must' 'ought', 'shall', 'would')
    
    def __init__(self):
        self.w = WordNetLemmatizer()
        self.cache = MemoryCache()
        # self.cache.fetchObjectId(text,  self.w.lemmatize, text.split(), pos='v' ):

    @staticmethod
    @MemoryCached
    def getPos(text):
        """ returns the pos tags for the given text """
        posMap = []
        for term, pos in pos_tag( text.split() ):
            mapping = [ spos for lpos, spos in RelationTypes.SHORT_POS.items() if pos.startswith(lpos) ]
            pos = mapping[0] if mapping else ''
            posMap.append( pos )

        return posMap


    def partitionRelation(self, text, removeAuxiliaryVerbs=True) :
        """ partitions a relation into the following comparision format:
              {'v': ( v1, ...), 'p': ('by', ...), '': ('also', ...) }
            @param[in] text the text describing the link
            @returns   the partitioned text 
        """
        result = defaultdict( list )
        for term, pos in zip( text.split(), self.getPos(text)):
            result[pos].append(  
                 self.cache.fetchObjectId(term, self.w.lemmatize, term, pos='v' ) if pos=='v' else term )

        if 'v' in result and removeAuxiliaryVerbs:
            result['v'] = self.removeAuxiliaryVerbs( result['v'] )
 
        return result

    @staticmethod
    def removeAuxiliaryVerbs( verbList ):
        """ removes auxiliary verbs from the given list, provided that
            at least one verb remains in the list.

            @param[in] verbList a list of verbs to analyze
            @returns   the cleaned verblist 
        """
        return [ v for v in verbList if v not in RelationTypes.AUXILIARY_VERBS ] or [ verbList[0] ]


class TestRelationTypes(object):

    def __init__(self):
        self.rt = RelationTypes()

    def testPosTagging(self):
        """ tests the pos tagging """
        print self.rt.getPos("can be saved by")
        assert self.rt.getPos("can be saved by") == ['v', 'v', 'v', 'p']

        print self.rt.getPos("involves")
        assert self.rt.getPos("involves") == ['v', ]

    def testPartitioning(self):
        """ tests the verb partitioning """
        print self.rt.partitionRelation("can be saved by") 
        assert dict(self.rt.partitionRelation("can be saved by")) == {'v': ['save', ], 'p': ['by',],  } 
        assert dict(self.rt.partitionRelation("results in"))      == {'v': ['result', ], 'p': ['in',],  }
        assert dict(self.rt.partitionRelation("e.g."))            == {'v': ["e.g."] }
        assert dict(self.rt.partitionRelation("????"))            == {'v': ["????"] }


    def testRemoveAuxiliaryVerbs(self):
        """ tests the removal of auxiliary verbs """
        assert self.rt.removeAuxiliaryVerbs( ("can", "be", "save", ) ) == ["save", ]

        print self.rt.removeAuxiliaryVerbs( ("be",))
        assert self.rt.removeAuxiliaryVerbs( ("be",)) == ["be",]
        assert self.rt.removeAuxiliaryVerbs( ("can", "range", "high")) == ["range", "high"]
        
