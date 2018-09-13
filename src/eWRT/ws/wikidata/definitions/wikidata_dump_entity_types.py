#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Modified on August 31

@author: jakob <jakob.steixner@modul.ac.at>

WIP: define different entity types and their specific
treatment for the purpose of grabbing data from the
wikidata dump.
'''

from wl_data_scripts.projects.wikibot.data import *

class EntityType:
    """"""
    SUBCLASS_QUERY = """SELECT ?class ?classLabel WHERE {
  ?class wdt:P279* wd:Q1656682 .
  SERVICE wikibase:label { 
		bd:serviceParam wikibase:language "en"	}
  }"""

    FUSEKI_CLIENT = FusekiWrapper('http://query.wikidata.org')

    def __init__(self, entity_type_label, entity_type_wdids, subclasses_ids, output_file_path=None):
        self.entity_type_label = entity_type_label
        if subclasses_ids == None:
            try:
                self.subclasses_ids = self.get_subclasses_from_csv()
            except IOError:
                self.subclasses_ids = self.get_subclasses_from_sparql(entity_type_wdids)
        else:
            self.subclasses_ids = subclasses_ids
        self.subclasses_idset = frozenset(self.subclasses_ids)
        self.entity_type_label = entity_type_label
        self.entity_type_wdids = entity_type_wdids
        self.output_file_path = output_file_path

    def get_subclasses_from_csv(self):
        """"""
        with open(self.entity_type_label + '_subclasses.csv') as entity_type_subtypes:
            type_types_csv = list(csv.reader(person_types))[1:]
            self.subclasses_ids = {entry[0].split('/')[-1]: entry[1] for entry in
                                   type_types_csv}
            self.subclasses_idset = frozenset(person_subclasses_dict.keys())

    def get_subclasses_from_sparql(self, wdids):
        ids = []
        for subclass_id in wdids:
            query = self.SUBCLASS_QUERY % subclass_id
            ids.extend(list(self.FUSEKI_CLIENT.run_query(query=query)))
        return {entry['class']['value']: entry['classLabel']['value'] for entry in ids}


