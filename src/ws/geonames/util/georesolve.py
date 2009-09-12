#!/usr/bin/env python
"""
 @package eWRT.ws.geonames.utils.georesolve
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
<<<<<<< .mine
from eWRT.util.cache import MemoryCached
from eWRT.config import DATABASE_CONNECTION
from warnings import warn
=======
from eWRT.config import GAZETTEER_DB, GAZETTEER_HOST, GAZETTEER_USER, GAZETTEER_PASS, CONTENT_DB, CONTENT_HOST, CONTENT_USER, CONTENT_PASS
>>>>>>> .r596

class GazetteerEntryNotFound(Exception):
    """ @class GazetteerEntryNotFound
        Base class for gazetteer lookup errors 
    """
    def __init__(self, id):
        self.id = id

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
    QUERY_HAS_PARENT = '''
        SELECT parent_id 
        FROM gazetteerentity JOIN locatedin ON (gazetteerentity.id = locatedin.child_id)
        WHERE child_id = %d'''

    QUERY_CONTENT_ID = '''
        SELECT gazetteer_id FROM content_id_gazeteer_id WHERE content_id = %d '''

    QUERY_NAME = '''
            SELECT entity_id, ispreferredname, lang, gazetteerentry_id
            FROM gazetteerentry_ordered_names
            WHERE name LIKE '%s' '''

    parents = []

    ## init - establishes the db-connections
    def __init__(self):
<<<<<<< .mine
        """ implement me """
        self.db = PostgresqlDb( **DATABASE_CONNECTION['gazetteer'] )
        #PostgresqlDb.DEBUG=True
=======
        self.db = PostgresqlDb(GAZETTEER_DB, GAZETTEER_HOST, GAZETTEER_USER, GAZETTEER_PASS)
>>>>>>> .r596
        self.db.connect()
<<<<<<< .mine
        self.db2 = PostgresqlDb( **DATABASE_CONNECTION['geo_mapping'] )
=======
        self.db2 = PostgresqlDb(CONTENT_DB, CONTENT_HOST, CONTENT_USER, CONTENT_PASS)
>>>>>>> .r596
        self.db2.connect()

    ## returns the location of the content ID
    # @param content_id
    # @return list of locaions, e.g. ['Europa', 'France', 'Centre']
    @MemoryCached
    def getGeoNameFromContentID(self, content_id):

        id = content_id
        query = self.QUERY_CONTENT_ID % content_id 
        result = self.db2.query(query)

        if result == []:
            return 'ContentID not found!'
        else:
            gaz_id = result[0]['gazetteer_id']
            return Gazetteer.getGeoNameFromGazetteerID(self, gaz_id)

    ## returns the location of the GazetteerEntry ID  
    # @param gazetteer-entry ID  
    # @return list of locations, e.g. ['Europa', 'France', 'Centre']
    @MemoryCached
    def getGeoNameFromGazetteerID(self, gazetteer_id):
        
        self.parents = []

        result = self.__getGazetteer(gazetteer_id)
        result.reverse()

        if result == []:
            return 'GazetteerID not found!'
        else:
            return result

<<<<<<< .mine
    @MemoryCached
=======
    ## returns the geoname for the given String
    # @param string
    # @return dictionary of locations
>>>>>>> .r596
    def getGeoNameFromString(self, name):
<<<<<<< .mine
        """ implement me """
        query = '''SELECT entity_id FROM gazetteerentry JOIN hasname ON (gazetteerentry.id = hasname.entry_id) WHERE name = '%s' '''
=======
>>>>>>> .r596

        res = set()

<<<<<<< .mine
        for result in self.db.query(query % name.replace("'", "''")):
            try:
                tmp = Gazetteer.getGeoNameFromGazetteerID(self, result['entity_id'])
                res.add( tuple(tmp) )
            except GazetteerEntryNotFound:
                pass
=======
        for result in self.db.query(QUERY_NAME % name):
            tmp = self.getGeoNameFromGazetteerID(result['entity_id'])
            list.append(tmp)
        
        return list
>>>>>>> .r596

        return list(res)


    ## builds the full location
    # @param id
    # @returns list of locations
    def __getGazetteer(self, id):
        list = []
        list.append(self.__getPreferredGeoName(id))

        parent = self.__hasParent(id)

        if parent:
            list.extend(self.__getGazetteer(parent))

        return list

    ## gets the preferred name for the location
    # @param id
    # @returns preferred name
    def __getPreferredGeoName(self, id):
        """ returns the preferred entry name for the given
            entity id
            @param[in] entity_id 
            @returns the geo entity's name
        """ 

        query = '''SELECT name FROM vw_gazetteer_c5000 WHERE id=%d 
                      ORDER BY (lang='en' and lang is not null) DESC,
                            preferred DESC
                      LIMIT 1''' % (id)
        result = self.db.query(query)
        if not result:
            raise GazetteerEntryNotFound(id)

        return result[0]['name']

    ## checks if the given ID has a parent
    # @param ID of the child
    # @return false or ID of the parent 
    def __hasParent(self, child_id):
        query = self.QUERY_HAS_PARENT % child_id
        result = self.db.query(query)
        
        # todo: is it necessary, that this functions can process multiple parents?
        if result.__len__() > 1:
            print '### result > 1 ###'
            print '    child_id:  %s' % child_id
            print '    parent_id: %s ' % parent_id


        # todo: does it make sense to fetch infinite loops
        if result == []:
            return 0 
        else:
            return result[0]["parent_id"]

<<<<<<< .mine
class TestGazeteer(object):
    
    def __init__(self):
        self.gazetteer = Gazetteer()
    
    def testUniqueStringResolver(self):
        assert Gazetteer.getGeoNameFromString( self.gazetteer, "Lainach" ) == []
        assert len(Gazetteer.getGeoNameFromString( self.gazetteer, "Vienna")) == 3

    def testContentIdResolver(self):
        assert Gazetteer.getGeoNameFromContentID(self.gazetteer, 86597672) == ['Europe', 'France', 'Centre']
    

=======

>>>>>>> .r596
if __name__ == "__main__":
    a = Gazetteer()
    if sys.argv.__len__() > 1:
        print a.getGeoNameFromContentID(sys.argv[1])
    else:
        print a.getGeoNameFromContentID(86597672)
        print a.getGeoNameFromContentID(90160635)
        print a.getGeoNameFromString('Vienna')
<<<<<<< .mine
        print a.getGeoNameFromString( "Lainach" )
        print a.getGeoNameFromString( "Spittal an der Drau" )
        print a.getGeoNameFromString( "Salzburg" )

=======
        print a.getGeoNameFromString('China')
        print a.getGeoNameFromString('Wien')
>>>>>>> .r596
