#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import unittest
from __init__ import GeoLyzard, GeoLyzardIterator
from warnings import warn

class TestGeoLyzard( unittest.TestCase ):

    def testGeoLyzardIterator(self):
        ''' test geoLyzardIterator '''
        input_dict = { 1: 'Lainach is a village in Carinthia',
                       2: 'Spittal an der Drau is a district located in the most southern district of Austria',
                       3: 'Ana lives in Vienna.',
                       4: 'Jasna lives in Vienna, the capital of Austria',
                       5: 'Parik lives in Perth'
                     }

        seq = ''

        for seq, result in enumerate( GeoLyzardIterator( input_dict )):
            assert len(result) > 0

        if not seq == '':
            
            print "SEQ: ", seq
            assert seq == len(input_dict)-1
        else:
            warn('GeoLyzard may not support compresed file transfer')
            
    
    def testGeoLyzard(self):
        ''' test getGeoEntities '''
        
        res = GeoLyzard.getGeoEntities('Lainach is a village in the district Spital an der Drau. Both are located in Carinthia, the most soutern state of Austria.', compress=True)
        print res
        assert res['id'][0]['confidence'] == '0.25'
        assert res['id'][0]['name'] =='Bundesland Kärnten'
        assert res['id'][0]['entity_id'] =='2774686'
        
        
if __name__ == '__main__':
    
    unittest.main()
