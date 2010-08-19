#!/usr/bin/env python
"""
Usage:

> calais = Calais(submitter="MyProjectID", api_key="your-opencalais-api-key")
> text = "some text"
> calais.analyze(text)

"""

# Opencalais module
# based on python-calais v.0.2 by Jordan Dimov (jdimov@mlke.net)
# 
# (C)opyrights 2008 by Jordan Dimov <jdimov@mlke.net>
#                      Albert Weichselbraun <albert@weichselbraun.net>
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


from random import choice
from xml.dom import minidom
from eWRT.access.http import Retrieve
from urllib import urlencode
from eWRT.config import OPENCALAIS_KEY, OPENCALAIS_CACHE_DIR, OPENCALAIS_URL, USER_AGENT
from eWRT.util.cache import DiskCache
import re

PARAMS_XML = """
<c:params xmlns:c="http://s.opencalais.com/1/pred/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"> 
<c:processingDirectives c:contentType="%s" c:outputFormat="Text/Simple"> 
</c:processingDirectives> 
<c:userDirectives c:allowDistribution="%s" calculateRelevanceScore="true" c:allowSearch="%s" c:externalID="%s" c:submitter="%s"> 
</c:userDirectives> 
<c:externalMetadata> 
</c:externalMetadata> 
</c:params>
"""

class Calais:
    submitter = USER_AGENT % "Calais"
    allow_distro = "false"
    allow_search = "false" 
    api_key = ""

    def __init__(self, submitter, api_key=OPENCALAIS_KEY, allow_distro="false", allow_search="false", cache_dir=OPENCALAIS_CACHE_DIR):
        """
        Creates a new handler for communicating with OpenCalais.  
                The parameter 'submitter' must contain a string, identifying your application.  
                'api_key' must contain a string with your OpenCalais API key (get it here: http://developer.opencalais.com/apps/register).  
        The optional parameter 'allow_distro', if set to 'true' gives OpenCalais permission to distribute the metadata extracted from your submissions.  The default value for 'allow_distro' is 'false'.  
        The optional parameter 'allow_search', if set to 'true' tells OpenCalais that future searches can be performed on the extracted metadata.  The default value for 'allow_search' is 'false'.  
        """
        assert(api_key) 
        self.submitter = submitter
        self.allow_distro = "false"
        self.allow_search = "false"
        self.api_key = api_key
        if cache_dir:
            self.cache  = DiskCache(cache_dir, cache_nesting_level=2, cache_file_suffix=".xml")

    @staticmethod
    def random_id(self):
        """
        Creates a random 10-character ID for your submission.  
        """
        chars = str.letters + str.digits
        return "".join( [ choice(chars) for i in xrange(10) ] )
    

    @staticmethod
    def content_id(text):
        """
        Creates a SHA1 hash of the text of your submission.  
        """
        try:
            import hashlib
            h = hashlib.sha1()
        except ImportError:
            import sha
            h = sha.new()

        h.update(text)
        return h.hexdigest()


    def analyze(self, text, content_type="text/txt"): 
        """ Submits 'text' to OpenCalais for analysis and memorizes the extracted metadata. 
            Set the content-type to 'text/html' if you are submitting HTML data.  
        """
        externalID = self.content_id( text )
        paramsXML = PARAMS_XML % (content_type, self.allow_distro, self.allow_search, externalID, self.submitter) 
        param = urlencode({'licenseID':self.api_key, 'content':text, 'paramsXML':paramsXML}) 
                
        # do not fetch the data again, if a file exists in the cache
        get_calais_data = lambda x: Retrieve(Calais.__name__).open(OPENCALAIS_URL, x).read()

        if self.cache is None:
            xml_data = self.unpack( get_calais_data( param ) )
        else:
            xml_data = self.unpack( self.cache.fetch( get_calais_data, param ) )

        return self.parse( xml_data )


    @staticmethod
    def unpack(calais_data):
        """ extracts calais' xml response from the data send by the calais 
            webservice 
        """
        dom = minidom.parseString(calais_data)
        return """<?xml version="1.0" encoding="utf-8"?>\n""" \
                 + dom.getElementsByTagName("string")[0].firstChild.data

    @staticmethod
    def cleanup_xml(xml_data):
        """ removes comments from xml-data-streams provided by opencalais
            @param[in] xml_data 
            @returns the xml data without any comments
        """
        result = []
        comment = False

        while '<!--' in xml_data:

            xml_data = re.sub('<!--[\s\S]*?-->', '', xml_data)
            if not re.search('<!--', xml_data):
                break
            
        return xml_data


    @staticmethod
    def parse(xml_data): 
        """ parses opencalai's xml output and returns it's dictionary representation """

        things = []

        xml_data = Calais.cleanup_xml(xml_data)

        # f= open("tmp","w"); f.write(xml_data.encode("utf8")); f.close()
        dom = minidom.parseString( xml_data.encode("utf8" ))
        
        for document in dom.getElementsByTagName("CalaisSimpleOutputFormat"):
            for annotations in document.childNodes:
                if not annotations.hasChildNodes():
                    continue
                
                if annotations.nodeName == 'Topics':
                    annotations = annotations.firstChild
                
                nodeName = annotations.nodeName
                nodeAttr = dict(annotations.attributes.items())
        
                nodeAttr.update( {'data': annotations.firstChild.data } )

                things.append( {nodeName: nodeAttr } )

        return things
