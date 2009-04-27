#!/usr/bin/env python

""" install libsts :) """

from distutils.core import setup
from sys import exit

setup(
      ###########################################
      ## Metadata
      name="eWrt",
      version      = "0.2",
      description  = 'eWrt',
      author       = 'Albert Weichselbraun, Heinz Lang',
      author_email = 'albert.weichselbraun@wu-wien.ac.at, heinz.lang@wu-wien.ac.at',
      url          = 'http://www.semanticlab.net/index.php/EWRT',
      license      = "GPL3", 
      package_dir  = {'eWrt': 'src'},

      ###########################################
      ## Scripts
      scripts = ['src/input/corpus/reuters/reuters.py' ],
 
      ###########################################
      ## Package List
      packages     = ['eWrt',
                      'eWrt.access',
                      'eWrt.input',
                      'eWrt.input.corpus',
                      'eWrt.input.corpus.reuters',
                      'eWrt.util',
                      'eWrt.ws',
                      'eWrt.ws.amazon',
                      'eWrt.ws.delicious',
                      'eWrt.ws.opencalias',
                      'eWrt.ws.wikipedia',
                     ],

      ###########################################
      ## Package Data
)
