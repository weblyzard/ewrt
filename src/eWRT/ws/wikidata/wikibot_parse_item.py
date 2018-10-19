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

from pywikibot import WbTime, Claim, Coordinate, WbQuantity
from pywikibot.site import DataSite

from eWRT.ws.wikidata.definitions import (local_attributes as LOCAL_ATTRIBUTES,
                                          image_attributes,
                                          GENERIC_PROPERTIES)
from eWRT.ws.wikidata.get_image_from_wikidataid import get_image, \
    NoImageFoundError
from eWRT.ws.wikidata.preferred_claim_value import attribute_preferred_value


if sys.version_info.major == 3:
    basestring = (bytes, str)

RELEVANT_LANGUAGES = ['en']

QUALIFIERS = {'P580': 'start date',
              'P582': 'end date',
              'P585': 'point in time',
              'P642': 'at_organization',
              'P854': 'reference_url',
              'P1686': 'for_work'}

QUALIFIERS = {}

CLAIMS_OF_INTEREST = ["P18", "P19", 'P39', 'P106', 'P108', 'P102']


def get_wikidata_timestamp(item_page):
    """

    :param item_page:
    :return:
    """
    # ItemPages come in two slightly different formats depending on how
    # they were created (probably a bug in pywikibot). We want to be able to
    # deal with both:
    try:
        timestamp = item_page['timestamp']
    except (TypeError, KeyError):
        try:
            timestamp = item_page.timestamp
        except AttributeError:
            timestamp = item_page.latest_revision.timestamp.isoformat()
        except KeyError:
            return None
    return timestamp

