#!/usr/bin/env python
"""
 @package eWRT.ws.geonames
"""

# (C)opyrights 2009 by Albert Weichselbraun <albert@weichselbraun.net>
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
from eWRT.access.db import PostgresqlDb
from eWRT.util.cache import MemoryCached, DiskCached
from eWRT.access.http import Retrieve
from eWRT.ws.geonames.gazetteer import Gazetteer
from eWRT.config import GEO_ENTITY_SEPARATOR

class GeoEntity(object):
    """ a geographic entity """

    def __init__(self, entityDict):
        assert isinstance(entityDict, dict)
        self.entityDict = entityDict
        self.id         = entityDict['id']

    @staticmethod
    @MemoryCached
    def factory(name=None, id=None, geoUrl=None):
        """ creates geoentity objects based on the given information
            @param[in] name   of the Entity
            @param[in] id     the GeoNames id 
            @param[in] geoUrl the entity url
        """
        g = Gazetteer()
        return [ GeoEntity( d ) for d in g.getGeoEntityDict(name, id, geoUrl) ]


    def __getitem__(self, key):
        return self.entityDict.get( key )


    def __sub__(self, geoEntity):
        """ returns the distance between the two locations 
            @param[in] the entity to compare
            @returns the distance in m
        """
        pass

    def __str__(self):
        return "GeoEntity <%s (id=%s)>" % (self.entityDict['geoUrl'], self.entityDict['id'] )

    def contains(self, geoEntity):
        """ Returns true if the Object contains the given GeoEntity.
            e.g. eu>at>Carinthia contains 
                 eu>at>Carinthia, eu>at>Carinthia>Spittal/Drau and any
                 other more detailed specification.
            
            @param[in] geoEntity
            @returns true or false """

        if self['geoUrl'] in geoEntity['geoUrl']:
            return True
        else:
            return False

    def highestCommonLevel(self, geoEntity):
        """ Returns the highest common level between the two GeoEntities
            e.g. eu>at>Carinthia, eu>at>Carinthia>Spittal/Drau => 3
            @param[in] geoEntity
            @returns the level
        """
        selfLevels = self['geoUrl'].split( GEO_ENTITY_SEPARATOR )
        cmpLevels  = geoEntity['geoUrl'].split( GEO_ENTITY_SEPARATOR ) 
        for level, (l1, l2) in enumerate( zip( selfLevels, cmpLevels) ):
            if l1 != l2:
                break
            level += 1

        return level

    def getState(self):
        """ Returns the state in which the given geoEntity
            is located """

        assert self['level']>=3
        print self['level'], self['idUrl'], self['idUrl'][2]
        return GeoEntity.factory( id = self['idUrl'][2] )[0]

    def getCountry(self):
        """ Returns the country in which the given geoEntity
            is located """

        assert self['level']>=2
        return GeoEntity.factory( id = self['idUrl'][1] )[0]

    def __eq__(self, o):
        """ add's support for comparisons using == """
        return self['id'] == o['id']

    def __neq__(self, o):
        """ adds support for the != operator """
        return self['id'] != o['id']

    def __cmp__(self, o):
        return self['id'].__cmp__(o['id'])

    def __hash__(self):
        return self['id'].__hash__()


class GeoNames(object):
    """ retrieves information for GeoNames ids
        please use the helper classes in utils.georesolve
        to translate geoURLs into geoIDs 
    """

    NEIGHBOURS_SERVICE_URL = "http://ws.geonames.org/neighboursJSON?geonameId=%d" 

    @staticmethod
    @DiskCached("./.geonames-neighbours")
    def getNeighbors(geo_entity):
        """ returns all neighbours for the given geo id
            (currently only implemented on a country level)
            @param[in] geo_entity
            @returns a list containing the neighbours of the given country """

        url = GeoNames.NEIGHBOURS_SERVICE_URL % geo_entity.id
        jsonData = eval( Retrieve('eWRT.ws.geonames').open(url).read() )
        return [ GeoEntity.factory( id = e['geonameId'] )[0] for e in jsonData['geonames'] ]


