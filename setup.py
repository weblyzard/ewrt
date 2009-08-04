#!/usr/bin/env python

""" install libsts :) """

from distutils.core import setup
from sys import exit

setup(
      ###########################################
      ## Metadata
      name="eWRT",
      version      = "0.3",
      description  = 'eWRT',
      author       = 'Albert Weichselbraun, Heinz Lang',
      author_email = 'albert.weichselbraun@wu-wien.ac.at, heinz.lang@wu-wien.ac.at',
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
                      'eWRT.input',
                      'eWRT.input.corpus',
                      'eWRT.input.corpus.reuters',
                      'eWRT.util',
                      'eWRT.ws',
                      'eWRT.ws.amazon',
                      'eWRT.ws.delicious',
                      'eWRT.ws.facebook',
                      'eWRT.ws.googletrends',
                      'eWRT.ws.opencalias',
                      'eWRT.ws.twittertrends',
                      'eWRT.ws.wikipedia'
                     ],

      ###########################################
      ## Package Data
)
