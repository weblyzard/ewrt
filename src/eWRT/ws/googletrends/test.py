from __init__ import GoogleTrends, LOADED

class TestGoogleTrends( object ):
    ''' Testing GoogleTrends webservice '''
    
    def setUp(self):
        if LOADED:
            self.trends = GoogleTrends()
        
    def testGetTrend(self):
        ''' test getting trends'''
        if LOADED:
            trends = self.trends.getTrends(('Terminator', 'Rambo'))
            print trends
            assert len(trends) > 52
            
            trends =  self.trends.getTrends(('Microsoft', 'Linux', 'Apple'))
            print trends
            assert len(trends) > 52


