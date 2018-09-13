import glob
import ujson
from pprint import pprint
import subprocess as sb
from collections import Counter

class OutputStatistics:

    def __init__(self, paths=None, data=None, total_length=0):
        if not data and not paths:
            raise ValueError("One of data and paths has to be set!")
        self.total_length = total_length

        self._data = data
        self.paths = paths
        self.malformed = 0
        self.unset = Counter()

    @property
    def data(self):
        if self._data:
            self.data = self._data
        else:
            for path in self.paths:
                try:
                    yield self.from_json(path)
                except Exception as e:
                    print('encountered exception: {}'.format(e))
                    self.malformed += 1

    def from_json(self, filename):
        with open(filename) as json_dump:
            return ujson.load(json_dump)

    @classmethod
    def from_glob(cls, glob_string):
        file_list = glob.glob(glob_string)
        return OutputStatistics.from_pathlist(file_list, total_length=len(file_list))

    @classmethod
    def from_pathlist(cls, paths):
        return OutputStatistics(paths=paths, total_length=len(paths))

    def count_attribute_set(self, attr):
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
