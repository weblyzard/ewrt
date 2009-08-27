#!/usr/bin/env python

""" install libsts :) """

from distutils.core import setup
from sys import exit

setup(
      ###########################################
      ## Metadata
      name="eWRT",
      version      = "0.4-1",
      description  = 'eWRT',
      author       = 'Albert Weichselbraun, Heinz Lang',
      author_email = 'albert.weichselbraun@wu.ac.at, heinz.lang@wu.ac.at',
      url          = 'http://www.semanticlab.net/index.php/EWRT',
      license      = "GPL3", 
      package_dir  = {'eWRT': 'src'},

      ###########################################
      ## Scripts
      scripts = ['src/input/corpus/reuters/reuters.py' ],
 
      ###########################################
      ## Package List
      packages     = ['eWRT',
                      'eWRT.access',
                      'eWRT.config',
                      'eWRT.input',
                      'eWRT.input.corpus',
                      'eWRT.input.corpus.reuters',
                      'eWRT.lib',
                      'eWRT.util',
                      'eWRT.ws',
                      'eWRT.ws.amazon',
                      'eWRT.ws.delicious',
                      'eWRT.ws.facebook',
                      'eWRT.ws.flickr',
                      'eWRT.ws.googletrends',
                      'eWRT.ws.opencalais',
                      'eWRT.ws.twittertrends',
                      'eWRT.ws.wikipedia'
                     ],

      ###########################################
      ## Package Data
)
