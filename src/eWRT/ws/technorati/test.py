#!/usr/bin/env python

import unittest
from __init__ import Technorati

TECHNORATI_TEST_TAGS = ['linux', ('debian', 'linux') ]

class TestTechnorati( unittest.TestCase ):

#    def test_tag_info(self):
#        print '### Testing tag_info ###'
#        
#        countTags = 0
#        
#        for tags in TECHNORATI_TEST_TAGS:
#            countTags = Technorati.getTagInfo( tags )
#            print '%s has %s counts ' % (tags, countTags)
#
#            assert countTags > 0
#
#
#    
#    def test_related_tags(self):
#        print '### Testing related_tags ###'
#        
#        print 'not supported by Technorati at the moment'
#        
##        countTags = 0
##        
##        for tags in TECHNORATI_TEST_TAGS:
##            countTags = Technorati.getRelatedTags( tags )
##            print '%s has related tags: %s' % (tags, countTags)
##        assert countTags > 0
#
#    def test_parse_url(self):
#        
#        print '### Test parsing URL ###'
#        assert Technorati._parseURL('linux') == 'http://technorati.com/search?usingAdvanced=1&q=linux&return=posts&source=advanced-source-all&topic=overall&authority=high'
#        assert Technorati._parseURL(('debian', 'linux')) == 'http://technorati.com/search?usingAdvanced=1&q=debian+linux&return=posts&source=advanced-source-all&topic=overall&authority=high'

    def test_get_blog_links(self):
        ''' tests retrieving the blog links '''
        
        links = Technorati.get_blog_links(['climate', 'change'])
        assert len(links) > 0
        
        links = Technorati.get_blog_links(['climate', 'change'], 20)
        assert len(links) == 20
        
        links = Technorati.get_blog_links(['climate', 'change'], 33)
        assert len(links) == 33


if __name__ == '__main__':
    unittest.main()
