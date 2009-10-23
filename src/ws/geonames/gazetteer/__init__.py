#!/usr/bin/env python
"""
 @package eWRT.ws.geonames.gazetteer
 fetches for an ContentID or GazEntry-ID where it is located
 e.g. for Vienna: Europe/Austria/Vienna
"""

# (C)opyrights 2009 by Heinz Lang <heinz.lang@wu.ac.at>
#                      Albert Weichselbraun <albert@weichselbraun.net>
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
from eWRT.util.cache import MemoryCached
from eWRT.config import DATABASE_CONNECTION
from eWRT.ws.geonames import GeoEntity
from eWRT.ws.geonames.exception import *

MIN_POPULATION = 5000


class Gazetteer(object):
    # sorting by population is a workaround for entries with multiple parents
    # (without the sorting loops occure)
    QUERY_HAS_PARENT = '''
        SELECT parent_id 
        FROM gazetteerentity ga 
        JOIN locatedin ON (ga.id = locatedin.child_id)
        JOIN gazetteerentity gb ON (gb.id = locatedin.parent_id)
        WHERE child_id = %d order by gb.population DESC LIMIT 1'''

    DEBUG = False

    def __init__(self):
        """ initializes the gazetteer object and the database connections  """
        self.db = PostgresqlDb( **DATABASE_CONNECTION['gazetteer'] )
        self.db.connect()
        self.db2 = PostgresqlDb( **DATABASE_CONNECTION['geo_mapping'] )
        self.db2.connect()

    @MemoryCached
    def getGeoEntities(self, name=None, id=None, geoUrl=None):
        """ returns a list of GeoEntities matching the given information
            @param[in] name   of the Entity
            @param[in] id     the GeoNames id 
            @param[in] geoUrl the entity url
        """
        geoId = []
        if name:
            geoId.extend( getIdFromName(name) )
        if id:
            geoId.extend( id )
        if geoUrl:
            geoId.extend( getIdFromGeoUrl( geoUrl ) )

        return getGeoEntityFromId( geoId )

    @MemoryCached
    def getIdFromName(self, name):
        """ returns the possible GeoNames ids for the given name 
            @param[in] name
            @returns a list of GeoNames ids
        """
        query = "SELECT DISTINCT entity_id FROM vw_entry_id_has_name WHERE name='%s'" % ( name.replace("'", "''") )
        return [ r['entity_id'] for r in self.db.query( query ) ]

    def getIdFromGeoUrl(self, geoUrl):
        """ returns the geoId forv the given geoUrl 
            @param[in] geoUrl 
            @returns a list of geonames ids matching the geoUrl
        """
        geoUrl = geoUrl.split("/")

        join  = []
        where = []
        for nr, name in enumerate( geoUrl ):
            join.append("JOIN locatedin L%d ON (A%d.id = L%d.parent_id) JOIN gazetteerentity A%d ON (A%d.id = L%d.child_id)" % (nr, nr, nr, nr+1, nr+1, nr) )
            where.append( "A%d.id IN (%s)" % (nr, ", ".join( map(str, self.getIdFromName(self, name))) ))

        query = "SELECT A%d.id AS id FROM gazetteerentity A0 %s WHERE %s;" % ( nr, " ".join(join[:-1]), " AND ".join(where) )
        return [ int(r['id']) for r in self.db.query( query ) ]

    @MemoryCached
    def getGeoEntityFromId(self, id):
        """ returns the location of the GazetteerEntry ID  
            @param id a list of geonames ids
            @return list of GeoEntities
        """
        q = "SELECT * FROM entity WHERE gazetteer_id IN (%s)" % ", ".join(gazetteer_id)
        entities = [ GeoEntity( result ) for result in self.db.query( q ) ]
        self._addGeoUrl( entities )
        return entities

    def _addGeoUrl( entities ):
        """ adds the geoUrl key to the given list of entities """
        for entity in entities:
            entry.entityDict['geoUrl'] = self._getGeoUrl( entity['id'] )


    def _getGeoUrl(self, id):
        """ returns the geoUrl for the given entity 
            @param[in] the geonames gazetteer id 
            @returns   the geoUrl (e.g. /Europe/Austria/Vienna)
        """
        geoPath = [ self.__getPreferredGeoName( id ) ]
        geoIdPath = [ id ]

        while id:
            parentLocationEntity = self._hasParent(id)
            if parentLocationEntity:
                parentLocationName = self._getPreferredGeoName( parentLocationEntity )
                if parentLocationEntity in geoIdPath:
                    print "%s in %s" % (parentLocationName, geoPath)
                    break
                geoPath.append( parentLocationName )

            geoIdPath.append( parentLocationEntity )
            id = parentLocationEntity

        return geoPath


    ## gets the preferred name for the location
    # @param id
    # @returns preferred name
    def _getPreferredGeoName(self, id):
        """ returns the preferred entry name for the given
            entity id
            @param[in] entity_id 
            @returns the geo entity's name
        """ 

        query = '''SELECT name FROM vw_gazetteer_tng WHERE id=%d 
                      ORDER BY 
                            (lang='en' and lang is not null) DESC,
                            (short=TRUE and short IS NOT NULL) DESC,
                            preferred DESC
                      LIMIT 1''' % (id)
        result = self.db.query(query)
        if not result:
            raise GazetteerEntryNotFound(id, query)

        return Gazetteer.DEBUG and result[0]['name']+"(%d)" % (id) or result[0]['name']


    ## checks if the given ID has a parent
    # @param ID of the child
    # @return false or ID of the parent 
    def _hasParent(self, child_id):
        query = self.QUERY_HAS_PARENT % child_id
        result = self.db.query(query)
        
        # todo: is it necessary, that this functions can process multiple parents?
        # multiple parents (!)
        if result.__len__() > 1:
            print '### result > 1 ###'
            print '    child_id:  %s' % child_id
            print '    parent_id: %s ' % [ e['parent_id'] for e in result ]


        # todo: does it make sense to fetch infinite loops
        if result == []:
            return 0 
        else:
            return result[0]['parent_id']


