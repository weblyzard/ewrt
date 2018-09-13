import datetime
import warnings
from pprint import pprint

from eWRT.ws.wikidata.definitions import (person_properties,
                                          location_properties,
                                          organization_properties)
from eWRT.ws.wikidata.get_image_from_wikidataid import get_image, NoImageFoundError

RELEVANT_LANGUAGES = ['en']

ENTITY_TYPES = {'person': person_properties,
                'organization': organization_properties,
                'geo': location_properties}

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

    def __init__(self, itempage, include_literals=False, claims_of_interest=None,
                 entity_type_properties=None,
                 entity_type='person', languages=None):
        """
        :param itempage: pywikibot.ItemPage to be parsed
        :param include_literals: bool defining whether to include further literals
        (descriptions, aliases) in the output. If False, only labels are included.
        :param claims_of_interest: list of claims by their WikiData identifiers
        that shall be parsed, if present.
        :param entity_type_properties: dict of property identifiers and their labels
        :param entity_type: type of entity, determines the default for
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

        if languages is None:
            languages = RELEVANT_LANGUAGES
        self.languages = languages
        if not entity_type_properties:
            self.entity_type_properties = ENTITY_TYPES[entity_type]

        if claims_of_interest is None:
            claims_of_interest = self.CLAIMS_OF_INTEREST
        self.claims_of_interest = [prop for prop in claims_of_interest if prop != 'P18']

        if 'P18' in claims_of_interest:
            self._image_requested = True
        else:
            self._image_requested = False

        self.item_raw = itempage
        self.process_attributes()
        if not self.include_literals:
            self.details = {key: self.details[key] for key in self.details if
                            self.details[key] and key not in self.LITERAL_PROPERTIES}

    def process_attributes(self):
        """Exctract information about the item, specified
        by the predicates in self.claims_of_interest:
          - extract literal attributes
          - find image link(s) (if requested)
          - make best effort attempt to parse
            the other claims_of_interest"""

        # get the ent
        self.details = self.extract_literal_properties(self.item_raw, self.languages,
                                                       self.literals)
        if self._image_requested:
            try:
                (self.details['image_description'],
                 _,
                 self.details['full_image']) = get_image(itempage=self.item_raw)
            except NoImageFoundError:
                pass
        # else:
        #     print('skipping image search')
        self.process_other_claims()

    def process_other_claims(self):
        """Generic best effort method to parse additional predicates
        and their qualifiers."""
        for claim in self.claims_of_interest:

            try:
                values = []
                claim_name = self.entity_type_properties[claim]
                self.details[claim_name] = {'values': values}
                claim_instances = self.item_raw.claims[claim]
                for sub_claim in self.item_raw.claims[claim]:
                    try:
                        value = ParseClaim(sub_claim, self.languages, self.literals).claim_details
                        if value:
                            values.append(value)
                    except Exception as e:
                        pass

                if len(claim_instances) > 1:
                    preferred = self.attribute_preferred_values(claim_instances)
                    if len(preferred) == 1:
                        self.details[claim_name]['preferred'] = preferred[0]
                elif len(claim_instances) == 0:
                    del self.details[claim_name]

            except KeyError:
                pass
                # warnings.warn(
                #    'claim {} not available for entity {}'.format(claim, self.details['labels']))

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
                    literal_properties[prop][language] = entity.text[prop][language]
                except KeyError:
                    pass
        return literal_properties

    @classmethod
    def attribute_preferred_values(self, claim_instances):
        def gettargets(claim):
            return [claim.target for claim in claim_instances]

        if len(claim_instances) == 1:
            return gettargets(claim_instances)
        else:
            preferred = [claim for claim in claim_instances if claim.rank == 'preferred']
            if len(preferred) == 1:
                pass
            elif len(preferred):
                warnings.warn('No claim instance marked as preferred!')
            else:
                warnings.warn(
                    'Incorrectly tagged data: several instances '
                    'marked as preferred, this should not happen!')
            return [claim.target for claim in preferred]


class ParseClaim:
    """Parse an individual claim and its qualifiers"""

    def __init__(self, claim, languages, literals):
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
        self.claim.get()
        self.languages = languages
        self.literals = literals
        self.claim_details = self.parse_claim()

    def parse_claim(self):
        """Identify literal attributes and temporal attributes,
        perform default operations on remaining qualifiers. of the claim.

        :return: dictionary of claim attributes/qualifiers and their values."""
        claim_details = self.extract_literal_claim()
        if isinstance(self.claim.target, basestring):
            claim_details['value'] = self.claim.target
        dates = self.get_claim_dates()
        if dates:
            claim_details['temporal_attributes'] = dates

        if self.claim.has_qualifier:
            for qualifier in OTHER_QUALIFIERS:
                if qualifier in self.claim.qualifiers:
                    try:
                        qualifier_targets = ['https://www.wikidata.org/wiki/' + valid_for.target.id
                                             for valid_for in self.claim.qualifiers[qualifier]]

                        claim_details[qualifier] = qualifier_targets
                    except (KeyError, AttributeError):
                        warnings.warn(
                            'qualifier not found: {}.'.format(OTHER_QUALIFIERS[qualifier]))
        return claim_details

    def extract_literal_claim(self):
        """Literals parsed by `ParseEntity.extract_literal_properties()"""
        target = self.claim.target
        claim_details = ParseItemPage.extract_literal_properties(target, self.languages,
                                                                 self.literals)
        claim_details['url'] = 'https://www.wikidata.org/wiki/' + self.claim.target.id
        return claim_details

    def get_claim_dates(self):
        """Check if the qualifiers include start time, end time or point in time
        attributes. If present, send it to self.claim_temporal_attributes()"""

        temporal_attributes = {}
        for attribute in TEMPORAL_QUALIFIERS:
            try:
                temporal_attributes[attribute] = self.claim_temporal_attributes(attribute)
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

                if int(claim_date.target.year) > 0:
                    json = claim_date.toJSON()
                    wb_time_string = wb_time_string = json['datavalue']['value']['time']

                    normalized_date_string = wb_time_string[8:]
                    if wb_time_string.startswith('-'):
                        normalized_date_string = '-' + normalized_date_string
                    pprint(normalized_date_string)
                else:
                    print('year is')
                    print(claim_date.target.year)
                date = datetime.datetime.strptime(normalized_date_string,
                                                  '%Y-%m-%dT%H:%M:%SZ')
                return date
            except TypeError:
                raise TypeError
        raise ValueError('No dates found.')


def start_date(instance):
    if 'temporal_attributes' not in instance or 'P580' not in instance[
        'temporal_attributes']:
        return None
    return (instance['temporal_attributes']['P580']['string'])


def end_date(instance):
    if 'temporal_attributes' not in instance or 'P582' not in instance[
        'temporal_attributes']:
        return None
    return (instance['temporal_attributes']['P582']['string'])


def guess_current_value(attribute_instances):
    """
    Guess the value still holding in a list-form attribute. Use with caution:
    For most use cases, ParseItemPage.attribute_preferred_values is better.

    :param attribute_instances: list of claim values as returned by ParseClaim
    :type attribute_instances: list
    :return: Single value for claim
    """
    if len(attribute_instances) == 1:
        return attribute_instances[0]
    else:
        try:
            instance_has_startdate = [instance for instance in attribute_instances if
                                      start_date(instance)]

            instance_has_enddate = [instance for instance in attribute_instances if
                                    end_date(instance)]
            try:
                assert instance_has_startdate or instance_has_enddate
            except AssertionError:
                raise ValueError('No instances of claim with start or end dates found!')
            begins_doesnt_end = [instance for instance in instance_has_startdate if
                                 not end_date(instance)]
            if len(begins_doesnt_end) == 1:
                print('found exactly one instance with start date but no end date, assumming this'
                      'to be current')
                most_recent_instance = begins_doesnt_end[0]
                return most_recent_instance

            most_recent_startdate = max(map(start_date, instance_has_startdate))

            most_recent_instances = filter(
                map(lambda i: start_date(i) == most_recent_startdate, instance_has_startdate))
            if len(most_recent_startdate) > 1:
                raise ValueError('Several equally recent start dates found.')
            else:
                return most_recent_instances[0]
        except Exception as e:
            raise ValueError(
                'Unable to determine most recent instance of attribute{}'.format(instance['url']) +
                '\nError message was: {}'.format(e))
