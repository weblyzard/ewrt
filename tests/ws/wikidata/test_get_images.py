#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on September 20, 2018

@author: jakob <jakob.steixner@modul.ac.at>
'''
import mock
import pytest
from eWRT.ws.wikidata.definitions.property_definitions import image_attributes
from eWRT.ws.wikidata.get_image_from_wikidataid import get_images, get_image
from pywikibot import Claim

DataSite, itempage = mock.Mock(), mock.Mock()

itempage.claims = {
    'P1442': [Claim.fromJSON(DataSite("wikidata", "wikidata"), {
        u'type': u'statement',
        u'mainsnak': {
            u'datatype': u'commonsMedia',
            u'datavalue': {u'type': u'string',
                           u'value': u"Douglas Adams' gravestone.jpg"},
            u'property': u'P1442',
            u'snaktype': u'value'},
        u'id': u'Q42$db1ba2ba-47b9-3650-e6c4-db683abf788c',
        u'rank': u'normal'
    })
              ],
    'P18': [Claim.fromJSON(DataSite("wikidata", "wikidata"), {
        u'mainsnak': {
            u'datatype': u'commonsMedia',
            u'datavalue': {
                u'type': u'string',
                u'value': u'Douglas adams portrait cropped.jpg'},
            u'property': u'P18', u'snaktype': u'value'},
        u'rank': u'normal', u'qualifiers': {u'P2096': [
            {u'datatype': u'monolingualtext',
             u'datavalue': {
                 u'type': u'monolingualtext',
                 u'value': {
                     u'text': u'Portr\xe6t af Douglas Adams',
                     u'language': u'da'}},
             u'property': u'P2096',
             u'hash': u'8406a17fdbde124e88aef130bef59ce9178d1e75',
             u'snaktype': u'value'},
            {u'datatype': u'monolingualtext',
             u'datavalue': {
                 u'type': u'monolingualtext',
                 u'value': {
                     u'text': u'A portrait photo of Douglas Adams',
                     u'language': u'en'}},
             u'property': u'P2096',
             u'hash': u'5220766c2a4c803feb845e3dd3dbe3a8893a2789',
             u'snaktype': u'value'},
            {u'datatype': u'monolingualtext',
             u'datavalue': {
                 u'type': u'monolingualtext',
                 u'value': {u'text': u'Portrait de Douglas Adams.',
                            u'language': u'fr'}},
             u'property': u'P2096',
             u'hash': u'3e61ddc5db06441ca450d9df1b27401afe9c2718',
             u'snaktype': u'value'},
            {u'datatype': u'monolingualtext',
             u'datavalue': {
                 u'type': u'monolingualtext',
                 u'value': {
                     u'text': u"Douglas Adams' Portr\xe4t.",
                     u'language': u'de'}},
             u'property': u'P2096',
             u'hash': u'daa551e283c4d6c7637beeb49174ca8666b78fae',
             u'snaktype': u'value'},
            {u'datatype': u'monolingualtext',
             u'datavalue': {u'type': u'monolingualtext',
                            u'value': {u'text': u'Portr\xe9t Douglase Adamse',
                                       u'language': u'cs'}},
             u'property': u'P2096',
             u'hash': u'c67416544467f9ab404b4b01323fc59a901257ec',
             u'snaktype': u'value'},
            {u'datatype': u'monolingualtext',
             u'datavalue': {
                 u'type': u'monolingualtext',
                 u'value': {
                     u'text': u'\u05d3\u05d9\u05d5\u05e7\u05e0\u05d5 \u05e9\u05dc \u05d3\u05d0\u05d2\u05dc\u05e1 \u05d0\u05d3\u05de\u05e1.',
                     u'language': u'he'}},
             u'property': u'P2096',
             u'hash': u'143d7b420be9b46cd82cdefb13f8388f69204978',
             u'snaktype': u'value'},
            {u'datatype': u'monolingualtext',
             u'datavalue': {
                 u'type': u'monolingualtext', u'value': {
                     u'text': u'\u041f\u043e\u0440\u0442\u0440\u0435\u0442 \u0414\u0443\u0433\u043b\u0430\u0441\u0430 \u0410\u0434\u0430\u043c\u0441\u0430',
                     u'language': u'ru'}}, u'property': u'P2096',
             u'hash': u'71352d2e108d8928e04f35ccc499f3dd5a1d324c',
             u'snaktype': u'value'},
            {u'datatype': u'monolingualtext',
             u'datavalue': {
                 u'type': u'monolingualtext',
                 u'value': {
                     u'text': u'Retrato de Douglas Adams.',
                     u'language': u'es'}},
             u'property': u'P2096',
             u'hash': u'd6a97c29af0840ae5a26ca57c116a0dbfc2cf8fa',
             u'snaktype': u'value'},
            {u'datatype': u'monolingualtext',
             u'datavalue': {u'type': u'monolingualtext',
                            u'value': {u'text': u'Douglas Adamsen erretratua.',
                                       u'language': u'eu'}},
             u'property': u'P2096',
             u'hash': u'34d5b0907828496ae7c902f5df236ef00ec04a10',
             u'snaktype': u'value'},
            {u'datatype': u'monolingualtext',
             u'datavalue': {
                 u'type': u'monolingualtext',
                 u'value': {
                     u'text': u'\u041f\u043e\u0440\u0442\u0440\u0435\u0442 \u043d\u0430 \u0414\u0430\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                     u'language': u'mk'}},
             u'property': u'P2096',
             u'hash': u'ed16424e72d43160f1d72b7cd2d44eaddf624f4e',
             u'snaktype': u'value'}]},
        u'qualifiers-order': [u'P2096'], u'type': u'statement',
        u'id': u'Q42$44889d0f-474c-4fb9-1961-9a3366cbbb9e'})]}

for claim in itempage.claims['P18'] + itempage.claims['P1442']:
    print claim

expected_links = [
    (128, [
        u'Q42$44889d0f-474c-4fb9-1961-9a3366cbbb9e',
        'https://commons.wikimedia.org/wiki/File:Douglas_adams_portrait_cropped.jpg',
        u'https://commons.wikimedia.org/w/thumb.php?width=128&f=Douglas_adams_portrait_cropped.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/c/c0/Douglas_adams_portrait_cropped.jpg']),
    (64, [
        u'Q42$44889d0f-474c-4fb9-1961-9a3366cbbb9e',
        'https://commons.wikimedia.org/wiki/File:Douglas_adams_portrait_cropped.jpg',
        u'https://commons.wikimedia.org/w/thumb.php?width=64&f=Douglas_adams_portrait_cropped.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/c/c0/Douglas_adams_portrait_cropped.jpg'])
]

expected_types = [
    ('P18', [u'Q42$44889d0f-474c-4fb9-1961-9a3366cbbb9e',
        'https://commons.wikimedia.org/wiki/File:Douglas_adams_portrait_cropped.jpg',
        u'https://commons.wikimedia.org/w/thumb.php?width=128&f=Douglas_adams_portrait_cropped.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/c/c0/Douglas_adams_portrait_cropped.jpg']),
    ('P1442', [
        u'Q42$db1ba2ba-47b9-3650-e6c4-db683abf788c',
        "https://commons.wikimedia.org/wiki/File:Douglas_Adams'_gravestone.jpg",
        u"https://commons.wikimedia.org/w/thumb.php?width=128&f=Douglas_Adams'_gravestone.jpg",
        'https://upload.wikimedia.org/wikipedia/commons/f/fe/Douglas_Adams%27_gravestone.jpg']
     )]


@pytest.mark.parametrize('width,expected_links', expected_links)
def test_get_images(width, expected_links):
    images = get_images(itempage)
    assert images

    assert isinstance(images, dict)
    assert len(images) == len(
        [at for at in image_attributes if at in itempage.claims])
    print images.keys()
    assert all([len(values.values()) == 4 for values in images.values()])
    assert images['P18'].values()[1]
    assert get_images(itempage, width)['P18'].values() == expected_links


@pytest.mark.parametrize('image_type,expected_types', expected_types)
def test_get_image(image_type, expected_types):
    assert get_image(itempage=itempage, image_type=image_type,include_claim_id=True).values() == expected_types
