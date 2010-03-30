from __init__ import Flickr
import unittest

class TestFlickr( unittest.TestCase ):
    ''' Testing Flickr webservice '''
    
    def testMultipleTags( self ):
        """ verifies whether multiple tags return results different from single tags """
        
        print '### Testing multiple ###'
        
        assert Flickr.getRelatedTags( ("berlin", "dom")) != Flickr.getRelatedTags( ("berlin",) ) 
        assert Flickr.getTagInfo( ("berlin", "dom") ) != Flickr.getTagInfo( ("berlin",) ) 

    def testTagInfo( self ):
        """ test the tag info """
        
        print '### Testing tag info ###'
        
        for tags in ( ('berlin','dom') , ('vienna',),  ('castle',)):
            count = Flickr.getTagInfo( tags )
            print '%s has tag count: %s' % (tags, count )
            assert count > 0

    def testRelatedTags( self ):
        """ test related tags by retrieving related tags for the following tags """
        
        print '### Testing related tags ###'
        
        tags = ('berlin', 'dom')
        count = Flickr.getRelatedTags( tags )
        print '%s has related tags: %s' % (tags, Flickr.getRelatedTags( tags ))
        assert count > 0
        count = Flickr.getRelatedTags( tags )
        print '%s has related tags: %s' % ('berlin', Flickr.getRelatedTags( tags ))
        assert count > 0

if __name__ == '__main__':
    unittest.main()