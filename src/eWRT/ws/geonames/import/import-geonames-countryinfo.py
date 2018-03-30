#!/usr/bin/env python

from xml.dom.minidom import parse
from gzip import open

COUNTRY_INFO_FILE = "./data/countryInfo.xml.gz"
BLACKLIST = (6697173,  # Antarktika
            )

def getText( node ):
    rc = [ n.data for n in node.childNodes if n.nodeType == n.TEXT_NODE ] 
    return "".join(rc)

getNode= lambda e, x: e.getElementsByTagName(x)[0]
getNodeText = lambda e,x: getText( getNode(e,x) )

for country in parse( open(COUNTRY_INFO_FILE) ).getElementsByTagName("country"):
    if int(getNodeText(country, "geonameId")) in BLACKLIST:
        continue

    population = getNodeText(country, "population")
    if not population:
        population = "NULL"
    else:
        population = "'"+population+"'"

    area = getNodeText(country, "areaInSqKm")
    if not area:
        area = "NULL"
    else:
        area = "'"+area+"'"

    print("INSERT INTO countryinfo (id, area, population) VALUES ('%s', %s, %s);" \
      % (getNodeText(country, "geonameId"), area, population))

    
