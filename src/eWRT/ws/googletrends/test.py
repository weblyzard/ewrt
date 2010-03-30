from __init__ import GoogleTrends
import unittest

class TestGoogleTrends( unittest.TestCase ):
    ''' Testing GoogleTrends webservice '''
    
    def setUp(self):
        self.trends = GoogleTrends()
        
    def testGetTrend(self):
        ''' test getting trends'''
        trends = self.trends.getTrends(('Terminator', 'Rambo'))
        print trends
        assert len(trends) > 52
        
        trends =  self.trends.getTrends(('Microsoft', 'Linux', 'Apple'))
        print trends
        assert len(trends) > 52


if __name__ == '__main__':
    unittest.main()