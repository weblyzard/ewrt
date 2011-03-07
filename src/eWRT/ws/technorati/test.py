#!/usr/bin/env python

import unittest, re
from __init__ import Technorati
from lxml import etree
from datetime import date, timedelta
import time

TECHNORATI_TEST_TAGS = ['linux', ('debian', 'linux') ]

class TestTechnorati(unittest.TestCase):

    def test_tag_info(self):
        print '### Testing tag_info ###'

        countTags = 0

        for tags in TECHNORATI_TEST_TAGS:
            countTags = Technorati.getTagInfo(tags)
            print '%s has %s counts ' % (tags, countTags)

            assert countTags > 0



    def test_related_tags(self):
        print '### Testing related_tags ###'

        print 'not supported by Technorati at the moment'

#        countTags = 0
#        
#        for tags in TECHNORATI_TEST_TAGS:
#            countTags = Technorati.getRelatedTags( tags )
#            print '%s has related tags: %s' % (tags, countTags)
#        assert countTags > 0

    def test_parse_url(self):

        print '### Test parsing URL ###'
        assert Technorati._parseURL('linux') == 'http://technorati.com/search?usingAdvanced=1&q=linux&return=posts&source=advanced-source-all&topic=overall&authority=high'
        assert Technorati._parseURL(('debian', 'linux')) == 'http://technorati.com/search?usingAdvanced=1&q=debian+linux&return=posts&source=advanced-source-all&topic=overall&authority=high'

    def test_get_blog_links(self):
        ''' tests retrieving the blog links '''

        links = Technorati.get_blog_links('climate change', maxResults=10)
        assert len(links) > 0

        links = Technorati.get_blog_links(['climate', 'change'], 20)
        assert len(links) == 20

        links = Technorati.get_blog_links(['climate', 'change'], 33)
        assert len(links) == 33

    def test_max_age(self):
        ''' tests fetching the articles by maxAge '''

        def testMaxAge(age, dimension, maxAge=0):
            if dimension == 'weeks': hours = age * 7 * 24
            elif dimension == 'days': hours = age * 24
            elif dimension == 'hours': hours = age
            elif dimension == 'minutes': hours = 1
            else: hours = age

            root = etree.Element("root")
            div = etree.SubElement(root, "div")
            div.text = '{age} {dimension} ago'.format(age=age, dimension=dimension)
            print 'Testing %s' % div.text
            linkDate = Technorati._getDate(root, 0)
            print 'LinkDate = ', linkDate
            return (date.fromtimestamp(time.time()) - timedelta(hours=hours)) == Technorati._getDate(root, maxAge)

        assert testMaxAge(7, 'weeks')
        assert testMaxAge(12, 'hours')
        assert testMaxAge(23, 'minutes')
        assert testMaxAge(8, 'minutes', 1)
        assert False == testMaxAge(23, 'miasdfasdnutes')
        assert False == testMaxAge(8, 'weeks', 5)
        assert False == testMaxAge(8, 'days', 5)

if __name__ == '__main__':
    unittest.main()
