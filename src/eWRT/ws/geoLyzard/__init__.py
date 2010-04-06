#!/usr/bin/env python

from xmlrpclib import ServerProxy, Error
from eWRT.config import GEOLYZARD_URL, GEOLYZARD_GAZETTEERS
from eWRT.util.cache import DiskCached
from base64 import b64decode, b64encode
from operator import itemgetter
from gzip import GzipFile
from StringIO import StringIO
import csv
import sys
try:
    import psyco
    psyco.full()
except ImportError:
    pass

DEFAULT_BATCH_SIZE = 5

def _pack(data):
    """ prepares the data for transmittion to the tagger. """
    
    outData = StringIO()
    d = GzipFile( mode="w", fileobj = outData )
    d.write(data)
    d.close()
    return b64encode( outData.getvalue() )

def _unpack(data):
    """ handles data returned from the tagger """
    return b64decode( data )
    # no uncompression is required because the returned data
    # is not compressed :)
    #
    # d = GzipFile( fileobj = StringIO( b64decode( data) ) )
    # res = d.read()
    # d.close()
    # return res


class GeoLyzardIterator(object):
    """ An iterator performing more efficient queries to the geoLyzard tagger """

    def __init__(self, documents, gazetteer="C", batch_size = DEFAULT_BATCH_SIZE ):
        """ @param[in] documents A dictionary of input documents to tag """
        self.documents     = documents.iteritems()
        self.batch_size    = batch_size
        self.xmlrpc_server = ServerProxy( GEOLYZARD_URL )
        self.gazetteer     = gazetteer
        self.result        = []

    def __iter__(self): return self


    def next(self):
        if not self.result:
            self.fetch_next_batch()

        if self.result:
            return self.result.pop()
        else:
            raise StopIteration

    def fetch_next_batch(self):
        """ processes the next batch of documents """
        tagger_input_dict = dict( [ (str(seq), _pack(text)) for nr, (seq, text) in zip(xrange(self.batch_size), self.documents)  ] )
        self.result = GeoLyzard.unpackTaggerResult( 
                         self.xmlrpc_server.Tagger.getTextGeoLocation( self.gazetteer, tagger_input_dict )).items()


class GeoLyzard(object):
    """ An xmlrpc object around the geoLyzard tagger """

    @staticmethod
    def getServerHandle():
        """ returns a handle to the geoLyzard Web service """
        return ServerProxy( GEOLYZARD_URL ).Tagger

    @staticmethod
    @DiskCached("./.geoLyzard")
    def getGeoEntities( text, gazetteer="C", compress=True ):
        """ determins the geoEntites occurring in the given text
            @param[in] input text
            @param compress: if retrieving geoEntities fails, try setting compress to False
            @returns a list of geographic entities
        """
        xmlrpc_server = ServerProxy( GEOLYZARD_URL )

        if compress:
            content = _pack(text)
        else:
            content = b64encode(text)

        annotations = xmlrpc_server.Tagger.getTextGeoLocation( gazetteer, { 'id': content } )

        res = GeoLyzard.unpackTaggerResult( annotations )

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
    def unpackTaggerResult( res ):
            """ unpacks the taggers results """
            for resultList in res.itervalues():
                    for listDict in resultList:
                            listDict['name'] = _unpack( listDict['name'] )
            return res

class TestGeoLyzard(object):

    def testGeoLyzardIterator(self):
        input_dict = { 1: 'Lainach is a village in Carinthia',
                       2: 'Spittal an der Drau is a district located in the most southern district of Austria',
                       3: 'Ana lives in Vienna.',
                       4: 'Jasna lives in Vienna, the capital of Austria',
                       5: 'Parik lives in Perth'
                     }

        for seq, result in enumerate( GeoLyzardIterator( input_dict )):
            assert len(result) > 0

        print "SEQ: ", seq
        assert seq == len(input_dict)-1


if __name__ == '__main__':
        #TEXT = "Lainach is a village in the district Spital an der Drau. Both are located in Carinthia, the most soutern state of Austria"
        TEXT = "Perth is a wonderfull city in Australia."
        res = GeoLyzard.getGeoEntities( TEXT )
        print res
        myCatch = GeoLyzard.getMostRelevantEntity( res )
        occurrences = GeoLyzard.getOccurrences( res )
        print res, myCatch
        print myCatch['entity_id'], myCatch['name'], myCatch['occurrences'], myCatch['focus_points'], myCatch['confidence']
        print "---"
        print ", ".join( [ o['name'] for o in occurrences ] )

