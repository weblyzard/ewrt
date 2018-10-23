#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on September 12, 2018

@author: Jakob Steixner, <jakob.steixner@modul.ac.at

Retrieve Wikidata's main image based on (exact) Wikipedia
article title in a specific language. Also allows to retrieve other
types of images (e.g. flags, coats of arms, etc.) where given.

CLI usage to get thumbnail link from WikiData ID: <path-to-script> <ID> [size]

'''

import hashlib
import sys
import warnings

import pywikibot

from collections import OrderedDict

from eWRT.ws.wikidata.definitions import image_attributes

if sys.version_info.major == 3:
    from urllib.parse import quote
else:
    from urllib2 import quote

DEFAULT_THUMBNAIL_WIDTH = 128


class NoImageFoundError(ValueError):
    pass


def get_images(itempage,
               image_width=DEFAULT_THUMBNAIL_WIDTH,
               image_types=image_attributes):
    """Find images of any specified type (e .g. 'image', 'flag'...).
    :param itempage: pywikibot.ItemPage
    :param image_width: width of the thumbnail
    :param image_types: dict of image-type properties identified
        by their Pxxx codes, such as `P18`: 'image', `P154`: 'logo image'
    :returns dict with keys=Pxx codes, values=list of [image_description_url,
        thumbnail_url, full_image_url]
    """
    try:
        claims = itempage['claims']
    except TypeError:
        claims = itempage.claims
    images_retrieved = {}
    for image_type in image_types:
        try:
            image = claims[image_type][0]
        except KeyError:
            # if we are looking for a *list* of image types,
            # we don't want to abort the process because
            # one is missing.
            continue
        try:
            target = image.getTarget()
        except AttributeError:
            from pywikibot import Claim
            from pywikibot.site import DataSite
            image = Claim.fromJSON(DataSite('wikidata', 'wikidata'), image)
            target = image.getTarget()
        claim_id = image.snak
        # str(target) returns a string of format [[site:namespace:filename]],
        # e. g. [[commons:File:Barack_Obama.jpg]], the wiki link of the image
        # page. We substitute this for a valid external link
        site, ns, link = image_interwiki_link = str(
            target).replace(' ', '_').strip('[]').split(':')
        image_description_page = 'https://{}.wikimedia.org/wiki/{}:{}'.format(
            *image_interwiki_link)

        # after:
        # https://stackoverflow.com/questions/34393884/how-to-get-image-url-property-from-wikidata-item-by-api
        thumbnail_template = u'https://{}.wikimedia.org/w/thumb.php?width={}&f={}'
        thumbnail_link = thumbnail_template.format(site, image_width, link.decode('utf8'))
        image_md5 = hashlib.md5(link).hexdigest()
        a, b = image_md5[:2]
        direct_link_template = 'https://upload.wikimedia.org/wikipedia/{}/{}/{}/{}'
        image_direct_link = direct_link_template.format(site, a, a + b,
                                                        quote(link)
                                                        )

        images_retrieved[image_type] = OrderedDict(
            [('claim_id', claim_id),
             ('description_page', image_description_page),
             ('thumbnail', thumbnail_link),
             ('full', image_direct_link)])
    try:
        assert images_retrieved
    except AssertionError:
        raise NoImageFoundError("No image available for entity!")
    return images_retrieved


def get_image(itempage, image_width=DEFAULT_THUMBNAIL_WIDTH, image_type='P18',
              include_claim_id=False):
    """Get one image type (default is `image`='P18') only.
    :param itempage: ItemPage
    :param image_width: width in pixels (int)
    :param image_type: Wikidata code of image type, default is
            `P18`='image'. Can be e. g. flag image, coat of arms, logo,...
    :returns list of [image_description_url, thumbnail_url, full_image_url]"""
    try:
        image = get_images(itempage=itempage, image_width=image_width,
                          image_types=[image_type])[image_type]
        if not include_claim_id:
            del image['claim_id']
        return image

    except KeyError:
        raise NoImageFoundError


def get_thumbnail(itempage, *args, **kwargs):
    """Return thumbnail of single image type only. Arguments that can be
    passed on to `get_image` are image_width (int, default
    `DEFAULT_THUMBNAIL_WIDTH`) and `image_type` as a Wikidata property
    code.

    :returns image link (str)
    """
    return get_image(itempage, *args, **kwargs)[1]


if __name__ == '__main__':
    # return list of thumbnail urls
    try:
        ids = sys.argv[1].upper()
    except IndexError:
        raise ValueError(
            "Required argument: wikidata IDs of entity(ies), comma separated!")

    thumbnails = []
    for entity_wikidata_id in ids.split(','):
        wikidata_site = pywikibot.site.DataSite("wikidata", "wikidata")
        page = pywikibot.ItemPage(site=wikidata_site, title=entity_wikidata_id)

        try:
            width = sys.argv[2]
        except IndexError:
            warnings.warn(
                'No width specified, using default value of {}px!'.format(
                    DEFAULT_THUMBNAIL_WIDTH))
            width = DEFAULT_THUMBNAIL_WIDTH

        try:
            thumbnail = get_thumbnail(page, width)
            thumbnails.append(thumbnail)
        except NoImageFoundError:
            warnings.warn("No image available for entity!")

    print(thumbnails)
