#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" install eWRT :) """
from setuptools import setup, find_packages

from sys import exit

setup(
      ###########################################
      ## Metadata
      name="eWRT",
      version="0.9.1.9",
      description='eWRT',
      author='Albert Weichselbraun, Heinz Lang, Gerhard Wohlgenannt, Johannes Duong, Norman Süsstrunk, Daniel Streiff',
      author_email='albert@weblyzard.com, lang@weblyzard.com, wohlg@ai.wu.ac.at, johannes.duong@wu.ac.at, norman.suestrunk@htwchur.ch, daniel.streiff@htwchur.ch',
      url='http://www.weblyzard.com/ewrt/',
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
      packages = find_packages('src'),

      ###########################################
      ## Package Data
      package_data={'eWRT.stat.language': ['data/*.csv'],
                    'eWRT.input.stock': ['data/*.csv'],
      },
)
