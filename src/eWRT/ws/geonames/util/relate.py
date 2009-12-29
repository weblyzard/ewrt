#!/usr/bin/env python
"""
 @package eWRT.ws.geonames.utils.relate
 compares two location strings and determins whether/how they are related
 e.g. (eu/at/Vienna, eu/at) -> isParent
"""

# (C)opyrights 2009 by Albert Weichselbraun <albert@weblyzard.com>
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

class Related(object):
    """ @interface Related
        verifies whether two objects are related
    """

    def isRelated( self, geoRef1, geoRef2 ):
        """ verifies whether the two objects are related or not 
            @param[in] geoRef1
            @param[in] geoRef2
            @returns a float describing the strength of the relation 
        """
        raise NotImplemented

    def setRelationWeights( self, weights ):
        """ sets the weights used to compute the relation's strength 
            @param[in] weights 
        """


class MoreSpecific(Related):
    """ Bsp: (eu/at, eu/at/Carinthia/Klagenfurt) 
        => more specific 
    """
    
    def __init__(self):
    	self.setRelationWeight(( 1.0, 1.0, 0.9, 0.9, 0.85 ))

    def isRelated( self, geoRef1, geoRef2):
    	entries_of_geoRef1 = ()
	entries_of_geoRef2 = ()
	for id, value in geoRef1:
		entries_of_geoRef1 = value
		
	for id, value in geoRef2:
		entries_of_geoRef2 = value
		
	relation_strength = 0
	print len(entries_of_geoRef1)
	print len(entries_of_geoRef2)
	weight = self.weights
	
	if entries_of_geoRef1[0] == entries_of_geoRef2[0]:
		if len(entries_of_geoRef2) > len(entries_of_geoRef1):
			diff = len(entries_of_geoRef2) - len(entries_of_geoRef1)
			if len(entries_of_geoRef2) == 5:     
				if diff == 4:
					relation_strength = weight[diff] * weight[diff-1] * weight[diff-2] * weight[diff-3]
					print relation_strength
					return relation_strength
				elif diff == 3:
					relation_strength = weight[diff] * weight[diff-1] * weight[diff+1]
					print relation_strength
					return relation_strength
				elif diff == 2:
					relation_strength = weight[diff+1] * weight[diff+2]
					print relation_strength
					return relation_strength
				elif diff == 1:
					relation_strength = weight[diff+3]
					print relation_strength
					return relation_strength
           		elif len(entries_of_geoRef2) == 4:
				if diff == 3:
					relation_strength = weight[diff] * weight[diff-1] * weight[diff-2]
					print relation_strength
					return relation_strength
				elif diff == 2:
						relation_strength = weight[diff] * weight[diff+1]
						print relation_strength
						return relation_strength
				elif diff == 1:
						relation_strength = weight[diff+2]
						print relation_strength
						return relation_strength
            		elif len(entries_of_geoRef2) == 3:
				if diff == 2:
					relation_strength = weight[diff] * weight[diff-1]
					print relation_strength
					return relation_strength
				elif diff == 1:
					relation_strength = weight[diff+1]
					print relation_strength
					return relation_strength
			elif len(entries_of_geoRef2) == 2:
				if diff == 1:
					relation_strength = weight[diff]
					print relation_strength
					return relation_strength
                  
        else:
                print relation_strength
                return relation_strength

    def setRelationWeight( self, weights ):
        self.weights = weights

	


class LessSpecific(Related):
	""" Bsp: (eu/at/Styria/Graz, eu/at/Styria)
        => less specific """
	"""
f.weights = ( 0.1, 0.3, 0.8, 0.95 )
	"""
	
	def __init__(self):
        	self.setRelationWeight(( 0.1, 0.3, 0.8, 0.95 ))

    	def isRelated( self, geoRef1, geoRef2):
		entries_of_geoRef1 = ()
		entries_of_geoRef2 = ()
		for id, value in geoRef1:
			entries_of_geoRef1 = value
	
		for id, value in geoRef2:
			entries_of_geoRef2 = value
	
		relation_strength = 0
		print len(entries_of_geoRef1)
		print len(entries_of_geoRef2)
		weight = self.weights
	
		if entries_of_geoRef1[0] == entries_of_geoRef2[0]:
			if len(entries_of_geoRef2) < len(entries_of_geoRef1):
				diff = len(entries_of_geoRef1) - len(entries_of_geoRef2)
				if len(entries_of_geoRef1) == 5:
					if diff == 4:
						relation_strength = weight[diff] * weight[diff-1] * weight[diff-2] * weight[diff-3]
						print relation_strength
						return relation_strength
					elif diff == 3:
						relation_strength = weight[diff] * weight[diff-1] * weight[diff+1]
						print relation_strength
						return relation_strength
					elif diff == 2:
						relation_strength = weight[diff+1] * weight[diff+2]
						print relation_strength
						return relation_strength
					elif diff == 1:
						relation_strength = weight[diff+3]
						print relation_strength
						return relation_strength
				elif len(entries_of_geoRef1) == 4:
					if diff == 3:
						relation_strength = weight[diff] * weight[diff-2] * weight[diff+1]
						print relation_strength
						return relation_strength
					elif diff == 2:
						relation_strength = weight[diff] * weight[diff+1]
						print relation_strength
						return relation_strength
					elif diff == 1:
						relation_strength = weight[diff+2]
						print relation_strength
						return relation_strength
				elif len(entries_of_geoRef1) == 3:
					if diff == 2:
						relation_strength = weight[diff] * weight[diff-1]
						print relation_strength
						return relation_strength
					elif diff == 1:
						relation_strength = weight[diff+1]
						print relation_strength
						return relation_strength
				elif len(entries_of_geoRef1) == 2:
					if diff == 1:
						relation_strength = weight[diff]
						print relation_strength
						return relation_strength
	
		else:
			print relation_strength
			return relation_strength

    	def setRelationWeight( self, weights ):
        	self.weights = weights



