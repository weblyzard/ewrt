#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
      version="0.7.6",
      description='eWRT',
      author='Albert Weichselbraun, Heinz Lang, Gerhard Wohlgenannt, Johannes Duong, Norman Süsstrunk',
      author_email='albert@weblyzard.com, lang@weblyzard.com, wohlg@ai.wu.ac.at, johannes.duong@wu.ac.at, norman.suesstrunk@htwchur.ch',
      url='http://www.semanticlab.net/index.php/EWRT',
      license="GPL3",
      package_dir={'': 'src'},

      ###########################################
      ## Run unittests
      test_suite='nose.collector',

      ###########################################
      ## Scripts
      scripts=['src/eWRT/input/corpus/reuters/reuters.py' ],

      ###########################################
      ## Package List
      packages=['eWRT',
                      'eWRT.access',
                      'eWRT.config',
                      'eWRT.input',
                      'eWRT.input.conv',
                      'eWRT.input.clean',
                      'eWRT.input.corpus',
                      'eWRT.input.corpus.reuters',
                      'eWRT.input.corpus.bbc',
                      'eWRT.input.stock',
                      'eWRT.lib',
                      'eWRT.stat',
                      'eWRT.stat.coherence',
                      'eWRT.stat.eval',
                      'eWRT.stat.language',
                      'eWRT.stat.string',
                      'eWRT.ontology',
                      'eWRT.ontology.compare',
                      'eWRT.ontology.compare.terminology',
                      'eWRT.ontology.compare.relations',
                      'eWRT.ontology.compare.relationtypes',
                      'eWRT.ontology.eval',
                      'eWRT.ontology.eval.terminology',
                      'eWRT.ontology.visualize',
                      'eWRT.output.plot',
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
                      'eWRT.ws.google',
                      'eWRT.ws.googletrends',
                      'eWRT.ws.opencalais',
                      'eWRT.ws.rss',
                      'eWRT.ws.technorati',
                      'eWRT.ws.twitter',
                      'eWRT.ws.wikipedia',
                      'eWRT.ws.yahoo',
                      'eWRT.ws.youtube',
                     ],

      ###########################################
      ## Package Data
      package_data={'eWRT.stat.language': ['data/*.csv'],
                    'eWRT.input.stock': ['data/*.csv'],
      },
)
