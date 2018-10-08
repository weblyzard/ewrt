#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on October 03, 2018

@author: jakob <jakob.steixner@modul.ac.at>

Split from wikibot_parse_item.ParseItemPage for dependency reasons
'''

from pywikibot import Claim
from pywikibot.site import DataSite


def attribute_preferred_value(claim_instances):
    """When an attribute has several instances, try to
    retrieve the one with rank=preferred. Raises a ValueError
    when no or more than one `preferred` instances are found.
    :param claim_instances: List of `Claim`s.
    :returns a 1-member list containing the unique `preferred`
        value, or the input list if it has length 1. Raises
        ValueError otherwise."""

    if len(claim_instances) == 1:
        return claim_instances
    else:
        try:
            claim_instances = [Claim.fromJSON(DataSite('wikidata', 'wikidata'), claim_instance) for claim_instance in claim_instances]
        # for claim_instance in claim_instances:
        #     try:
        #         claim_instance = Claim.fromJSON(DataSite('wikidata', 'wikidata'), claim_instance)
        #     except:
        #         pass
        #     try:
        #         claim_instance.get()
        except TypeError:
                pass
        preferred = [
            claim for claim in claim_instances if claim.rank == 'preferred']
        if len(preferred) == 1:
            return [claim for claim in preferred]

            pass
        elif len(preferred) == 0:
            raise ValueError('No claim instance marked as preferred!')
        else:
            raise ValueError(
                'Incorrectly tagged data: several instances '
                'marked as preferred, this should not happen!')
        # return [claim.target for claim in preferred]

