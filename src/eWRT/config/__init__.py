#!/usr/bin/env python

""" @package eWRT.config
    evaluates ~/.eWRT/siteconfig.py and publishes the values"""

# (C)opyrights 2004-2013 by Albert Weichselbraun <albert@weichselbraun.net>
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

import sys
from warnings import warn
from os.path import expanduser, exists, dirname, join as os_join

SYS_EWRT_CONF = "/etc/eWRT/sysconfig.py"
USR_EWRT_CONF = expanduser("~/.eWRT/siteconfig.py")

# commands used to convert various formats to text
CMD_CONV = {'html': '/usr/bin/lynx -stdin -width=20000 -force_html -nocolor -dump -nolist -nobold -pseudo_inlines=0 -assume_charset=%s -display_charset=utf8',
            'pdf' : '/usr/bin/pdftotext -layout - - ',
            'doc' : '/usr/bin/antiword -',
            }

# ===================================================================
# DEFAULT CONFIGURATION VALUES
# - please either create a configuration file in 
#     /etc/eWRT/sysconfig or
#     ~/.eWRT/siteconfig.py
#
#   to overwrite these settings
# ===================================================================


PROXY_SERVER = ''
USER_AGENT = 'eWRT Version/0.5; MODUL <%s> +http://p.semanticlab.net/eWRT'

# default sleep time in seconds
DEFAULT_WEB_REQUEST_SLEEP_TIME = 1

# ===================================================================
# DATABASE CONFIGURATION
# ===================================================================
DATABASE_CONNECTION = {
            'db-name'  : {'host': 'localhost', 'dbname': 'postgres', 'username': '', 'passwd': ''},
    }
 
# ===================================================================
# USERNAMES AND API-KEYS
# ===================================================================

# delicious
DELICIOUS_USER = ''
DELICIOUS_PASS = ''

# opencalais
OPENCALAIS_KEY = ''
OPENCALAIS_CACHE_DIR = ''
OPENCALAIS_URL = "http://api.opencalais.com/enlighten/calais.asmx/Enlighten"

# geoTagger
GEOLYZARD_URL = ''
GEOLYZARD_GAZETTEERS = ''


# amazon
AMAZON_ACCESS_KEY_DICT = { 'user': 'pass',
                         }
AMAZON_ACCESS_KEY = AMAZON_ACCESS_KEY_DICT['user']

# file to copy all xml input from the amazon webservice (the content is only
# copyied if a file is specified)
AMAZON_DEBUG_FILE = ""


# ===================================================================
# PATHS AND URLs
# ===================================================================

AMAZON_LOCATIONS = { 'us': 'http://webservices.amazon.com/onca/xml?Service=AWSECommerceService',
                     'uk': 'http://webservices.amazon.co.uk/onca/xml?Service=AWSECommerceService',
		     'de': 'http://webservices.amazon.de/onca/xml?Service=AWSECommerceService',
		     'jp': 'http://webservices.amazon.co.jp/onca/xml?Service=AWSECommerceService',
		     'fr': 'http://webservices.amazon.fr/onca/xml?Service=AWSECommerceService',
		     'ca': 'http://webservices.amazon.ca/onca/xml?Service=AWSECommerceService' }

# ===================================================================
# CORPUS LOCATIONS
# ===================================================================
CORPUS_DIR = '/data/corpus'
AUTOCLASS_SAMPLE = "reuters-10000-multitoken"

BBC_CORPUS       = os_join( CORPUS_DIR, "news.bbc.co.uk" )
BBC_CORPUS_HTML  = os_join( BBC_CORPUS, "html" )
BBC_CORPUS_LOW   = os_join( BBC_CORPUS, "low" )
BBC_CORPUS_RSS   = os_join( BBC_CORPUS, "rss" )
BBC_CORPUS_PRINT = os_join( BBC_CORPUS, "print" )

BBC_CORPUS_TIMEFORMAT = "%a, %d %b %Y %H:%M:%S %Z"

# COMPRESSED VERSION OF THE CORPUS
BBC_CORPUS_COMPRESSED = "data/news.bbc.co.uk.tar.gz"

# geonames
GEO_ENTITY_SEPARATOR = ">"

# facebook
FACEBOOK_API_KEY = "api-key"
FACEBOOK_SECRET_KEY = "secret-key"
FACEBOOK_SESSION_KEY = "session-key"
FACEBOOK_ACCESS_KEY = "access-key"
FACEBOOK_APPLICATION_ID = "application-id"

SNMP_HOST_CFG = {'server'          : 'localhost',
                 'port'            : '162',
                 'community_string': 'public',
                 'oid'             : 'SNMPv2-SMI::enterprises.30538.5000',
                }

SNMP_MODULE_NAME = {}
SNMP_LOG_LEVEL   = { 'ok': '0', 'warning': '1', 'critical': '2' }

# twitter keys .. gila 
TWITTER_CONSUMER_KEY    = ''
TWITTER_CONSUMER_SECRET = ''
TWITTER_ACCESS_TOKEN    = ''
TWITTER_TOKEN_SECRET    = ''

# --------------------------------------------------------------------------
#
#  Overwrite global config based on 
#   a) the system configuraiton and
#   b) the user configuration.
#
# --------------------------------------------------------------------------
if exists( SYS_EWRT_CONF ):
    sys.path.append( dirname(SYS_EWRT_CONF) )
    try:
        from sysconfig import *
    except ImportError:
        warn("No siteconfig in present.")

if exists( USR_EWRT_CONF ):
    sys.path.append( dirname(USR_EWRT_CONF) )
    try:
        from siteconfig import *
    except ImportError:
        warn("Could not finde siteconfig.py in ~/.eWRT")
    
# $Id$
