#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" install eWRT :) """
import sys

from setuptools import setup, find_packages

from sys import exit

setup(
    ###########################################
    # Metadata
    name="eWRT",
    version="3.0.0.20190729-dev",
    description='eWRT',
    author='Albert Weichselbraun, Heinz Lang, Gerhard Wohlgenannt, Johannes Duong, Norman Süsstrunk, Daniel Streiff',
    author_email='albert@weblyzard.com, lang@weblyzard.com, wohlg@ai.wu.ac.at, johannes.duong@wu.ac.at, norman.suestrunk@htwchur.ch, daniel.streiff@htwchur.ch',
    url='http://www.weblyzard.com/ewrt/',
    license="GPL3",
    package_dir={'': 'src'},
    install_requires=['redis',
                      'google-cloud-storage==1.10.0',
                      'oauth2client==2.2.0',  # YT
                      'google-api-python-client==1.4.0',  # YT,
                      'six',
                      'gdata',
                      'wikipedia',
                      'pywikibot',
                      'bz2file',
                      'googleads==19.0.1' if sys.version_info.major == 2 else 'googleads',
                      #                         'python-oauth2' #linkedin
                      ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],


    ###########################################
    # Run unittests 
    # NOTE: is this still needed with gitlab-ci in place?
    test_suite='nose.collector',

    ###########################################
    # Scripts
    scripts=['src/eWRT/input/corpus/reuters/reuters.py'],

    ###########################################
    # Package List
    packages=find_packages('src'),

    ###########################################
    # Package Data
    package_data={'eWRT.stat.language': ['data/*.csv'],
                  'eWRT.input.stock': ['data/*.csv'],
                  },
)
