# #!/usr/bin/python
# # -*- coding: utf-8 -*-
# '''
# Created on Nov 29, 2017
# 
# .. codeauthor: max goebel <mcgoebel@gmail.com>
# '''
# import unittest
# 
# from eWRT.ws.twitter import Twitter
# 
# 
# class TwitterTest( unittest.TestCase ):
# 
#     TWITTER_TEST_TAGS = [ 'linux', ('linux', 'debian') ]
# 
#     def testUrlInfo(self):
#         for tag in self.TWITTER_TEST_TAGS:
#             relTags = Twitter.getRelatedTags(tag)
#             print 'related to %s are %s.'% (tag, relTags )
#             
# if __name__ == '__main__':
#     unittest.main()