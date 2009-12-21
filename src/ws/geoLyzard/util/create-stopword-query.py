#!/usr/bin/env python

""" identify-ambiguous-terms.py
    creates a query to mark ambiguous terms
"""

stopwords = [ "'%s'" % line.strip() for line in open("stopword-list.txt") ]

print "UPDATE Gazetteerentry SET isambiguous=TRUE WHERE name in (%s);" % ", ".join( stopwords )
