#!/usr/bin/env python

""" @package eWRT.ws.amazon
    provides access to amazon data """

# (C)opyrights 2008 by Albert Weichselbraun <albert@weichselbraun.net>
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



__revision__ = "$Revision$"


import time
import logging

from urllib import quote
from xml.parsers.expat import ParserCreate
from eWRT.access.http import Retrieve
from eWRT.config import AMAZON_ACCESS_KEY, AMAZON_LOCATIONS, AMAZON_DEBUG_FILE

from time import strftime

import base64
import hashlib
import hmac
import urllib

# time to wait after an error in seconds
ERROR_SLEEP_TIME = 30

BROWSE_NODE_ID = { 'book' : '283155',
                   'dvd'  : '130',
                   'music': '5174'
                 }

class ResultList:
    """ converts xml results into a list of dictionaries """

    def __init__(self, targetPath, hunt=()):

        assert(isinstance(targetPath, str))

        self.p = ParserCreate()
        self.p.StartElementHandler = self.startElement
        self.p.EndElementHandler = self.endElement
        self.p.CharacterDataHandler = self.charData

        self.xmlResult = []
        self.targetPath = targetPath
        self.path = []

        self.hunt = hunt
        self.huntValue = {}


    def startElement(self, element, attrs):
        """ start Element handler """
        self.path.append(element)
        if self.targetPath == "/".join(self.path):
            self.xmlResult.append({})
        

    def charData(self, data):
        """ adds data to the dictionary """
        currentElement = self.path[-1] 
        if self.targetPath in "/".join(self.path):
                    try:
                        self.xmlResult[-1][ currentElement ] = self.xmlResult[-1].get(currentElement, "") + data.encode("utf8")
                    except IndexError:
                        raise "Given Search Path '%s' is not a Sub-Path of '%s'\n" % ("/".join(self.path), self.targetPath)
                
        if currentElement in self.hunt:
            self.huntValue[currentElement] = data.encode("utf8")
            

    def endElement(self, element):
        assert(self.path)
        self.path.pop()


    def parse(self, data):
        """ parses xml data """
        self.p.Parse(data)


    def parseNew(self, data):
        self.path = []
        self.p.Parse(data)


    def test(self):
        self.parse(open("a.xml").read())
        print self.xmlResult



class AmazonWS:
    """ This class provides low level amazon web service access """
    
    def __init__(self, location='us', key=None):
        """ init """
        assert (location in AMAZON_LOCATIONS)
        self.retrieve = Retrieve(self.__class__.__name__)
        self.wsBase = AMAZON_LOCATIONS[ location ]
        self.accessKey = key or AMAZON_ACCESS_KEY
        self.amazon_url = AmazonUrl()


    def generateWsUrl(self, arguments):
        """ generates a valid amazon webservice request url """
        argList = [ "%s&SubscriptionId=%s" % (self.wsBase, self.accessKey) ] + [ "%s=%s" % (k, quote(v)) for k, v in arguments.items() ]
        return "&".join(argList)

    def generateSignedWsUrl(self, **arguments):
        """ generates a valid amazon webservice request url """
        #argList = [ "%s&SubscriptionId=%s" % (self.wsBase, self.accessKey) ] + [ "%s=%s" % (k,quote(v)) for k,v in arguments.items() ]
        #return "&".join(argList)
        return self.amazon_url.get_request_url(arguments)


    def query(self, arguments):
        """ retrieves a result from amazon webservice """
        url = self.generateWsUrl(arguments)

        done = False
        while not done:
            try:
                f = self.retrieve.open(url)
                res = f.read()
                self._write_debug_data(res)
                f.close()
                done = True
            except ValueError:
                logging.warning("Exception webservice query - waiting for %d seconds...\n" % ERROR_SLEEP_TIME)
                time.sleep(ERROR_SLEEP_TIME)
        return res

        @staticmethod
        def _write_debug_data(data):
            """ writes the given data to the debug file, if specified """
            if not AMAZON_DEBUG_FILE:
                return

            d = open(AMAZON_DEBUG_FILE, "a")
            d.write(data)
            d.close()



    def searchItem(self, searchIndex='Books', **param):
        """ searches an item in the amazon product repository """
        arguments = { 'Operation'    : 'ItemSearch',
                      'SearchIndex'  : searchIndex,
                  'BrowseNode'   : '1000',
                  'Sort'         : 'salesrank',
                  'ResponseGroup': 'SalesRank,Small'}

        arguments.update(param)
        return self.query(arguments)


    def queryReview(self, itemId, **param):
        """ queries customers reviews to the selected Item """
        arguments = { 'Operation' : 'ItemLookup',
                      'ResponseGroup': 'Reviews',
                      'ItemId'    : itemId }
        arguments.update(param)
        return self.query(arguments)


        def newReleases(self, **param):
            """ returns a list of asins of new releases """
            arguments = { 'Operation'    : 'BrowseNodeLookup',
                          'ResponseGroup': 'NewReleases',
                          'Marketplace'  : 'us' }

            arguments.update(param)
            return self.query(arguments)


        def itemAttributes(self, item_id, **param):
            """ returns all item attribues """
            arguments = {'Operation'    : 'ItemLookup',
                         'ItemId'       : item_id,
                         'IdType'       : 'ASIN',
                         'ResponseGroup': 'ItemAttributes,SalesRank' }
            arguments.update(param)
            return self.query(arguments)


AWS_ACCESS_KEY_ID = {'AWSAccessKeyId': AMAZON_ACCESS_KEY}

class AmazonUrl:

    def timestamp(self):
        """ determine the current timestamp """
        current_timestamp = strftime('%Y-%m-%dT%H:%M:%SZ')
        return {'Timestamp': current_timestamp}

    def get_signature(self, msg):
        """ apply hmac with sha256 to the msg using key """
        hmac_sha256_alg = hmac.new(self.access_key, msg, hashlib.sha256)
        signature = hmac_sha256_alg.digest()
        signature = base64.encodestring(signature)
        return signature

    def get_msgs(self, params):
        """ determine the sig_msg (i.e. the message to be hmac encoded) and the
        url_msg (i.e. the message to be sent to amazon) """

        GET = 'GET'
        ECS = 'ecs.amazonaws.com'
        ONCA = '/onca/xml'
        
        params.update(self.timestamp())
        params.update(AWS_ACCESS_KEY_ID)
        url_encoded = urllib.urlencode(params)

        msg = [entry for entry in url_encoded.split('&')]
        msg.sort() # amazon also calculates signature from sorted entries
        msg = '&'.join(msg)

        sig_msg = '\n'.join([GET, ECS, ONCA, msg])
        url_msg = '%s%s%s?%s' % ('http://', ECS, ONCA, msg)
        return url_msg, sig_msg

    def get_request_url(self, params):
        """ generate a url containing signature and timestamp with the given
        parameters """
        url_msg, sig_msg = self.get_msgs(params)
        signature = self.get_signature(sig_msg)
        request_url = "%s&%s" % (url_msg, urllib.urlencode({ 'Signature': signature }))
        return request_url.replace('%0A', '')

if __name__ == "__main__":
    url_generator = AmazonWS()
    url = url_generator.generateSignedWsUrl(Operation='BrowseNodeLookup', Service='AWSECommerceService', ResponseGroup='NewReleases', Marketplace='us', BrowseNodeId='281052')
    print url
