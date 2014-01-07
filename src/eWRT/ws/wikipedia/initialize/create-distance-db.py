#!/usr/bin/env python

""" creates the distance database based on a wikipedia dump
"""

# -----------------------------------------------------------------------------------
# (C)opyrights 2010 by Albert Weichselbraun <albert@weichselbraun.net>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------------------

from sys import stdin
import re
import xml.parsers.expat

quote_str = lambda x: "'%s'" % x.replace("'", "''").replace("_", " ").replace("\\", "").encode("utf8").lower().replace("\"", "")

class WikiParse(object):

    RE_REDIRECT = re.compile("#REDIRECT\s*:?\s*\[\[\s*:?\s*(.*?)(?:\]\]|\||#)", re.I)
    RE_LINK     = re.compile("\[\[([^\]^\|]+)(?:\||\]\])", re.I | re.M)

    INSERT_FUNCTION = "wiki_insert"

    def __init__(self):
        self.p = xml.parsers.expat.ParserCreate()

        self.p.StartElementHandler  = self.start_element
        self.p.EndElementHandler    = self.end_element
        self.p.CharacterDataHandler = self.char_data

        self.container = None
        self._clear()
	self.count = 0
	self.prn   = False


    def _clear(self):
        self._wiki_concept   = ""
        self._wiki_links     = set()
        self._wiki_redirects = set()

       
    # 3 handler functions
    def start_element(self, name, attrs):
        self.container = name.lower()

    def end_element(self, name):
        if name == 'page':
            if self._wiki_concept.startswith("'Wikipedia:"):
            	self.clear()
		return

	    #if self.prn:
	    if self._wiki_concept in self._wiki_redirects:
		self._wiki_redirects.remove( self._wiki_concept )
	    if self._wiki_concept in self._wiki_links:
		self._wiki_links.remove( self._wiki_concept )
	    self._wiki_links = self._wiki_links.difference(self._wiki_redirects)  # remove redirects from links

	    print "SELECT %s(%s, ARRAY[%s]::text[], ARRAY[%s]::text[]);" % (self.INSERT_FUNCTION,
		       self._wiki_concept,
		       ",".join( self._wiki_redirects ),
		       ",".join( self._wiki_links ), )
            #else:
            #        if self._wiki_concept == "'template:australian rules football'":
            #        	self.prn = True

            self._clear()

                                                  

    def char_data(self, data):
        if self.container == 'title':
            self._wiki_concept = quote_str(data)
            self.container = ''
        elif self.container == 'text':
            self._wiki_redirects = self._wiki_redirects.union( map(quote_str, self.RE_REDIRECT.findall(data)) )
            self._wiki_links     = self._wiki_links.union( map(quote_str, self.RE_LINK.findall(data)) )

    def parse(self, fhandle):
        self.p.ParseFile(fhandle)



w = WikiParse()
w.parse(stdin)

