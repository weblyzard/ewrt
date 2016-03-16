#!/usr/bin/env python
# encoding: utf-8
'''
 @package eWRT.ws.stat.string.normalize
 Normalizes strings prior to the application of distance metrics
'''

# (C)opyrights 2015 by Albert Weichselbraun <albert@weichselbraun.net>
#
# The code published in this module is either under the GNU General
# Public License (see below) or under the license specified in the 
# function. 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# Sources for look-alike characters:
# - http://ux.stackexchange.com/questions/53341/are-there-any-letters-numbers-that-should-be-avoided-in-an-id
# - pwgen source code
OCR_TRANSLATION_TABLE = {ord(u'8'): u'B',
                         ord(u'6'): u'G',
                         ord(u'1'): u'I',
                         ord(u'l'): u'I',
                         ord(u'0'): u'O',
                         ord(u'Q'): u'O',
                         ord(u'5'): u'S',
                         ord(u'2'): u'Z',
                         ord(u'Ä'): u'A',
                         ord(u'Ö'): u'O',
                         ord(u'Ü'): u'U',
                         ord(u'ß'): u'B',
                         ord(u'ä'): u'a',
                         ord(u'ö'): u'o',
                         ord(u'ü'): u'u',
                         ord(u'é'): u'e',
                         ord(u'û'): u'u',
                         ord(u'à') :u'a',
                         ord(u'â') :u'a',
                         }

def ocr_normalize(ocr_text):
    '''
    normalizes OCR text - i.e. provides a normalized representation of 
    characters that are frequently confused.

    ::param ocr_text:
        the unicode representation of the text to normalize
    ::returns:
        the normalized text
    '''
    return ocr_text.translate(OCR_TRANSLATION_TABLE)



# -------------------------------------------------------------------------
#
# Unittests
# 
# -------------------------------------------------------------------------

def test_ocr_normalize():
    assert ocr_normalize(u'002 in Österreich') == u'OOZ in Osterreich'
    assert ocr_normalize(u'6000 Zürich')  == u'GOOO Zurich'

