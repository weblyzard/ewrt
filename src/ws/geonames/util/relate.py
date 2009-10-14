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

    def setRelationWeight( self, weights ):
        self.weights = ( 1.0, 1.0, 0.9, 0.9, 0.85 )



class LessSpecific(Related):
    """ Bsp: (eu/at/Styria/Graz, eu/at/Styria)
        => less specific """

    def setRelationWeight( weights ):
        self.weights = ( 0.1, 0.3, 0.8, 0.95 )


class MoreOrLessSpecific(Related):
    """ combines less and more specific """




class TestRelated(object):

    def testRelated(object):
        r = Related()
        assert r.isRelated( "eu/at/Vienna/Vienna", "eu/at/Styria" ) == 0.7 

