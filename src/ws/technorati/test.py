import unittest
from __init__ import Technorati

TECHNORATI_TEST_TAGS = ['linux', ('debian', 'linux')]

class TestTechnorati( unittest.TestCase ):

    def test_tag_info(self):
        print '### Testing tag_info ###'
        for tags in TECHNORATI_TEST_TAGS:
            print '%s has %s counts ' % (tags, Technorati.getTagInfo( tags ))

    
    def test_related_tags(self):
        print '### Testing related_tags ###'
        for tags in TECHNORATI_TEST_TAGS:
            print '%s has related tags: %s' % (tags, Technorati.getRelatedTags( tags ))

if __name__ == '__main__':
    unittest.main()