class MoreOrLessSpecific(Related):
    """ combines less and more specific """

    def __init__(self):
    	self.setRelationWeight(( 1.0, 1.0, 0.9, 0.9, 0.85 ))
    	self.setRelationWeightl(( 0.1, 0.3, 0.8, 0.95, 1.5 ))


    def isRelated( self, geoRef1, geoRef2):
    	entries_of_geoRef1 = ()
	entries_of_geoRef2 = ()
	for id, value in geoRef1:
		entries_of_geoRef1 = value
		
	for id, value in geoRef2:
		entries_of_geoRef2 = value
		
	relation_strength = 0
	print len(entries_of_geoRef1)
	print len(entries_of_geoRef2)
	weight = self.weights
	weightl = self.weightsl
	
	if entries_of_geoRef1[0] == entries_of_geoRef2[0]:
		if len(entries_of_geoRef2) > len(entries_of_geoRef1):
			diff = len(entries_of_geoRef2) - len(entries_of_geoRef1)
			if len(entries_of_geoRef2) == 5:     
				if diff == 4:
					relation_strength = weight[diff] * weight[diff-1] * weight[diff-2] * weight[diff-3]
					print relation_strength
					return relation_strength
				elif diff == 3:
					relation_strength = weight[diff] * weight[diff-1] * weight[diff+1]
					print relation_strength
					return relation_strength
				elif diff == 2:
					relation_strength = weight[diff+1] * weight[diff+2]
					print relation_strength
					return relation_strength
				elif diff == 1:
					relation_strength = weight[diff+3]
					print relation_strength
					return relation_strength
           		elif len(entries_of_geoRef2) == 4:
				if diff == 3:
					relation_strength = weight[diff] * weight[diff-1] * weight[diff-2]
					print relation_strength
					return relation_strength
				elif diff == 2:
						relation_strength = weight[diff] * weight[diff+1]
						print relation_strength
						return relation_strength
				elif diff == 1:
						relation_strength = weight[diff+2]
						print relation_strength
						return relation_strength
            		elif len(entries_of_geoRef2) == 3:
				if diff == 2:
					relation_strength = weight[diff] * weight[diff-1]
					print relation_strength
					return relation_strength
				elif diff == 1:
					relation_strength = weight[diff+1]
					print relation_strength
					return relation_strength
			elif len(entries_of_geoRef2) == 2:
				if diff == 1:
					relation_strength = weight[diff]
					print relation_strength
					return relation_strength
                elif len(entries_of_geoRef2) < len(entries_of_geoRef1):
			diff = len(entries_of_geoRef1) - len(entries_of_geoRef2)
			if len(entries_of_geoRef1) == 5:
				if diff == 4:
					relation_strength = weightl[diff] * weightl[diff-1] * weightl[diff-2] * weightl[diff-3]
					print relation_strength
					return relation_strength
				elif diff == 3:
					relation_strength = weightl[diff] * weightl[diff-1] * weightl[diff+1]
					print relation_strength
					return relation_strength
				elif diff == 2:
					relation_strength = weightl[diff+1] * weightl[diff+2]
					print relation_strength
					return relation_strength
				elif diff == 1:
					relation_strength = weightl[diff+3]
					print relation_strength
					return relation_strength
			elif len(entries_of_geoRef1) == 4:
				if diff == 3:
					relation_strength = weightl[diff] * weightl[diff-2] * weightl[diff+1]
					print relation_strength
					return relation_strength
				elif diff == 2:
					relation_strength = weightl[diff] * weightl[diff+1]
					print relation_strength
					return relation_strength
				elif diff == 1:
					relation_strength = weightl[diff+2]
					print relation_strength
					return relation_strength
			elif len(entries_of_geoRef1) == 3:
				if diff == 2:
					relation_strength = weightl[diff] * weightl[diff-1]
					print relation_strength
					return relation_strength
				elif diff == 1:
					relation_strength = weightl[diff+1]
					print relation_strength
					return relation_strength
			elif len(entries_of_geoRef1) == 2:
				if diff == 1:
					relation_strength = weightl[diff]
					print relation_strength
					return relation_strength
	
		else:
			print relation_strength
			return relation_strength 
        else:
                print relation_strength
                return relation_strength

    def setRelationWeight( self, weights ):
        self.weights = weights

    def setRelationWeightl( self, weightsl ):
        self.weightsl = weightsl





class TestRelated(object):

    def testRelated(object):
        r = Related()
        assert r.isRelated( "eu/at/Vienna/Vienna", "eu/at/Styria" ) == 0.7 

if __name__ == "__main__":
	
	#ms = MoreSpecific()
	#a = [(90610L, ('Europe', 'Austria', 'Carinthia', 'Klagenfurt'))]
	#b = [(8184691L, ('Europe', 'Austria'))]
	#ms.isRelated(b,a)
	
	#ms = LessSpecific()
	#a = [(90610L, ('Europe', 'Austria', 'Carinthia', 'Klagenfurt'))]
	#b = [(8184691L, ('Europe', 'Austria'))]
	#ms.isRelated(a,b)
	
	ms = MoreOrLessSpecific()
	a = [(90610L, ('Europe', 'Austria', 'Carinthia', 'Klagenfurt'))]
	b = [(8184691L, ('Europe', 'Austria'))]
	ms.isRelated(a,b)
	
