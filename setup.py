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
    version="3.0.0-dev",
    description='eWRT',
    author='Albert Weichselbraun, Heinz Lang, Gerhard Wohlgenannt, Johannes Duong, Norman Süsstrunk, Daniel Streiff',
    author_email='albert@weblyzard.com, lang@weblyzard.com, wohlg@ai.wu.ac.at, johannes.duong@wu.ac.at, norman.suestrunk@htwchur.ch, daniel.streiff@htwchur.ch',
    url='http://www.weblyzard.com/ewrt/',
    license="GPL3",
    package_dir={'': 'src'},
    install_requires=['redis',
                      'google-cloud-storage==2.0.0',
                      'oauth2client==4.1.3',  # YT
                      'google-api-python-client==2.42.0',  # YT,
                      'six',
                      'gdata @ git+https://github.com/dvska/gdata-python3#egg=gdata',
                      'wikipedia',
                      'pywikibot==7.0.0',
                      'mwparserfromhell',  # dependency for pywikibot from 6.3.0
                      'bz2file',
                      'googleads==31.0.0' if sys.version_info.major == 2 else 'googleads',
                      'ujson'
                      ],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
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