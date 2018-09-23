#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on September 22, 2018

@author: jakob <jakob.steixner@modul.ac.at>
'''
import pytest

from eWRT.ws.wikidata.extract_meta import collect_entities_iterative

expected_result = [(1, 2)]


@pytest.mark.parametrize('a,b', expected_result)
@pytest.mark.xfail(reason='WIP')
def test_collect_entities_iterative(a, b, expected_result):
    assert collect_entities_iterative(2, 2, languages=['en'],
                                      include_literals=False,
                                      entity_type='person',
                                      wd_parameters=['P18']) == expected_result


def test_collecct_attributes_from_wd_and_wd():
    pass


if __name__ == '__main__':
    import pprint
    from eWRT.ws.wikidata.wp_to_wd import wikidata_from_wptitle

    obama = wikidata_from_wptitle('Barrack Obama')
    wd_parameters = [
        'P18',  # image
        'P17',  # country
        'P19',  # place of birth
        'P39',  # position held
        'P569',  # date of birth
        'P570',  # date of death
        'P1411'  # nominated for
    ]
    pprint.pprint(collect_attributes_from_wd_and_wd(obama,
                                                    languages=['de', 'en',
                                                               'hr'],
                                                    wd_parameters=wd_parameters,
                                                    include_literals=False))