class ParseItemPage:
    """Methods to parse pywikibot.ItemPage for a specifiable list
        of properties, returning a dict of property labels and values."""
    LITERAL_PROPERTIES = ['labels', 'aliases', 'descriptions']
    attribute_preferred_value = attribute_preferred_value

    def __init__(self, itempage, include_literals=False,
                 claims_of_interest=None,
                 entity_type_properties=None, languages=None,
                 require_country=True,
                 include_attribute_labels=True,
                 qualifiers_of_interest=None,
                 filter=None):
        """
        :param itempage: pywikibot.ItemPage to be parsed
        :param include_literals: bool defining whether to includehttps://gitlab.semanticlab.net/nlp-backend/issues0
            further literals (descriptions, aliases) in the output. If
            False, only labels are included.
        :param claims_of_interest: list of claims by their WikiData identifiers
        that shall be parsed, if present.
        :param entity_type_properties: dict of property identifiers and
            their labels entity_type_properties.
        :param languages: list of languages of interest in their preferred order
        :param require_country: whether to try and deduce country from other
            location attributes ('location', 'place of birth', 'headquarters
            location'...).
        :param include_attribute_labels: Include the labels of attribute values
            e. g. the names of locations, or just their wikidata ID. Set to False
            for offline extraction from JSON/testing.
        """

        # include 'labels' only if include_literals == False
        # itempage.get()
        self.item_raw = itempage
        try:
            self.claims = itempage['claims']
        except AttributeError:
            self.claims = itempage['claims']
        if filter and not self.filter(filter):
            raise ValueError
        if not isinstance(itempage, dict):
            id = itempage.id
            timestamp = itempage.timestamp
            itempage = itempage.text
            itempage.update({'id': id, 'timestamp': timestamp})

        timestamp = get_wikidata_timestamp(itempage)
        if qualifiers_of_interest is None:
            self.qualifiers_of_interest = QUALIFIERS
        self.include_attribute_labels = include_attribute_labels
        self.include_literals = include_literals
        if self.include_literals:
            self.literals = self.LITERAL_PROPERTIES
        else:
            self.literals = ['labels']
        self._require_country = require_country
        if languages is None: \
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
        self.process_attributes()

        assert self.details
        self.details['wikidata_timestamp'] = timestamp
        self.details['wikidata_id'] = itempage['id']

    def filter(self, filter_params):
        """
        reject results that do not match a filter.
        Filters can require the presence of an attribute or require that it
        must be above/below a certain value.
        example: filter for individuals with a stated birth place and a birth
        date in the year 1950
        >>> params = [('P19', 'has_attr', None), ('P569', 'min', '+1950-01-01'), ('P569', 'max', '+1950-12-31')]
        >>> ParseItemPage(itempage, filter_params=params)
        (this will raise a ValueError for individuals not matching the criteria)
        :param filter_params:
        :return:
        """
        min_max = {'min': max, 'max': min}
        def inside(threshold, testee, mode):
            if mode == 'min':
                return testee >= threshold
            elif mode == 'max':
                return testee <= threshold

        def inside_both(testee, min=None, max=None):
            if min and not inside(min, testee, 'min'):
                return False
            if max and not inside(max, testee, 'max'):
                return False
            return True

        for claim, mode, threshold_value in filter_params:
            if not claim in self.claims:
                return False

        for claim in set([item[0] for item in filter_params]):

            filter_claims = {param[1]: param[2] for param in filter_params if param[0] == claim}
            if not any(filter_claims.values()):
                continue
            values = self.complete_claim_details(claim,
                                                 self.claims[claim],
                                                 languages=[],
                                                 literals=[],
                                                 include_attribute_labels=False,
                                                 )
            thresholds = {param: filter_claims[param] for param in ['min', 'max'] if param in filter_claims}
            if not any([inside_both(instance['value'], **thresholds) for instance in values['values'] if instance['value'] is not None]):
                return False
            
        return True

        
        
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
                self.details[type_literal] = {'url': image_type, 'values': [get_image(
                    itempage=self.item_raw,
                    image_type=image_type,
                include_claim_id=True)]}
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
                claim_instances = self.claims[claim]
                if claim_instances:
                    self.details[claim_name] = self.complete_claim_details(
                        claim, claim_instances,
                        languages=self.languages,
                        literals=self.literals,
                        include_attribute_labels=self.include_attribute_labels,
                        qualifiers=self.qualifiers_of_interest)
                    if self.details[claim_name]:
                        self.details[claim_name]['url'] = \
                            'https://www.wikidata.org/wiki/Property:' + claim
                    else:
                        warnings.warn(
                            'Unable to parse claim {claim} for item {item}, '
                            'should be present!'.format(claim=claim,
                                                        item=self.item_raw[
                                                            'id']))

            except KeyError as e:
                pass

            # warnings.warn(
            #    'claim {} not available for entity {}'.format(claim, self.details['labels']))
        if ('country' not in self.details or not self.details['country']) and \
                self._require_country:
            country_info = self.get_country_from_any(self.item_raw,
                                                     local_attributes=LOCAL_ATTRIBUTES,
                                                     languages=self.languages,
                                                     include_attribute_labels=self.include_attribute_labels)
            if country_info:
                try:
                    country_info[0]['claim_id'] = self.item_raw['id'] + '@' + \
                                                  country_info[0]['claim_id']
                except KeyError:
                    print(country_info)
                self.details['country'] = {'values': country_info,
                                           'url': 'https://www.wikidata.org/wiki/Property:P17'
                                           }

        for attribute in [a for a in self.details]:

            if not self.details[attribute] or 'values' in self.details[
                attribute] and not self.details[attribute]['values']:
                del self.details[attribute]

    @classmethod
    def complete_claim_details(cls, claim_id, claim_instances, languages,
                               literals, include_attribute_labels=True,
                               qualifiers=None):
        """Find values for specified claim types for which no specific
        handling is defined.
        :param claim_id: Pxx id of the attribute.
        :param claim_instances: list of propositions (pywikibot.Claim instances).
        :param languages: list of languages
        :param literals: list of literal properties to include
        :returns dictionary with claim id, values"""
        values = []
        if include_attribute_labels is False:
            literals = []
        assert claim_instances
        for sub_claim in claim_instances:
            try:
                value = ParseClaim(sub_claim, languages,
                                   literals,
                                   include_attribute_labels=include_attribute_labels,
                                   qualifiers=qualifiers).claim_details
                if value:
                    values.append(value)
            except ValueError as e:
                pass
        if values:
            wd_prop_url = 'https://www.wikidata.org/wiki/Property:'
            claim_details = {'values': values,
                             'url': wd_prop_url + claim_id}
        else:
            claim_details = {}
        if len(claim_instances) > 1:
            try:
                marked_preferred = attribute_preferred_value(
                    claim_instances)
                if len(marked_preferred) == 1:
                    preferred = marked_preferred[0]
                    claim_details['preferred'] = [instance for instance in
                                                  claim_details['values'] if
                                                  instance['claim_id'] ==
                                                  preferred.snak]

            except ValueError as e:
                # try:
                #     most_recent = guess_current_value([Claim.fromJSON(site=DataSite('wikidata', 'wikidata'),
                #                    data=claim) for claim in claim_instances])
                #     claim_details['preferred'] = [instance for instance in
                #                                   claim_details['values'] if
                #                                   instance['claim_id'] ==
                #                                   most_recent.snak]
                # except Exception as e:

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
        try:
            entity = entity.text
        except AttributeError:
            pass
        literal_properties = {prop: {} for prop in literals}
        for prop in literal_properties:
            for language in languages:
                try:
                    literal_properties[prop][language] = \
                        entity[prop][language]
                    if isinstance(literal_properties[prop][language], dict):
                        literal_properties[prop][language] = \
                            literal_properties[prop][language]['value']
                    elif isinstance(literal_properties[prop][language], list):
                        try:
                            literal_properties[prop][language] = [entry['value']
                                                                  for entry in
                                                                  literal_properties[
                                                                      prop][
                                                                      language]]
                        except TypeError:
                            pass
                except (KeyError, AttributeError, TypeError):
                    pass
        return literal_properties

    @classmethod
    def get_country_from_location(cls, location_item_page, languages,
                                  include_attribute_labels=True):
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
                country_identified = ParseItemPage.complete_claim_details(
                    'P17',
                    country,
                    languages=languages,
                    literals=['labels'],
                    include_attribute_labels=include_attribute_labels,
                    qualifiers=[])
                # country_iso_code = COUNTRY_ISO2_CODES_DICT[country_identified[0]['url']]
                return country_identified
            else:
                raise ValueError('No country found for this location!')
        except KeyError:
            raise ValueError('No country found for this location!')

    @classmethod
    def get_country_from_any(cls, itempage, local_attributes, languages,
                             include_attribute_labels=True):
        """
        Try to
        :param itempage: parent item
        :param local_attributes: attributes which might be used to infer country
        :param languages: languages for country label
        :returns list with dictionaries ofID, labels of (preferred) country or
        countries.
        :raises ValueError if no country can be reconstrued.
        """
        if local_attributes is None:
            local_attributes = LOCAL_ATTRIBUTES
        try:
            claims = itempage['claims']
        except:
            claims = itempage.text['claims']
        for location_type in local_attributes:
            if location_type in claims:
                for location in claims[location_type]:
                    if location:
                        if not isinstance(location, Claim):
                            location = Claim.fromJSON(
                                DataSite('wikidata', 'wikidata'), data=location)
                        try:
                            country = \
                                ParseItemPage.get_country_from_location(
                                    location.target,
                                    languages=languages,
                                    include_attribute_labels=include_attribute_labels
                                )
                            if 'preferred' in country:
                                return country['preferred']
                            elif len(country['values']) >= 1:
                                return country['values']
                            else:
                                pass
                        except ValueError:
                            pass
                    else:
                        warnings.warn('Entity {} has location property {} '
                                      'set to null'.format(itempage['id'],
                                                           location_type))
        raise ValueError


