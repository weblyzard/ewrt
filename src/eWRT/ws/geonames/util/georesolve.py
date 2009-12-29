#!/usr/bin/env python
"""
 @package eWRT.ws.geonames.util.georesolve
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
# from warnings import warn

MIN_POPULATION = 5000

class GazetteerEntryNotFound(Exception):
    """ @class GazetteerEntryNotFound
        Base class for gazetteer lookup errors 
    """
    def __init__(self, id, query):
        self.id = id
        self.query = query
        print id, query

    def __str__(self):
        return "Gazetteer lookup for entity-id '%s' failed." % (self.id)


class GazetteerNameNotFound(Exception):
    """ @class GazetteerNameNotFound
        This exception is thrown if a lookup name has not been found in the gazetteer
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Gazetteer lookup of name '%s' failed." % (self.name)


class Gazetteer(object):
    # sorting by population is a workaround for entries with multiple parents
    # (without the sorting loops occure)
    QUERY_HAS_PARENT = '''
        SELECT parent_id 
        FROM gazetteerentity ga 
        JOIN locatedin ON (ga.id = locatedin.child_id)
        JOIN gazetteerentity gb ON (gb.id = locatedin.parent_id)
        WHERE child_id = %d order by gb.population DESC LIMIT 1'''

    QUERY_CONTENT_ID = '''
        SELECT gazetteer_id FROM content_id_gazeteer_id WHERE content_id = %d '''

    QUERY_NAME = '''
            SELECT entity_id, ispreferredname, lang, gazetteerentry_id
            FROM gazetteerentry_ordered_names
            WHERE name LIKE '%s' '''

    DEBUG = False

    ## init - establishes the db-connections
    def __init__(self):
        """ implement me """
        self.db = PostgresqlDb( **DATABASE_CONNECTION['gazetteer'] )
        #PostgresqlDb.DEBUG=True
        self.db.connect()
        self.db2 = PostgresqlDb( **DATABASE_CONNECTION['geo_mapping'] )
        self.db2.connect()

    @MemoryCached
    def getGeoNameFromContentID(self, content_id):
        """ returns the location of the content ID
            @param content_id
            @return list of locaions, e.g. ['Europa', 'France', 'Centre']
        """

        query = self.QUERY_CONTENT_ID % content_id 
        result = self.db2.query(query)

        if result == []:
            return 'ContentID not found!'
        else:
            gaz_id = result[0]['gazetteer_id']
            return Gazetteer.getGeoNameFromGeoId(self, gaz_id)

    ## returns the location of the GazetteerEntry ID  
    # @param gazetteer-entry ID  
    # @return list of locations, e.g. ['Europa', 'France', 'Centre']
    @MemoryCached
    def getGeoNameFromGeoId(self, gazetteer_id):
        result = self.__getLocationTree(gazetteer_id)
        result.reverse()

        if result == []:
            return 'GazetteerID not found!'
        else:
            return result

    @MemoryCached
    def getGeoNameFromString(self, name):
        """ returns the geoname for the given string
            @param string
            @return a list of tuples (population, location) 
        """
        res = set()
        query = '''SELECT entity_id, population FROM gazetteerentry JOIN hasname ON (gazetteerentry.id = hasname.entry_id) 
                  JOIN gazetteerentity ON (gazetteerentity.id=hasname.entity_id) WHERE name = '%%s' AND (population > %d or feature_code in ('ADM1', 'ADM2', 'ADM3')) ''' % ( MIN_POPULATION)
        for result in self.db.query(query % name.replace("'", "''")):
            try:
                tmp = Gazetteer.getGeoNameFromGeoId(self, result['entity_id'])
                res.add( (result['population'], tuple(tmp)) )
            except GazetteerEntryNotFound:
                pass

        return list(res)


    ## recursive function to build the full location tree
    # @param id
    # @returns list of locations
    def __getLocationTree(self, id):
        geoPath = [ self.__getPreferredGeoName( id ) ]
        geoIdPath = [ id ]

        while id:
            parentLocationEntity = self.__hasParent(id)
            if parentLocationEntity:
                parentLocationName = self.__getPreferredGeoName( parentLocationEntity )
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
    def __getPreferredGeoName(self, id):
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
    def __hasParent(self, child_id):
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

    @MemoryCached
    def __getNameGeoId(self, name):
        """ returns the possible geoids for the given name 
            @param[in] name
            @returns a list of geoids
        """
        query = "SELECT DISTINCT entity_id FROM vw_entry_id_has_name WHERE name='%s'" % ( name.replace("'", "''") )
        return [ r['entity_id'] for r in self.db.query( query ) ]


    def getGeoIdFromGeoUrl(self, geoUrl):
        """ returns the geoId forv the given geoUrl 
            @param[in] geoUrl String or List containing the geoUrl
            @returns the geoId
        """
        if isinstance(geoUrl, str):
            geoUrl = geoUrl.split("/")

        join  = []
        where = []
        for nr, name in enumerate( geoUrl ):
            join.append("JOIN locatedin L%d ON (A%d.id = L%d.parent_id) JOIN gazetteerentity A%d ON (A%d.id = L%d.child_id)" % (nr, nr, nr, nr+1, nr+1, nr) )
            where.append( "A%d.id IN (%s)" % (nr, ", ".join( map(str, self.__getNameGeoId(self, name))) ))

        query = "SELECT A%d.id AS id FROM gazetteerentity A0 %s WHERE %s;" % ( nr, " ".join(join[:-1]), " AND ".join(where) )
        return [ int(r['id']) for r in self.db.query( query ) ]

    def getGeoDict(self, geoId):
        """ returns a dictinary with all information about the given geoId """
        print geoId
        query = "SELECT * FROM gazetteerentity WHERE id = %s" % geoId
        res = self.db.query( query )
        if len(res)>0:
            return dict(res[0])
        else:
            return {}


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


