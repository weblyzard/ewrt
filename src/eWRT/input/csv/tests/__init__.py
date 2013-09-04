#!/usr/bin/env python

from eWRT.input.csv import get_csv_data
from eWRT.util.module_path import get_resource

TEST_FILE = get_resource(__file__, ('test.csv', ))

def test_csv_data():
    CORRECT = ( [1,2],[2,4],[4,6] )
    with open(TEST_FILE) as f:
        for correct, computed in zip(CORRECT, get_csv_data(f,
                                                        ('int(row["a"])', 'int(row["a"])+int(row["b"])'),
                                                        'row["show"]=="True"')):
            print correct, computed
            assert correct == computed
