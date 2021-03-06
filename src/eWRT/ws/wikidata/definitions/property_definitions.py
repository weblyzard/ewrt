#!/usr/bin/python
# -*- coding: utf-8 -*-
# provides mappings property key-> English label
# for properties typically associated with
# a variety of entity types

import copy
from collections import OrderedDict, namedtuple

local_attributes = OrderedDict([
    ("P17", u"country"),
    ("P131", u"located in the administrative territorial entity"),
    ("P19", u"place of birth"),
    ("P27", u"country of citizenship"),
    ("P551", u"residence"),
    ("P159", u"headquarters location"),
    ("P740", u"location of formation"),
])

image_attributes = {
    "P18": u"image",
    "P41": u"flag image",
    "P94": u"coat of arms image",
    "P242": u"locator map image",
    "P1442": u"image of grave",
    "P154": u"logo image", }

location_properties = {
    "P18": u"image",
    "P31": u"instance of",
    "P41": u"flag image",
    "P47": u"shares border with",
    "P17": u"country",
    "P94": u"coat of arms image",
    "P131": u"located in the administrative territorial entity",
    "P190": u"twinned administrative body",
    "P227": u"GND ID",
    "P150": u"contains administrative territorial entity",
    "P242": u"locator map image",
    "P571": u"inception",
    "P473": u"local dialing code",
    "P268": u"BnF ID",
    "P910": u"topic's main category",
    "P625": u"coordinate location",
    "P935": u"Commons gallery",
    "P421": u"located in time zone",
    "P948": u"page banner",
    "P281": u"postal code",
    "P1465": u"category for people who died here",
    "P1566": u"GeoNames ID",
    "P1740": u"category for films shot at this location",
    "P1792": u"category of associated people",
    "P982": u"MusicBrainz area ID",
    "P1082": u"population",
    "P4290": u"official app",
    "P1464": u"category for people born here",
    "P2044": u"elevation above sea level",
    "P2046": u"area",
    "P6": u"head of government",
    "P30": u"continent",
    "P35": u"head of state",
    "P36": u"capital",
    "P37": u"official language",
    "P38": u"currency",
    "P78": u"top-level Internet domain",
    "P85": u"anthem",
    "P138": u"named after",
    "P163": u"flag",
    "P122": u"basic form of government",
    "P237": u"coat of arms",
    "P194": u"legislative body",
    "P209": u"highest judicial authority",
    "P297": u"ISO 3166-1 alpha-2 code",
    "P298": u"ISO 3166-1 alpha-3 code",
    "P443": u"pronunciation audio",
    "P463": u"member of",
    "P474": u"country calling code",
    "P530": u"diplomatic relation",
    "P299": u"ISO 3166-1 numeric code",
    "P610": u"highest point",
    "P984": u"IOC country code",
    "P901": u"FIPS 10-4 (countries and regions)",
    "P402": u"OSM relation ID",
    "P856": u"official website",
    "P1081": u"Human Development Index",
    "P832": u"public holiday",
    "P1125": u"Gini coefficient",
    "P1334": u"coordinates of easternmost point",
    "P1335": u"coordinates of westernmost point",
    "P2852": u"emergency phone number",
    "P2853": u"electrical plug type",
    "P2936": u"language used",
    "P1332": u"coordinates of northernmost point",
    "P1333": u"coordinates of southernmost point",
    "P3221": u"NYT topic ID",
    "P1589": u"deepest point",
    "P1622": u"driving side",
    "P2979": u"maritime identification digits",
    "P2988": u"GOST 7.67 cyrillic",
    "P3024": u"ITU letter code",
    "P3067": u"GS1 country code",
    "P3106": u"Guardian topic ID",
    "P1689": u"central government debt as a percent of GDP",
    "P1791": u"category of people buried here",
}

