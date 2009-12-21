#!/usr/bin/env python

from xmlrpclib import ServerProxy, Error
from eWRT.config import GEOLYZARD_URL, GEOLYZARD_GAZETTEERS
from eWRT.util.cache import DiskCached
from base64 import b64decode, b64encode
import csv
import sys
try:
    import psyco
    psyco.full()
except ImportError:
    pass


class GeoLyzard(object):
    """ An xmlrpc object around the geoLyzard tagger """

    @staticmethod
    def getServerHandle():
        """ returns a handle to the geoLyzard Web service """
        return ServerProxy( GEOLYZARD_URL ).Tagger

    @staticmethod
    @DiskCached("./.geoLyzard")
    def getGeoEntities( text, gazetteer="C10000" ):
        """ determins the geoEntites occurring in the given text
            @param[in] input text
            @returns a list of geographic entities
        """
        xmlrpc_server = ServerProxy( GEOLYZARD_URL )
        res = GeoLyzard.__unpackTaggerResult( 
            xmlrpc_server.Tagger.getTextGeoLocation( gazetteer, { 'id': b64encode(text) } ))

        return res


    @staticmethod
    def getMostRelevantEntity( res ):
        """ returns the entry with the highest number of focus points; if 2 entries have the
            same number of focus points, the confidence is used as second criteria
            @param[in] a geotagger tagging result list
            @returns the most relevant geo entity
        """
        if not res:
            return

        current = {'focus_points': 0.0}
        for entity in res.values()[0]:
            if ( float(entity['focus_points']) == float(current['focus_points']) and float(entity['confidence']) > float(current['confidence'])) or \
                 float(entity['focus_points']) > float(current['focus_points']):
                current = entity

        return current

    @staticmethod
    def getOccurrences( res ):
        """ returns a list of geoEntities, which occured at least once in the text
            @param[in] geotagger tagging result list
            @returns occuring geoEntities
        """
        for e in res.values()[0]:
            print "***", e
        return [ e for e in res.values()[0] if int(e['occurrences']) > 0 ]
             

    @staticmethod
    def __unpackTaggerResult( res ):
            """ unpacks the taggers results """
            for resultList in res.itervalues():
                    for listDict in resultList:
                            listDict['name'] = b64decode( listDict['name'] )
            return res


if __name__ == '__main__':
        TEXT = "Lainach is a village in the district Spital an der Drau. Both are located in Carinthia, the most soutern state of Austria"
        res = GeoLyzard.getGeoEntities( TEXT )
        myCatch = GeoLyzard.getMostRelevantEntity( res )
        occurrences = GeoLyzard.getOccurrences( res )
        print res, myCatch
        print myCatch['entity_id'], myCatch['name'], myCatch['occurrences'], myCatch['focus_points'], myCatch['confidence']
        print "---"
        print ", ".join( [ o['name'] for o in occurrences ] )

