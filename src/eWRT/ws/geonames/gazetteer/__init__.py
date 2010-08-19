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

from eWRT.access.db import PostgresqlDb
from eWRT.util.cache import MemoryCached
from eWRT.config import DATABASE_CONNECTION, GEO_ENTITY_SEPARATOR
from eWRT.ws.geonames.gazetteer.exception import GazetteerEntryNotFound

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

    def getGeoEntityDict(self, name=None, id=None, geoUrl=None):
        """ returns a list of GeoEntities matching the given information
            @param[in] name   of the Entity
            @param[in] id     the GeoNames id 
            @param[in] geoUrl the entity's dictionary
        """
        geoId = []
        if name:
            geoId.extend( self.getIdFromName(self, name) )
        if id:
            geoId.append( id )
        if geoUrl:
            geoId.extend( self.getIdFromGeoUrl( geoUrl ) )
        return self.getGeoEntityDictFromId( geoId )

    @MemoryCached
    def getIdFromName(self, name):
        """ returns the possible GeoNames ids for the given name 
            @param[in] name
            @returns a list of GeoNames ids
        """
        query = "SELECT id FROM vw_gazetteer WHERE name='%s' ORDER BY population DESC" % ( name.replace("'", "''") )
        res = [ r['id'] for r in self.db.query( query ) ]
        #query = "SELECT DISTINCT entity_id FROM vw_entry_id_has_name WHERE name='%s'" % ( name.replace("'", "''") )
        return [ r['id'] for r in self.db.query( query ) ]

    def getIdFromGeoUrl(self, geoUrl):
        """ returns the geoId for the given geoUrl 
            @param[in] geoUrl 
            @returns a list of geonames ids matching the geoUrl
        """
        geoUrl = geoUrl.split(GEO_ENTITY_SEPARATOR)

        join  = []
        where = []
        for nr, name in enumerate( geoUrl ):
            join.append("JOIN locatedin L%d ON (A%d.id = L%d.parent_id) JOIN gazetteerentity A%d ON (A%d.id = L%d.child_id)" % (nr, nr, nr, nr+1, nr+1, nr) )
            where.append( "A%d.id IN (%s)" % (nr, ", ".join( map(str, self.getIdFromName(self, name))) ))

        query = "SELECT A%d.id AS id FROM gazetteerentity A0 %s WHERE %s;" % ( nr, " ".join(join[:-1]), " AND ".join(where) )
        return [ int(r['id']) for r in self.db.query( query ) ]

    # @MemoryCached
    def getGeoEntityDictFromId(self, id):
        """ returns the location of the GazetteerEntry ID  
            @param id a list of geonames ids
            @return list of GeoEntities
        """
        if id:
            q = "SELECT * FROM gazetteerentity LEFT JOIN countryInfo USING(id) WHERE id IN (%s)" % ", ".join( map(str, id ))
            res = self.db.query( q ) 
            if len(res)>0:
                entities = [ dict(self._getResultById(res, i).items()) for i in id ]
                self._addGeoUrl( entities )
                return entities

            print "WARNING: no entities found for ", ", ".join( map(str,id) )

        return []

    def _getResultById(self, l, id, idAttr="id"):
        """ returns the database column matching the given id 
            @param[in] l      the list of query results
            @param[in] id     the row id to return
            @param[in] idAttr attribute to consider for the id
        """
        return [ e for e in l if e[idAttr] == id ][0]


    def _addGeoUrl( self, entities ):
        """ adds the geoUrl and level key to the given list of entities """
        for entity in entities:
            idUrl, nameUrl = self._getGeoUrl( entity['id'] )
            entity['geoUrl'] = GEO_ENTITY_SEPARATOR.join(nameUrl)
            entity['idUrl']  = idUrl
            entity['level']  = len(nameUrl)                         # hierarchy level of the entity (e.g. eu>at => 2)

    def _getGeoUrl(self, id):
        """ returns the geoUrl for the given entity 
            @param[in] the geonames gazetteer id 
            @returns   two lists containing (geoIdPath, geoNamePath) 
        """
        geoNamePath = [ self._getPreferredGeoName( id ) ]
        geoIdPath = [ id ]

        while id:
            parentLocationEntity = self._hasParent(id)
            if parentLocationEntity:
                parentLocationName = self._getPreferredGeoName( parentLocationEntity )
                if parentLocationEntity in geoIdPath:
                    print "%s in %s" % (parentLocationName, geoNamePath)
                    break
                geoNamePath.append( parentLocationName )

            geoIdPath.append( parentLocationEntity )
            id = parentLocationEntity

        geoIdPath.reverse()
        geoNamePath.reverse()
        return (geoIdPath[1:], geoNamePath)


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
                        (lang='en') DESC, (lang IS NULL) DESC, (lang = '') DESC,
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