person_properties = {
    "P18": u"image",
    "P19": u"place of birth",
    "P21": u"sex or gender",
    "P20": u"place of death",
    "PP1411": u"nominated for",
    "P22": u"father",
    "P31": u"instance of",
    "P27": u"country of citizenship",
    "P25": u"mother",
    "P26": u"spouse",
    "P39": u"position held",
    "P40": u"child",
    "P53": u"family",
    "P102": u"member of political party",
    "P103": u"native language",
    "P106": u"occupation",
    "P108": u"employer",
    "P119": u"place of burial",
    "P172": u"ethnic group",
    "P496": u"ORCID iD",
    "P214": u"VIAF ID",
    "P451": u"partner",
    "P735": u"given name",
    "P734": u"family name",
    "P140": u"religion",
    "P497": u"CBDB ID",
    "P509": u"cause of death",
    "P746": u"date of disappearance",
    "P937": u"work location",
    "P1038": u"relative",
    "P1050": u"medical condition",
    "P569": u"date of birth",
    "P1442": u"image of grave",
    "P1532": u"country for sport",
    "P1559": u"name in native language",
    "P1254": u"Slovenska biografija ID",
    "P1317": u"floruit",
    "P1412": u"languages spoken, written or signed",
    "P570": u"date of death",
    "P1196": u"manner of death",
    "P1477": u"birth name",
    "P1636": u"date of baptism in early childhood",
    "P586": u"IPNI author ID",
    "P640": u"Léonore ID",
    "P2048": u"height",
    "P2067": u"mass",
    "P1853": u"blood type",
    "P2021": u"Erdős number",
    "P2456": u"DBLP ID",
    "P2605": u"ČSFD person ID",
    "P2889": u"FamilySearch person ID",
    "P3373": u"sibling",
    "P463": u"member of",
    "P166": u"award received",
    "P69": u"educated at",
    "P551": u"residence",
    "P2218": u"net worth estimate"
}

organization_properties = {
    "P154": u"logo image",
    "P166": u"award received",
    "P112": u"founder",
    "P17": u"country",
    "P159": u"headquarters location",
    "P527": u"has part",
    "P463": u"member of",
    "P571": u"inception",
    "P199": u"business division",
    "P37": u"official language",
    "P213": u"ISNI",
    "PP1411": u"nominated for",
    "P169": u"chief executive officer",
    "P740": u"location of formation",
    "P355": u"subsidiary",
    "P1056": u"product or material produced",
    "P1128": u"employees",
    "P1278": u"Legal Entity ID",
    "P1297": u"IRS Employer Identification Number",
    "P1320": u"OpenCorporates ID",
    "P749": u"parent organization",
    "P807": u"separated from",
    "P1454": u"legal form",
    "P1546": u"motto",
    "P1616": u"SIREN number",
    "P452": u"industry",
    "P1662": u"DOI prefix",
    "P1705": u"native label",
    "P856": u"official website",
    "P1789": u"chief operating officer",
    "P1830": u"owner of",
    "P1961": u"CTHS society ID",
    "P2088": u"Crunchbase organisation ID",
    "P2189": u"BiblioNet publisher ID",
    "P2740": u"ResearchGate institute ID",
    "P2813": u"mouthpiece",
    "P2828": u"corporate officer",
    "P3163": u"Scottish Charity number",
    "P3215": u"FR SIRET number",
    "P3220": u"KvK company ID",
    "P3273": u"Actorenregister ID",
    "P3393": u"LittleSis organisation ID",
    "P2388": u"office held by head of the organisation",
    "P2391": u"OKPO ID",
    "P2541": u"operating area",
    "P2657": u"EU transparency register ID",
    "P3500": u"Ringgold ID",
    "P3534": u"Australian Government Organisations Register ID",
    "P3549": u"Australian Company Number",
    "P3642": u"ARCHON code",
    "P3797": u"autonomous system number",
    "P3914": u"GuideStar Israel organization ID",
    "P4090": u"Biodiversity Repository ID",
    "P4290": u"official app",
}


PropertyParseInstruction = namedtuple(
    typename='PropertyParseInstruction',
    field_names=['name', # str
                 'identifiers', # str
                 'is_optional', # bool
                 'language_specific' # int, one of (-1, 0, 1)
                 ],
)
PropertyParseInstruction.__new__.__defaults__ = ('', '', True, 0)
# PropertyParseInstructions.language_specific expects values:
#   - 0: not language specific, e. g. datetime, coordinates or official website
#   - 1: language specific literal
#   - -1: WikiData entity, as an abstract key not language specific but
#         can have language specific labels (to allow searching for the labels
#         too where that makes sense


