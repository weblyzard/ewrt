#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on September 10, 2018

@author: Jakob Steixner, <jakob.steixner@modul.ac.at

Retrieve image based on
'''

import hashlib
import sys
import urllib2
import warnings

import pywikibot

from eWRT.ws.wikidata.definitions.property_definitions import image_attributes
DEFAULT_THUMBNAIL_WIDTH = 128


class NoImageFoundError(ValueError):
    pass


def get_images(raw_entity, image_width=DEFAULT_THUMBNAIL_WIDTH, image_types=image_attributes):
    """Find an image associated with the entity (if available).
    :param raw_entity: pywikibot.ItemPage
    :param image_width: width of the thumbnail
    """
    try:
        claims = raw_entity.claims
    except AttributeError:
        claims = raw_entity.text['claims']
    images_retrieved = []
    for image_type in image_types:
        try:
            image = claims[image_type][0]
        except KeyError:
            raise NoImageFoundError("No image available for entity!")
        target = image.getTarget()
        # str(target) returns a string of format [[site:namespace:filename]],
        # e. g. [[commons:File:Barack_Obama.jpg]], the wiki link of the image
        # page. We substitute this for a valid external link
        site, ns, link = image_interwiki_link = str(target).replace(' ', '_').strip('[]').split(':')
        image_description_page = 'https://{}.wikimedia.org/wiki/{}:{}'.format(*image_interwiki_link)

        # after:
        # https://stackoverflow.com/questions/34393884/how-to-get-image-url-property-from-wikidata-item-by-api
        thumbnail_link = 'https://{}.wikimedia.org/w/thumb.php?width={}&f={}'.format(site, image_width,
                                                                                     link)
        image_md5 = hashlib.md5(link).hexdigest()
        a, b = image_md5[:2]
        image_direct_link = 'https://upload.wikimedia.org/wikipedia/{}/{}/{}/{}'.format(
            site, a, a + b, urllib2.quote(link)
        )
        images_retrieved.append([image_description_page, thumbnail_link, image_direct_link])
    return images_retrieved

def get_image(raw_entity, image_width=DEFAULT_THUMBNAIL_WIDTH):
    """Get the `image`='P18' only.
    :param raw_entity: ItemPage
    :param image_width: width in pixels (int)"""
    return get_images(raw_entity=raw_entity, image_width=width, image_types=['P18'])[0]

def get_thumbnail(*args, **kwargs):
    """Return thumbnail only."""
    return get_image(*args, **kwargs)[1]


if __name__ == '__main__':
    # return list of thumbnail urls
    try:
        ids = sys.argv[1].upper()
    except IndexError:
        raise ValueError("Required argument: wikidata IDs of entity(ies), comma separated!")

    thumbnails = []
    for entity_wikidata_id in ids.split(','):
        wikidata_site = pywikibot.Site("wikidata", "wikidata")
        page = pywikibot.ItemPage(site=wikidata_site, title=entity_wikidata_id)

        try:
            width = sys.argv[2]
        except IndexError:
            warnings.warn(
                'No width specified, using default value of {}px!'.format(DEFAULT_THUMBNAIL_WIDTH))
            width = DEFAULT_THUMBNAIL_WIDTH

        try:
            thumbnail = get_thumbnail(page, width)
            thumbnails.append(thumbnail)
        except NoImageFoundError:
            warnings.warn("No image available for entity!")

    print(thumbnails)