class TestGazeteer(object):
    
    def __init__(self):
        self.gazetteer = Gazetteer()
    
    def testUniqueStringResolver(self):
        getName = Gazetteer.getGeoNameFromString
        for name, entries in ( ('Lainach', 0), ('Vienna', 4), ('Madrid', 5), ('Graz', 1), ('Poland', 2), ('Geneva', 5) ):
            assert len( getName( self.gazetteer, name )) == entries 

    def testContentIdResolver(self):
        assert Gazetteer.getGeoNameFromContentID(self.gazetteer, 86597672) == ['Europe', 'France', 'Centre']

    def testGetGeoIdFromGeoUrl(self):
        """ tests the resolution from geurls to geoid's """
        for geoId in ( 2761367,  # Vienna
                       4277145,  # Perth
                       2063523, 
                       2599670,  # Bosten
                       6470560,  # New York
                       2772400): # Linz

            geoUrl    = self.gazetteer.getGeoNameFromGeoId( self.gazetteer, geoId )
            geoIdList = self.gazetteer.getGeoIdFromGeoUrl( geoUrl )
            assert len(geoIdList) == 1
            assert geoId == geoIdList[0]
    
if __name__ == "__main__":
    a = Gazetteer()
    if sys.argv.__len__() > 1:
        # print a.getGeoIdFromGeoUrl( "Europe/Austria/Vienna/Vienna" )
        print Gazetteer.getGeoNameFromString(a, sys.argv[1])
    else:
        # print Gazetteer.getGeoNameFromContentID(a, 86597672)
        # print Gazetteer.getGeoNameFromContentID(a, 90160635)
        print Gazetteer.getGeoNameFromString(a, 'Vienna')
        print Gazetteer.getGeoNameFromString(a, "Lainach" )
        print Gazetteer.getGeoNameFromString(a, "Spittal an der Drau" )
        print Gazetteer.getGeoNameFromString(a, "Salzburg" )
        print Gazetteer.getGeoNameFromString(a, "London" )