class ParseClaim:
    """Parse an individual claim and its qualifiers"""

    def __init__(self, claim, languages, literals, delay=False,
                 include_attribute_labels=True, qualifiers=None):
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
        if qualifiers is None:
            qualifiers = QUALIFIERS
        self.qualifiers = qualifiers
        if not isinstance(claim, Claim):
            claim = Claim.fromJSON(site=DataSite('wikidata', 'wikidata'),
                                   data=claim)

        self.include_attribute_labels = include_attribute_labels
        self.claim = claim
        self.languages = languages
        self.literals = literals
        if self.include_attribute_labels:
            self.literals = ['labels']
        if delay:
            self.claim_details = {}
        else:
            self.claim_details = self.parse_claim()

    def parse_claim(self):
        """Identify literal attributes and temporal attributes,
        perform default operations on remaining qualifiers. of the claim.

        :return: dictionary of claim attributes/qualifiers and their values."""
        claim_details = {}
        try:
            claim_details['claim_id'] = self.claim.snak
            if not claim_details['claim_id']:
                claim_details['claim_id'] = self.claim.hash
                if not claim_details['claim_id']:
                    warnings.warn('No claim id identified')
        except Exception as e:
            warnings.warn('No claim id identified!')
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
        elif isinstance(self.claim.target, Coordinate):
            claim_details[
                'values'] = self.claim.target.lat, self.claim.target.lon
        elif isinstance(self.claim.target, WbQuantity):
            claim_details['value'] = float(self.claim.target.amount)
        elif not self.claim.target is None:
            claim_details['url'] = 'https://www.wikidata.org/wiki/' + \
                                   self.claim.target.id
            if self.include_attribute_labels:
                claim_details.update(self.extract_literal_claim())
        else:
            warnings.warn('claim {} on item {} is None'.format(
                self.claim.id,
                claim_details['claim_id'].split('$')[0]
            ))
            return None
        # dates = self.get_claim_dates()
        # if dates:
        #     claim_details['temporal_attributes'] = dates
        # self.qualifiers.update(TEMPORAL_QUALIFIERS)
        if self.claim.has_qualifier and self.claim.qualifiers:
            for qualifier in self.qualifiers:
                if qualifier in self.claim.qualifiers:
                    try:
                        qualifier_targets = ParseItemPage.complete_claim_details(
                            claim_id=qualifier,
                            claim_instances=self.claim.qualifiers[qualifier],
                            languages=self.languages, literals=[],
                            include_attribute_labels=self.include_attribute_labels,
                            qualifiers={})

                        claim_details[self.qualifiers[qualifier]] = {
                            'url': qualifier,
                            'values': qualifier_targets}
                    except (KeyError, AttributeError):
                        warnings.warn(
                            'qualifier not found: {}.'.format(
                                self.qualifiers[qualifier]))
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
    try:
        if instance.has_qualifier or instance.qualifiers:
            if 'P580' in instance.qualifiers:

                if isinstance(instance.qualifiers['P580'][0].target, WbTime):
                    try:
                        start_date = instance.qualifiers['P580'][
                            0].target.toTimestr(
                            force_iso=True)
                        return start_date
                    except AttributeError:
                        pass

    except Exception as e:
        pass

    if 'temporal_attributes' not in instance or 'P580' not in \
            instance['temporal_attributes']:
        return None
    return instance['temporal_attributes']['P580']['string']


def end_date(instance):
    if 'temporal_attributes' not in instance or 'P582' not in \
            instance['temporal_attributes']:
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

            # instance_has_enddate = [instance for instance in attribute_instances
            #                         if
            #                         end_date(instance)]
            try:
                assert instance_has_startdate  # or instance_has_enddate
            except AssertionError:
                raise ValueError(
                    'No instances of claim with start or end dates found!')
            # begins_doesnt_end = [instance for instance in instance_has_startdate
            #                      if
            #                      not end_date(instance)]
            # if len(begins_doesnt_end) == 1:
            #     print(
            #         'found exactly one instance with start date but no end '
            #         'date, assumming thisto be current')
            #     most_recent_instance = begins_doesnt_end[0]
            #     return most_recent_instance

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
