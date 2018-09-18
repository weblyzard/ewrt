#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on September 10, 2018

@author: Jakob Steixner, <jakob.steixner@modul.ac.at

Retrieve Wikidata's image based on (exact) Wikipedia
article in any language. Also allows to retrieve other
types of images (e.g. flags, coats of arms, etc.) where given.

'''

import glob
import ujson
from collections import Counter


class OutputStatistics:
    """Tools to process statistics about the results from
    a batch of items processed by
    eWRT.ws.wikidata.extract_meta.collect_attributes_from_wd_and_wd"""

    def __init__(self, paths=None, data=None, total_length=0):
        if not data and not paths:
            raise ValueError("One of data and paths has to be set!")
        self.total_length = total_length

        self._data = data  # data provided as list of dicts
        self.paths = paths  # list of paths to load sub results one by
        # one save memore when working with large datasets
        self.malformed = 0
        self.unset = Counter()  # counter properties: number of items
        # where this property is not set.

    @property
    def data(self):
        """The as a list/generator of dicts as formatted by
        eWRT.ws.wikidata.extract_meta.collect_attributes_from_wd_and_wd """
        if self._data:
            self.data = self._data
        else:
            for path in self.paths:
                try:
                    yield self.json_load(path)
                except Exception as e:
                    print('encountered exception: {}'.format(e))
                    self.malformed += 1

    def json_load(self, filename):

        with open(filename) as json_dump:
            return ujson.load(json_dump)

    @classmethod
    def from_glob(cls, glob_string):
        """data as generator over json files, specified by glob string"""
        file_list = glob.glob(glob_string)
        return OutputStatistics.from_pathlist(file_list)

    @classmethod
    def from_pathlist(cls, paths):
        """explicit list of paths"""
        return OutputStatistics(paths=paths, total_length=len(paths))

    def count_attribute_set(self, attr):
        """count the number of items in the data
        where the attribute `attr` is set
        :param attr: str identifying a property"""
        attr_present = 0
        for item in self.data:
            if attr in item:
                if item[attr]['values']:
                    attr_present += 1
                    continue
                else:
                    self.unset[attr] += 1
        return attr_present

    def count_at_least_one(self, attributes):
        """count the number of items where at
        least one of several related attributes, e.g.
        temporal or geographic, is set."""
        neither = []
        attr_present = 0
        for item in self.data:
            if any([attr in item and item[attr]['values'] for attr in attributes]):
                attr_present += 1
                print(item['url'])
                continue

            else:
                neither.append({
                    'wp_url': item['url'],
                    'wd_url': item['wikidata_id']
                })
        self.unset[tuple(attributes)] = neither
        with open('testoutput/geo_attributes_unset.json', 'w') as dump:
            ujson.dump(neither, dump, indent=2, escape_forward_slashes=False)
        return attr_present


if __name__ == '__main__':
    file_list = glob.glob('/tmp/entity_enrichment_organization_Q*')

    attribute = 'headquarters location'
    geo_attrs = 'headquarters location', 'country'

    statistics = OutputStatistics.from_pathlist(file_list)
    print('total entities {}'.format(statistics.total_length))
    print('malformed: {}'.format(statistics.malformed))
    statistics.count_at_least_one(geo_attrs)
    for attribute in geo_attrs:
        statistics.count_attribute_set(attribute)
    print(statistics.unset)

# result with a sample run in debugging:
# total entities 96
# malformed: 0
# contains attribute `headquarters location`:  35
# contains attribute `country`:  48