class TestGeoNames(object):

    EXAMPLE_ENTITIES = { '.ch'       : GeoEntity.factory( id = 2658434 )[0],
                         '.at'       : GeoEntity.factory( id = 2782113 )[0],
                         '.carinthia': GeoEntity.factory( id = 2774686 )[0],
                         '.eu': GeoEntity.factory( id = 6255148 )[0],
                         'villach'   : GeoEntity.factory( id = 2762372 )[0],
                         'hermagor'  : GeoEntity.factory( id = 2776497 )[0],
                       }

    def testGetNeighbors(self):
        geoEntity = self.EXAMPLE_ENTITIES['.ch'] # .ch
        assert set([ g.id for g in GeoNames.getNeighbors(geoEntity) ]) == set([2782113, 3017382, 2921044, 3175395, 3042058])

    def testContains(self):
        geoEntity = self.EXAMPLE_ENTITIES['.at'] # .at
        assert geoEntity.contains( self.EXAMPLE_ENTITIES['.at'] ) == True
        assert geoEntity.contains( self.EXAMPLE_ENTITIES['.carinthia'] ) == True
        assert geoEntity.contains( self.EXAMPLE_ENTITIES['.eu'] ) == False
        assert geoEntity.contains( self.EXAMPLE_ENTITIES['.ch'] ) == False
       
    def testIsContained(self):
        geoEntity = self.EXAMPLE_ENTITIES['.at'] # .at
        assert self.EXAMPLE_ENTITIES['.at'].contains( geoEntity ) == True
        assert self.EXAMPLE_ENTITIES['.carinthia'].contains( geoEntity ) == False
        assert self.EXAMPLE_ENTITIES['.eu'].contains( geoEntity ) == True
        assert self.EXAMPLE_ENTITIES['.ch'].contains( geoEntity ) == False

    def testHighestCommonLevels(self):
        g = self.EXAMPLE_ENTITIES['.carinthia']
        assert g.highestCommonLevel( self.EXAMPLE_ENTITIES['.at'] ) == 2
        assert g.highestCommonLevel( self.EXAMPLE_ENTITIES['.eu'] ) == 1
        print g.highestCommonLevel( self.EXAMPLE_ENTITIES['.ch'])
        assert g.highestCommonLevel( self.EXAMPLE_ENTITIES['.ch'] ) == 1
        assert g.highestCommonLevel( self.EXAMPLE_ENTITIES['.carinthia'] ) == 3

    def testGetState(self):
        assert self.EXAMPLE_ENTITIES['villach'].getState() == self.EXAMPLE_ENTITIES['.carinthia']
        assert self.EXAMPLE_ENTITIES['hermagor'].getState() == self.EXAMPLE_ENTITIES['.carinthia']
        assert self.EXAMPLE_ENTITIES['.carinthia'].getState() == self.EXAMPLE_ENTITIES['.carinthia']

    def testGetCountry(self):
        assert self.EXAMPLE_ENTITIES['villach'].getCountry() == self.EXAMPLE_ENTITIES['.at']
        assert self.EXAMPLE_ENTITIES['hermagor'].getCountry() == self.EXAMPLE_ENTITIES['.at']
        assert self.EXAMPLE_ENTITIES['.carinthia'].getCountry() == self.EXAMPLE_ENTITIES['.at']
        assert self.EXAMPLE_ENTITIES['.at'].getCountry() == self.EXAMPLE_ENTITIES['.at']
        assert not self.EXAMPLE_ENTITIES['.at'].getCountry() == self.EXAMPLE_ENTITIES['.ch']

    def testSetProperties(self):
        """ verifies that functions such as __hash__, __cmp__ required for handling
            sets work """
        a = set( self.EXAMPLE_ENTITIES.values() )
        b = set( (self.EXAMPLE_ENTITIES['villach'], self.EXAMPLE_ENTITIES['hermagor']) )
        assert a.intersection(b) == b
        assert len(a.difference(b)) < len(a)


if __name__ == '__main__':
    g = GeoEntity.factory(geoUrl = 'Europe>Austria>Vienna')
    print g, g[0]
    print g[0].entityDict
