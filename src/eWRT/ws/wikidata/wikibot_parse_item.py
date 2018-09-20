#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Last modified on September 17, 2018

@author: Jakob Steixner, <jakob.steixner@modul.ac.at

Retrieve info about an entity, specifying a list of
relevant attributes and languages for literals

'''
import sys
import warnings

from eWRT.ws.wikidata.definitions import (local_attributes,
                                          image_attributes,
                                          GENERIC_PROPERTIES)
from eWRT.ws.wikidata.get_image_from_wikidataid import get_image, \
    NoImageFoundError
from pywikibot import WbTime

if sys.version_info.major == 3:
    basestring = (bytes, str)

RELEVANT_LANGUAGES = ['en']

TEMPORAL_QUALIFIERS = {'P580': 'start date',
                       'P582': 'end date',
                       'P585': 'point in time',
                       }

# other claim qualifiers we don't want to skip, if present
OTHER_QUALIFIERS = {'P642': 'at_organization',
                    'P854': 'reference_url',
                    'P1686': 'for_work'}

CLAIMS_OF_INTEREST = ["P18", "P19", 'P39', 'P106', 'P108', 'P102']


class ParseItemPage:
    """Methods to parse pywikibot.ItemPage for a specifiable list
        of properties, returning a dict of property labels and values."""
    LITERAL_PROPERTIES = ['labels', 'aliases', 'descriptions']
    
    def __init__(self, itempage, include_literals=False,
                 claims_of_interest=None,
                 entity_type_properties=None, languages=None,
                 require_country=True):
        """
        :param itempage: pywikibot.ItemPage to be parsed
        :param include_literals: bool defining whether to include further literals
        (descriptions, aliases) in the output. If False, only labels are included.
        :param claims_of_interest: list of claims by their WikiData identifiers
        that shall be parsed, if present.
        :param entity_type_properties: dict of property identifiers and their labels
        entity_type_properties.
        :param languages: list of languages of interest in their preferred order
        """
        
        # include 'labels' only if include_literals == False
        itempage.get()
        self.include_literals = include_literals
        if self.include_literals:
            self.literals = self.LITERAL_PROPERTIES
        else:
            self.literals = ['labels']
        self._require_country = require_country
        if languages is None:
            languages = RELEVANT_LANGUAGES
        self.languages = languages
        if not entity_type_properties:
            self.entity_type_properties = GENERIC_PROPERTIES
        
        if claims_of_interest is None:
            self.claims_of_interest = CLAIMS_OF_INTEREST
        else:
            self.claims_of_interest = claims_of_interest
        self._image_requested = {attribute: image_attributes[attribute] for
                                 attribute in
                                 self.claims_of_interest if
                                 attribute in image_attributes}
        
        self.claims_of_interest = [c for c in self.claims_of_interest if
                                   c not in self._image_requested]
        self.item_raw = itempage
        self.process_attributes()
        if not self.include_literals:
            self.details = {key: self.details[key] for key in self.details if
                            self.details[
                                key] and key not in self.LITERAL_PROPERTIES}
    
    def process_attributes(self):
        """Exctract information about the item, specified
        by the predicates in self.claims_of_interest:
          - extract literal attributes
          - find image link(s) (if requested)
          - make best effort attempt to parse
            the other claims_of_interest"""
        
        # special process for retrieving literals
        self.details = self.extract_literal_properties(self.item_raw,
                                                       self.languages,
                                                       self.literals)
        
        # special methods for images
        for image_type in self._image_requested:
            type_literal = self._image_requested[image_type]
            try:
                (self.details[type_literal + '_description'],
                 _,
                 self.details['full_{}'.format(type_literal)]) = get_image(
                    itempage=self.item_raw,
                    image_type=image_type)
            except NoImageFoundError:
                pass
        
        # generic method for other/unkown types of claims
        self.process_other_claims()
    
    def process_other_claims(self):
        """Generic best effort method to parse additional predicates
        and their qualifiers."""
        for claim in self.claims_of_interest:
            try:
                claim_name = self.entity_type_properties[claim]
                claim_instances = self.item_raw.claims[claim]
                if claim_instances:
                    self.details[claim_name] = self.complete_claim_details(
                        claim, claim_instances,
                        languages=self.languages,
                        literals=self.literals, )
                    if self.details[claim_name]:
                        self.details[claim_name]['url'] = \
                            'https://www.wikidata.org/wiki/Property:' + claim
                    else:
                        warnings.warn(
                            'Unable to parse claim {claim} for item {item}, '
                            'should be present!'.format(claim=claim,
                                                        item=self.item_raw))
            
            except KeyError as e:
                pass
            
            # warnings.warn(
            #    'claim {} not available for entity {}'.format(claim, self.details['labels']))
        if 'country' not in self.details or not self.details[
            'country'] and self._require_country:
            country_info = self.get_country_from_any(self.item_raw,
                                                     local_attributes=local_attributes,
                                                     languages=self.languages)
            if country_info:
                self.details['country'] = country_info
        
        for attribute in [a for a in self.details]:
            
            if not self.details[attribute] or 'values' in self.details[
                attribute] and not \
                    self.details[attribute]['values']:
                print('deleting attribute')
                del self.details[attribute]
    
    @classmethod
    def complete_claim_details(cls, claim_id, claim_instances, languages,
                               literals):
        """Find values for specified claim types for which no specific
        handling is defined.
        :param claim_id: Pxx id of the attribute.
        :param claim_instances: list of propositions (pywikibot.Claim instances).
        :param languages: list of languages
        :param literals: list of literal properties to include
        :returns dictionary with claim id, values"""
        values = []
        assert claim_instances
        for sub_claim in claim_instances:
            try:
                value = ParseClaim(sub_claim, languages,
                                   literals).claim_details
                if value:
                    values.append(value)
            except Exception as e:
                pass
        if values:
            wd_prop_url = 'https://www.wikidata.org/wiki/Property:'
            claim_details = {'values': values,
                             'url': wd_prop_url + claim_id}
        else:
            claim_details = {}
        if len(claim_instances) > 1:
            try:
                marked_preferred = cls.attribute_preferred_value(
                    claim_instances)
                if len(marked_preferred) == 1:
                    preferred = marked_preferred[0]
                    try:
                        preferred_id = preferred.id
                        preferred_labels = \
                            ParseItemPage.extract_literal_properties(preferred,
                                                                     languages=languages,
                                                                     literals=[
                                                                         'labels'])[
                                'labels']
                        claim_details['preferred'] = {
                            'url': preferred_id,
                            'labels': preferred_labels
                        }
                    except AttributeError:
                        if isinstance(preferred, WbTime):
                            claim_details['preferred'] = \
                                preferred.toTimestr(force_iso=True)
                        
                        elif isinstance(preferred, basestring):
                            claim_details['preferred'] = preferred
            
            
            except ValueError as e:
                warnings.warn('encountered exception: {}'.format(e))
                
                # ParseItemPage.extract_literal_properties(preferred[0],
                #                                          languages=languages,
                #                                          literals=[
                #                                              'labels'])
        return claim_details if claim_details else None
    
    @classmethod
    def extract_literal_properties(cls, entity, languages, literals=None):
        """Create a dictionary with the entity's labels, descriptions and
        aliases in the selected languages.
        :param entity: pywikibot.Claim() or pywikibot.ItemPage
        :param languages: list of languages by their ISO code for which to
        extract literals
        :param literals: list of literals to parse (default:
        ['labels', 'aliases', 'descriptions']"""
        if literals is None:
            literals = cls.LITERAL_PROPERTIES
        literal_properties = {prop: {} for prop in literals}
        for prop in literal_properties:
            for language in languages:
                try:
                    literal_properties[prop][language] = \
                        entity.text[prop][language]
                except (KeyError, AttributeError):
                    pass
        return literal_properties
    
    @classmethod
    def attribute_preferred_value(cls, claim_instances):
        """When an attribute has several instances, try to
        retrieve the one with rank=preferred. Raises a ValueError
        when no or more than one `preferred` instances are found.
        :param claim_instances: List of `Claim`s.
        :returns a 1-member list containing the unique `preferred`
            value, or the input list if it has length 1. Raises
            ValueError otherwise."""
        
        def gettargets(claim_instances):
            return [claim.target for claim in claim_instances]
        
        if len(claim_instances) == 1:
            return gettargets(claim_instances)
        else:
            for claim_instance in claim_instances:
                try:
                    claim_instance.get()
                except AttributeError:
                    pass
            preferred = [
                claim for claim in claim_instances if claim.rank == 'preferred']
            if len(preferred) == 1:
                return [claim.target for claim in preferred]
                
                pass
            elif len(preferred) == 0:
                raise ValueError('No claim instance marked as preferred!')
            else:
                raise ValueError(
                    'Incorrectly tagged data: several instances '
                    'marked as preferred, this should not happen!')
            # return [claim.target for claim in preferred]
    
    @classmethod
    def get_country_from_location(cls, location_item_page, languages):
        """Get country info from sub-country location.
        :param location_item_page: a location-type entities ItemPage.
        :type location_item_page: pywikibot.ItemPage
        :returns: country of the location as a list of `ItemPage`s.
        :param languages: list of languages
        :returns dictionary"""
        try:
            location_item_page.get()
        except AttributeError:
            raise ValueError(
                'Parameter location_item_page has to be an ItemPage!')
        
        try:
            country = location_item_page.claims['P17']
            if country:
                return ParseItemPage.complete_claim_details('P17', country,
                                                            languages=languages,
                                                            literals=['labels'])
            else:
                raise ValueError('No country found for this location!')
        except KeyError:
            raise ValueError('No country found for this location!')
    
    @classmethod
    def get_country_from_any(cls, itempage, local_attributes, languages):
        """
        Try to
        :param itempage: parent item
        :param local_attributes: attributes which might be used to infer country
        :param languages: languages for country label
        :returns dictionary with id, labels of country (or None):
        """
        itempage.get()
        country_prop_url = "https://www.wikidata.org/wiki/Property:P17"
        
        for location_type in local_attributes:
            if location_type in itempage.claims:
                for location in itempage.claims[location_type]:
                    if location:
                        try:
                            country = \
                                ParseItemPage.get_country_from_location(
                                    location.target,
                                    languages=languages
                                )
                            if len(country) == 1:
                                return country
                            elif 'preferred' in country:
                                return {"url": country_prop_url,
                                        'values': [country['preferred']]}
                            else:
                                pass
                        except ValueError:
                            pass
                    else:
                        warnings.warn('Entity {} has location property {} '
                                      'set to null'.format(itempage.id,
                                                           location_type))
        raise ValueError


class ParseClaim:
    """Parse an individual claim and its qualifiers"""
    
    def __init__(self, claim, languages, literals, delay=False):
        """
        Parse additional information about a specified claim. The result
        (dict format) is accessible through ParseClaim(claim).claim_details

        :param claim: pywikibot.Claim object to be parsed
        :type claim: pywikibot.Claim
        :param languages: list of language ISO codes
        :type languages: List(str)
        :param literals: list of literal properties to be included in result
        :type literals: List(str)
        """
        self.claim = claim
        self.languages = languages
        self.literals = literals
        if delay:
            self.claim_details = {}
        else:
            self.claim_details = self.parse_claim()
    
    def parse_claim(self):
        """Identify literal attributes and temporal attributes,
        perform default operations on remaining qualifiers. of the claim.

        :return: dictionary of claim attributes/qualifiers and their values."""
        claim_details = {}
        if isinstance(self.claim.target, basestring):
            
            claim_details['value'] = self.claim.target
            return claim_details
        elif isinstance(self.claim.target, WbTime):
            try:
                claim_details['value'] = self.claim.target.toTimestr(
                    force_iso=True)
            except AttributeError:
                pass
            return claim_details
        else:
            claim_details = self.extract_literal_claim()
        claim_details['url'] = 'https://www.wikidata.org/wiki/' + \
                               self.claim.target.id
        dates = self.get_claim_dates()
        if dates:
            claim_details['temporal_attributes'] = dates
        
        if self.claim.has_qualifier:
            for qualifier in OTHER_QUALIFIERS:
                if qualifier in self.claim.qualifiers:
                    try:
                        qualifier_targets = [
                            'https://www.wikidata.org/wiki/' + valid_for.target.id
                            for valid_for in self.claim.qualifiers[qualifier]]
                        
                        claim_details[qualifier] = qualifier_targets
                    except (KeyError, AttributeError):
                        warnings.warn(
                            'qualifier not found: {}.'.format(
                                OTHER_QUALIFIERS[qualifier]))
        return claim_details
    
    def extract_literal_claim(self):
        """Literals parsed by `ParseEntity.extract_literal_properties()"""
        target = self.claim.target
        claim_details = ParseItemPage.extract_literal_properties(target,
                                                                 self.languages,
                                                                 self.literals)
        return claim_details
    
    def get_claim_dates(self):
        """Check if the qualifiers include start time, end time or point in time
        attributes. If present, send it to self.claim_temporal_attributes()"""
        
        temporal_attributes = {}
        for attribute in TEMPORAL_QUALIFIERS:
            try:
                temporal_attributes[TEMPORAL_QUALIFIERS[attribute]] = \
                    self.claim_temporal_attributes(attribute)
            except ValueError:
                pass
        return temporal_attributes
    
    def claim_temporal_attributes(self, temporal_attribute):
        """Parse an individual temporal attribute (start date, end date,...)"""
        
        if self.claim.has_qualifier and temporal_attribute in self.claim.qualifiers:
            try:
                claim_date = self.claim.qualifiers[temporal_attribute][-1]
                if not claim_date:
                    raise ValueError('No dates found.')
                
                normalized_date_string = claim_date.target.toTimestr(
                    force_iso=True)
                # pprint(normalized_date_string)
                # date = datetime.datetime.strptime(normalized_date_string,
                #                                   '%Y-%m-%dT%H:%M:%SZ')
                return normalized_date_string
            except TypeError:
                raise TypeError
        raise ValueError('No dates found.')


def start_date(instance):
    if 'temporal_attributes' not in instance or 'P580' not in instance[
        'temporal_attributes']:
        return None
    return instance['temporal_attributes']['P580']['string']


def end_date(instance):
    if 'temporal_attributes' not in instance or 'P582' not in instance[
        'temporal_attributes']:
        return None
    return instance['temporal_attributes']['P582']['string']


def guess_current_value(attribute_instances):
    """
    Guess the value still holding in a list-form attribute. Use with caution:
    For most use cases, ParseItemPage.attribute_preferred_value is better.

    :param attribute_instances: list of claim values as returned by ParseClaim
    :type attribute_instances: list
    :return: Single value for claim
    """
    if len(attribute_instances) == 1:
        return attribute_instances[0]
    else:
        try:
            instance_has_startdate = [instance for instance in
                                      attribute_instances if
                                      start_date(instance)]
            
            instance_has_enddate = [instance for instance in attribute_instances
                                    if
                                    end_date(instance)]
            try:
                assert instance_has_startdate or instance_has_enddate
            except AssertionError:
                raise ValueError(
                    'No instances of claim with start or end dates found!')
            begins_doesnt_end = [instance for instance in instance_has_startdate
                                 if
                                 not end_date(instance)]
            if len(begins_doesnt_end) == 1:
                print(
                    'found exactly one instance with start date but no end '
                    'date, assumming thisto be current')
                most_recent_instance = begins_doesnt_end[0]
                return most_recent_instance
            
            most_recent_startdate = max(
                map(start_date, instance_has_startdate))
            
            most_recent_instances = filter(
                lambda i: start_date(i) == most_recent_startdate,
                instance_has_startdate)
            if len(most_recent_startdate) > 1:
                raise ValueError('Several equally recent start dates found.')
            else:
                return most_recent_instances[0]
        except Exception as e:
            raise ValueError(
                'Unable to determine most recent instance of attribute!' +
                '\nError message was: {}'.format(e))
