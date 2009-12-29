#!/usr/bin/env python

""" install eWRT :) """

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from sys import exit

setup(
      ###########################################
      ## Metadata
      name="eWRT",
      version      = "0.5",
      description  = 'eWRT',
      author       = 'Albert Weichselbraun, Heinz Lang',
      author_email = 'albert.weichselbraun@wu.ac.at, heinz.lang@wu.ac.at',
      url          = 'http://www.semanticlab.net/index.php/EWRT',
      license      = "GPL3", 
      requires     = [ "psycopg2", ],
      package_dir  = {'': 'src'},

      ###########################################
      ## Scripts
      scripts = ['src/eWRT/input/corpus/reuters/reuters.py' ],
 
      ###########################################
      ## Package List
      packages     = ['eWRT',
                      'eWRT.access',
                      'eWRT.config',
                      'eWRT.convert',
                      'eWRT.input',
                      'eWRT.input.corpus',
                      'eWRT.input.corpus.reuters',
                      'eWRT.input.corpus.bbc',
                      'eWRT.lib',
                      'eWRT.util',
                      'eWRT.ws',
                      'eWRT.ws.amazon',
                      'eWRT.ws.delicious',
                      'eWRT.ws.facebook',
                      'eWRT.ws.flickr',
                      'eWRT.ws.geoLyzard',
                      'eWRT.ws.geonames',
                      'eWRT.ws.geonames.gazetteer',
                      'eWRT.ws.geonames.util',
                      'eWRT.ws.googletrends',
                      'eWRT.ws.opencalais',
                      'eWRT.ws.technorati',
                      'eWRT.ws.twittertrends',
                      'eWRT.ws.twitter',
                      'eWRT.ws.wikipedia',
                      'eWRT.ws.yahoo'
                     ],

      ###########################################
      ## Package Data
)
