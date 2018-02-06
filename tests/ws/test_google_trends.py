# #!/usr/bin/python
# # -*- coding: utf-8 -*-
# import unittest
# 
# from eWRT.ws.googletrends import GoogleTrends, LOADED
# 
# 
# class TestGoogleTrends(unittest.TestCase):
#     ''' Testing GoogleTrends webservice '''
#     
#     def setUp(self):
#         if LOADED:
#             self.trends = GoogleTrends()
#         
#     def testGetTrend(self):
#         ''' test getting trends'''
#         if LOADED:
#             trends = self.trends.getTrends(('Terminator', 'Rambo'))
#             print trends
#             assert len(trends) > 52
#             
#             trends =  self.trends.getTrends(('Microsoft', 'Linux', 'Apple'))
#             print trends
#             assert len(trends) > 52
# 
# if __name__ == '__main__':
#     unittest.main()