# a subset of properties potentially present for all entity types
CORE_GENERIC_PROPERTIES = [
    PropertyParseInstruction(name='label',
                             identifiers='(rdfs:label|wdt:P2561)',
                             is_optional=False, language_specific=1),
    PropertyParseInstruction(name='altLabel',
                             identifiers='(skos:altLabel|wdt:P1449|wdt:P742)',
                             is_optional=True, language_specific=1),
    PropertyParseInstruction(name='description',
                             identifiers='schema:description',
                             is_optional=True,
                             language_specific=1),
    PropertyParseInstruction(name='type', identifiers='wdt:P31',
                             is_optional=True, language_specific=-1)
]

# a subset of properties relevant for events with human readable identifiers,
# some defined as mandatory here though they're not strictly mandatory in
# wikidata's model, e.g. an event without a start date cannot be used for
# constructing a timeline and will thus be discarded
CORE_PROPERTIES_EVENTS = [
    PropertyParseInstruction(name='startDate',
                             identifiers='(wdt:P580|wdt:P585|wdt:P619|wdt:P577)',
                             is_optional=False,
                             language_specific=0),
    PropertyParseInstruction(name='coord',
                             identifiers='wdt:P625',
                             is_optional=True,
                             language_specific=0),
    PropertyParseInstruction(name='location',
                             identifiers='(wdt:P276|wdt:P1427|wdt:P1444)',
                             is_optional=True,
                             language_specific=-1),
    PropertyParseInstruction(name='administrative',
                             identifiers='wdt:P131',
                             is_optional=True,
                             language_specific=-1),
    PropertyParseInstruction(name='country',
                             identifiers='wdt:P17',
                             is_optional=True,
                             language_specific=0),
    PropertyParseInstruction(name='endDate',
                             identifiers='wdt:P582',
                             is_optional=True,
                             language_specific=0),
    PropertyParseInstruction(name='hashtag',
                             identifiers='wdt:P2572',
                             is_optional=True,
                             language_specific=0),
    PropertyParseInstruction(name='website',
                             identifiers='wdt:P856',
                             is_optional=True,
                             language_specific=0),
    PropertyParseInstruction(name='organizer',
                             identifiers='(wdt:P664)',
                             is_optional=True,
                             language_specific=-1),
    PropertyParseInstruction(name='participatingTeam',
                             identifiers='wdt:P1923',
                             is_optional=True,
                             language_specific=-1),
    PropertyParseInstruction(name='participant',
                             identifiers='wdt:P710',
                             is_optional=True,
                             language_specific=-1),
    PropertyParseInstruction(name='winner',
                             identifiers='(wdt:P991|wdt:P13469|wdt:P1346)',
                             is_optional=True,
                             language_specific=-1),
    PropertyParseInstruction(name='speaker',
                             identifiers='wdt:P823',
                             is_optional=True,
                             language_specific=-1),
    PropertyParseInstruction(name='guestOfHonor',
                             identifiers='wdt:P967',
                             is_optional=True,
                             language_specific=0),
    PropertyParseInstruction(name='openedBy',
                             identifiers='wdt:P542',
                             is_optional=True,
                             language_specific=0),
    PropertyParseInstruction(name='partOf',
                             identifiers='wdt:P361',
                             is_optional=True,
                             language_specific=0),
    PropertyParseInstruction(name='follows',
                             identifiers='wdt:P155',
                             is_optional=True,
                             language_specific=-1),
    PropertyParseInstruction(name='followedBy',
                             identifiers='wdt:P156',
                             is_optional=True,
                             language_specific=-1),
    PropertyParseInstruction(name='sport',
                             identifiers='wdt:P641',
                             is_optional=True,
                             language_specific=-1)
]

# mapping from main entity type as human readable string to the respective
# relevant properties
ENTITY_TYPE_DEFINITIONS = {'person': person_properties,
                           'organization': organization_properties,
                           'geo': location_properties}

GENERIC_PROPERTIES = copy.copy(person_properties)
GENERIC_PROPERTIES.update(organization_properties)
GENERIC_PROPERTIES.update(location_properties)
