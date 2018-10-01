#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
An example of a Wikidata page
'''
from pywikibot import (Claim, ItemPage)
from pywikibot.site import DataSite

itempage = {
    u'claims': {u'P535': [Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                         {u'type': u'statement',
                                          u'references': [{
                                              u'snaks': {
                                                  u'P813': [
                                                      {
                                                          u'datatype': u'time',
                                                          u'datavalue': {
                                                              u'type': u'time',
                                                              u'value': {
                                                                  u'after': 0,
                                                                  u'precision': 11,
                                                                  u'time': u'+00000002013-12-07T00:00:00Z',
                                                                  u'timezone': 0,
                                                                  u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                                  u'before': 0}},
                                                          u'property': u'P813',
                                                          u'snaktype': u'value'}],
                                                  u'P577': [
                                                      {
                                                          u'datatype': u'time',
                                                          u'datavalue': {
                                                              u'type': u'time',
                                                              u'value': {
                                                                  u'after': 0,
                                                                  u'precision': 11,
                                                                  u'time': u'+00000002001-06-25T00:00:00Z',
                                                                  u'timezone': 0,
                                                                  u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                                  u'before': 0}},
                                                          u'property': u'P577',
                                                          u'snaktype': u'value'}],
                                                  u'P123': [
                                                      {
                                                          u'datatype': u'wikibase-item',
                                                          u'datavalue': {
                                                              u'type': u'wikibase-entityid',
                                                              u'value': {
                                                                  u'entity-type': u'item',
                                                                  u'numeric-id': 63056}},
                                                          u'property': u'P123',
                                                          u'snaktype': u'value'}],
                                                  u'P1476': [
                                                      {
                                                          u'datatype': u'monolingualtext',
                                                          u'datavalue': {
                                                              u'type': u'monolingualtext',
                                                              u'value': {
                                                                  u'text': u'Douglas Noel Adams',
                                                                  u'language': u'en'}},
                                                          u'property': u'P1476',
                                                          u'snaktype': u'value'}],
                                                  u'P854': [
                                                      {
                                                          u'datatype': u'url',
                                                          u'datavalue': {
                                                              u'type': u'string',
                                                              u'value': u'http://www.findagrave.com/cgi-bin/fg.cgi?page=gr&GRid=22814'},
                                                          u'property': u'P854',
                                                          u'snaktype': u'value'}]},
                                              u'hash': u'7dfe2e0d2d86c960cf4b365dd64fe9934fcf9ffe',
                                              u'snaks-order': [
                                                  u'P1476',
                                                  u'P854',
                                                  u'P123',
                                                  u'P577',
                                                  u'P813']}],
                                          u'mainsnak': {
                                              u'datatype': u'external-id',
                                              u'datavalue': {u'type': u'string',
                                                             u'value': u'22814'},
                                              u'property': u'P535',
                                              u'snaktype': u'value'},
                                          u'id': u'q42$0DD4F039-6CDC-40C9-871B-63CDE4A47032',
                                          u'rank': u'normal'})],
                u'P2387': [
                    Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                   {u'type': u'statement',
                                    u'mainsnak': {
                                        u'datatype': u'external-id',
                                        u'datavalue': {
                                            u'type': u'string',
                                            u'value': u'1289170'},
                                        u'property': u'P2387',
                                        u'snaktype': u'value'},
                                    u'id': u'Q42$29c1b057-497d-7d15-864e-3d889a76c750',
                                    u'rank': u'normal'})],
                u'P434': [
                    Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                   {u'type': u'statement',
                                    u'mainsnak': {u'datatype': u'external-id',
                                                  u'datavalue': {
                                                      u'type': u'string',
                                                      u'value': u'e9ed318d-8cc5-4cf8-ab77-505e39ab6ea4'},
                                                  u'property': u'P434',
                                                  u'snaktype': u'value'},
                                    u'id': u'q42$fc61f952-4071-7cc1-c20a-dc7a90ad6515',
                                    u'rank': u'normal'})],
                u'P3762': [
                    Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                   {u'type': u'statement',
                                    u'mainsnak': {u'datatype': u'external-id',
                                                  u'datavalue': {
                                                      u'type': u'string',
                                                      u'value': u'140290'},
                                                  u'property': u'P3762',
                                                  u'snaktype': u'value'},
                                    u'id': u'Q42$6BC778E7-7176-4F20-A450-A9A0FC3B3209',
                                    u'rank': u'normal'})],
                u'P1273': [
                    Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                   {u'type': u'statement', u'references': [{
                                       u'snaks': {
                                           u'P854': [
                                               {
                                                   u'datatype': u'url',
                                                   u'datavalue': {
                                                       u'type': u'string',
                                                       u'value': u'https://viaf.org/viaf/113230702/'},
                                                   u'property': u'P854',
                                                   u'snaktype': u'value'}]},
                                       u'hash': u'cbd294ba99228d76563dacad5326342b7cbcd81c',
                                       u'snaks-order': [
                                           u'P854']}],
                                    u'mainsnak': {u'datatype': u'external-id',
                                                  u'datavalue': {
                                                      u'type': u'string',
                                                      u'value': u'a10667040'},
                                                  u'property': u'P1273',
                                                  u'snaktype': u'value'},
                                    u'id': u'Q42$4A2873C0-D848-4F3D-8066-38204E50414C',
                                    u'rank': u'normal'})], u'P2469': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'238p'},
                                          u'property': u'P2469',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$32DACDAA-0C29-489B-B587-7CB5D374EEE5',
                            u'rank': u'normal'})],
                u'P1375': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 54919}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'759b2a264fff886006b6f49c3ef2f1acbfd1cef0',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'000010283'},
                                          u'property': u'P1375',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$97db6877-4c06-88ce-2db5-aaba53383fd2',
                            u'rank': u'normal'})],
                u'P136': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P577': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-03-11T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P577',
                                           u'snaktype': u'value'}],
                                   u'P123': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 11148}},
                                           u'property': u'P123',
                                           u'snaktype': u'value'}],
                                   u'P1476': [
                                       {
                                           u'datatype': u'monolingualtext',
                                           u'datavalue': {
                                               u'type': u'monolingualtext',
                                               u'value': {
                                                   u'text': u'Douglas Adams is still the king of comic science fiction',
                                                   u'language': u'en'}},
                                           u'property': u'P1476',
                                           u'snaktype': u'value'}],
                                   u'P854': [
                                       {
                                           u'datatype': u'url',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'https://www.theguardian.com/books/2013/mar/11/douglas-adams-king-comic-science-fiction'},
                                           u'property': u'P854',
                                           u'snaktype': u'value'}]},
                               u'hash': u'2f8e9f13763cdad3dcd7bc1cde454c244907cda2',
                               u'snaks-order': [
                                   u'P854',
                                   u'P1476',
                                   u'P123',
                                   u'P577']}],
                            u'mainsnak': {u'datatype': u'wikibase-item',
                                          u'datavalue': {
                                              u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 24925}},
                                          u'property': u'P136',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$0ff4aeeb-4fdb-56cf-5fe9-916e1bbbbc73',
                            u'rank': u'normal'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P577': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-03-11T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P577',
                                           u'snaktype': u'value'}],
                                   u'P123': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 11148}},
                                           u'property': u'P123',
                                           u'snaktype': u'value'}],
                                   u'P1476': [
                                       {
                                           u'datatype': u'monolingualtext',
                                           u'datavalue': {
                                               u'type': u'monolingualtext',
                                               u'value': {
                                                   u'text': u'Douglas Adams is still the king of comic science fiction',
                                                   u'language': u'en'}},
                                           u'property': u'P1476',
                                           u'snaktype': u'value'}],
                                   u'P854': [
                                       {
                                           u'datatype': u'url',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'https://www.theguardian.com/books/2013/mar/11/douglas-adams-king-comic-science-fiction'},
                                           u'property': u'P854',
                                           u'snaktype': u'value'}]},
                               u'hash': u'2f8e9f13763cdad3dcd7bc1cde454c244907cda2',
                               u'snaks-order': [
                                   u'P854',
                                   u'P1476',
                                   u'P123',
                                   u'P577']},
                               {
                                   u'snaks': {
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.screenonline.org.uk/people/id/1233876/index.html'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'bab32d323b6c92d91ff7d0c4707346012900761b',
                                   u'snaks-order': [
                                       u'P854']}],
                            u'mainsnak': {u'datatype': u'wikibase-item',
                                          u'datavalue': {
                                              u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 40831}},
                                          u'property': u'P136',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$2ac90f53-4dc5-2ecc-d595-70f7c43f2fda',
                            u'rank': u'normal'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P854': [
                                       {
                                           u'datatype': u'url',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'https://www.theguardian.com/commentisfree/2015/aug/07/hitchhikers-guide-galaxy-book-changed-me-vogons-economics'},
                                           u'property': u'P854',
                                           u'snaktype': u'value'}]},
                               u'hash': u'fb6300cf6bc0ce72d3d960d4d671fd772125d3ee',
                               u'snaks-order': [
                                   u'P854']}],
                            u'mainsnak': {u'datatype': u'wikibase-item',
                                          u'datavalue': {
                                              u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 128758}},
                                          u'property': u'P136',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$43f046bb-47a4-00aa-5174-aa7ca343396b',
                            u'rank': u'normal'})], u'P3154': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'adamsdou'},
                                          u'property': u'P3154',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$916F4133-B433-4FA1-B888-F86DA132B1DE',
                            u'rank': u'normal'})], u'P1284': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'00000020676'},
                                          u'property': u'P1284',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$2EE16C9C-B74B-4322-9542-4A132555B363',
                            u'rank': u'normal'})], u'P1280': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'6050147'},
                                          u'property': u'P1280',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$0DFBA3E4-F98E-4ED5-AE30-CE8556429229',
                            u'rank': u'normal'})], u'P2435': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'208947'},
                                          u'property': u'P2435',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$daf51782-49c8-1e46-7738-e923dba42cb0',
                            u'rank': u'normal'})], u'P2168': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'271209'},
                                          u'property': u'P2168',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$77b4aae6-473c-f860-1918-9ca573cdfb2e',
                            u'rank': u'normal'})],
                u'P1411': [
                    Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                   {u'mainsnak': {u'datatype': u'wikibase-item',
                                                  u'datavalue': {
                                                      u'type': u'wikibase-entityid',
                                                      u'value': {
                                                          u'entity-type': u'item',
                                                          u'numeric-id': 3414212}},
                                                  u'property': u'P1411',
                                                  u'snaktype': u'value'},
                                    u'rank': u'normal',
                                    u'qualifiers': {u'P585': [
                                        {u'datatype': u'time',
                                         u'datavalue': {u'type': u'time',
                                                        u'value': {u'after': 0,
                                                                   u'precision': 9,
                                                                   u'time': u'+00000001979-00-00T00:00:00Z',
                                                                   u'timezone': 0,
                                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                                   u'before': 0}},
                                         u'property': u'P585',
                                         u'hash': u'21ce2394cef40d7e380a249ee1911d6efa38d1af',
                                         u'snaktype': u'value'}],
                                        u'P1686': [
                                            {
                                                u'datatype': u'wikibase-item',
                                                u'datavalue': {
                                                    u'type': u'wikibase-entityid',
                                                    u'value': {
                                                        u'entity-type': u'item',
                                                        u'numeric-id': 3521267}},
                                                u'property': u'P1686',
                                                u'hash': u'6976dd054773df55af13d08387ac072427e71cb6',
                                                u'snaktype': u'value'}]},
                                    u'qualifiers-order': [u'P1686', u'P585'],
                                    u'type': u'statement',
                                    u'id': u'Q42$1B3C484C-643E-45D0-B01C-F6DAD3D1F88E'}),
                    Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                   {u'mainsnak': {u'datatype': u'wikibase-item',
                                                  u'datavalue': {
                                                      u'type': u'wikibase-entityid',
                                                      u'value': {
                                                          u'entity-type': u'item',
                                                          u'numeric-id': 2576795}},
                                                  u'property': u'P1411',
                                                  u'snaktype': u'value'},
                                    u'rank': u'normal',
                                    u'qualifiers': {u'P585': [
                                        {u'datatype': u'time',
                                         u'datavalue': {u'type': u'time',
                                                        u'value': {u'after': 0,
                                                                   u'precision': 9,
                                                                   u'time': u'+00000001983-00-00T00:00:00Z',
                                                                   u'timezone': 0,
                                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                                   u'before': 0}},
                                         u'property': u'P585',
                                         u'hash': u'1f4575b36bd16a12b6ce37bd18576d2809be2317',
                                         u'snaktype': u'value'}],
                                        u'P1686': [
                                            {
                                                u'datatype': u'wikibase-item',
                                                u'datavalue': {
                                                    u'type': u'wikibase-entityid',
                                                    u'value': {
                                                        u'entity-type': u'item',
                                                        u'numeric-id': 721}},
                                                u'property': u'P1686',
                                                u'hash': u'e7bb7e6e72fbe3cab6b40bc12cd86966ff4f9175',
                                                u'snaktype': u'value'}]},
                                    u'qualifiers-order': [u'P585', u'P1686'],
                                    u'type': u'statement',
                                    u'id': u'Q42$285E0C13-9674-4131-9556-51B316A57AEE'})],
                u'P910': [Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                         {u'type': u'statement',
                                          u'mainsnak': {
                                              u'datatype': u'wikibase-item',
                                              u'datavalue': {
                                                  u'type': u'wikibase-entityid',
                                                  u'value': {
                                                      u'entity-type': u'item',
                                                      u'numeric-id': 8935487}},
                                              u'property': u'P910',
                                              u'snaktype': u'value'},
                                          u'id': u'Q42$3B111597-2138-4517-85AD-FD0056D3DEB0',
                                          u'rank': u'normal'})], u'P1415': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'75853'},
                                          u'property': u'P1415',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$E10A1B54-9D65-4334-8F2C-58B21B49D565',
                            u'rank': u'normal'})], u'P1417': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'biography/Douglas-Adams'},
                                          u'property': u'P1417',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$2B2DC742-3BC1-4DAA-BECF-C81A33453B57',
                            u'rank': u'normal'})], u'P2163': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'56544'},
                                          u'property': u'P2163',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$7424C174-D7A8-4D60-89E3-416156EAC76D',
                            u'rank': u'normal'})], u'P1303': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 6607}},
                               u'property': u'P1303', u'snaktype': u'value'},
                            u'id': u'Q42$67547850-C3A0-4C99-AFE4-3C18956CB19A',
                            u'rank': u'normal'})], u'P2963': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'4'},
                                          u'property': u'P2963',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$eb0d02d3-4b1d-0e19-cb86-78a0a5439144',
                            u'rank': u'normal'})], u'P1263': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'731/000023662'},
                                          u'property': u'P1263',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$9B26C69E-7B9E-43EB-9B20-AD1305D1EE6B',
                            u'rank': u'normal'})], u'P998': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'Arts/Literature/Authors/A/Adams,_Douglas/'},
                                          u'property': u'P998',
                                          u'snaktype': u'value'},
                            u'rank': u'preferred', u'qualifiers': {
                               u'P407': [{u'datatype': u'wikibase-item',
                                          u'datavalue': {
                                              u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 1860}},
                                          u'property': u'P407',
                                          u'hash': u'daf1c4fcb58181b02dff9cc89deb084004ddae4b',
                                          u'snaktype': u'value'}]},
                            u'qualifiers-order': [u'P407'],
                            u'type': u'statement',
                            u'id': u'Q42$BE724F6B-6981-4DE9-B90C-338768A4BFC4'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'World/Dansk/Kultur/Litteratur/Forfattere/A/Adams,_Douglas/'},
                                          u'property': u'P998',
                                          u'snaktype': u'value'},
                            u'rank': u'normal', u'qualifiers': {
                               u'P407': [{u'datatype': u'wikibase-item',
                                          u'datavalue': {
                                              u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 9035}},
                                          u'property': u'P407',
                                          u'hash': u'4a90e9ca00d0eae667dbbdeb5d575498ec041124',
                                          u'snaktype': u'value'}]},
                            u'qualifiers-order': [u'P407'],
                            u'type': u'statement',
                            u'id': u'Q42$5776B538-2441-4B9E-9C39-4E6289396763'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'World/Fran\xe7ais/Arts/Litt\xe9rature/Genres/Science-fiction_et_fantastique/Auteurs/Adams,_Douglas/'},
                                          u'property': u'P998',
                                          u'snaktype': u'value'},
                            u'rank': u'normal', u'qualifiers': {
                               u'P407': [{u'datatype': u'wikibase-item',
                                          u'datavalue': {
                                              u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 150}},
                                          u'property': u'P407',
                                          u'hash': u'd197d0a5efa4b4c23a302a829dd3ef43684fe002',
                                          u'snaktype': u'value'}]},
                            u'qualifiers-order': [u'P407'],
                            u'type': u'statement',
                            u'id': u'Q42$B60CF952-9C65-4875-A4BA-6B8516C81E99'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'World/Deutsch/Kultur/Literatur/Autoren_und_Autorinnen/A/Adams,_Douglas/'},
                                          u'property': u'P998',
                                          u'snaktype': u'value'},
                            u'rank': u'normal', u'qualifiers': {
                               u'P407': [{u'datatype': u'wikibase-item',
                                          u'datavalue': {
                                              u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 188}},
                                          u'property': u'P407',
                                          u'hash': u'46bfd327b830f66f7061ea92d1be430c135fa91f',
                                          u'snaktype': u'value'}]},
                            u'qualifiers-order': [u'P407'],
                            u'type': u'statement',
                            u'id': u'Q42$A0B48E74-C934-42B9-A583-FB3EAE4BC9BA'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'World/Italiano/Arte/Letteratura/Autori/A/Adams,_Douglas/'},
                                          u'property': u'P998',
                                          u'snaktype': u'value'},
                            u'rank': u'normal', u'qualifiers': {
                               u'P407': [{u'datatype': u'wikibase-item',
                                          u'datavalue': {
                                              u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 652}},
                                          u'property': u'P407',
                                          u'hash': u'2ab2e485ce235a18142330fa1873a5bba7115d23',
                                          u'snaktype': u'value'}]},
                            u'qualifiers-order': [u'P407'],
                            u'type': u'statement',
                            u'id': u'Q42$F2632AC4-6F24-49E4-9E4E-B008F26BA8CE'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'World/Svenska/Kultur/Litteratur/Genre/Science_fiction_och_fantasy/F\xf6rfattare/Adams,_Douglas/'},
                                          u'property': u'P998',
                                          u'snaktype': u'value'},
                            u'rank': u'normal', u'qualifiers': {
                               u'P407': [{u'datatype': u'wikibase-item',
                                          u'datavalue': {
                                              u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 9027}},
                                          u'property': u'P407',
                                          u'hash': u'e41efcf0acaa18ea8fca63b87e2e0c24618f5664',
                                          u'snaktype': u'value'}]},
                            u'qualifiers-order': [u'P407'],
                            u'type': u'statement',
                            u'id': u'Q42$84B82B5A-8F33-4229-B988-BF960E676875'})],
                u'P1266': [Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                          {u'type': u'statement',
                                           u'mainsnak': {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'97049'},
                                               u'property': u'P1266',
                                               u'snaktype': u'value'},
                                           u'id': u'Q42$788bd2c1-46a0-9898-6410-5339ecf90a8b',
                                           u'rank': u'normal'})], u'P5587': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1798125}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}],
                                   u'P577': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002018-03-26T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P577',
                                           u'snaktype': u'value'}],
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002018-08-24T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P854': [
                                       {
                                           u'datatype': u'url',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'https://libris.kb.se/katalogisering/1zcfh30k0gr4zxt'},
                                           u'property': u'P854',
                                           u'snaktype': u'value'}]},
                               u'hash': u'32d6fcfbc1af77960e30b94b4c199ac07b39730d',
                               u'snaks-order': [
                                   u'P248',
                                   u'P854',
                                   u'P577',
                                   u'P813']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'1zcfh30k0gr4zxt'},
                                          u'property': u'P5587',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$21178ECC-11CC-4CD3-BBD4-E35EB788B26E',
                            u'rank': u'normal'})], u'P5357': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 28054658}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'154031fdff9fbadaa5f15c8b7e4ae46ca13db45a',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'adams_douglas'},
                                          u'property': u'P5357',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$63B203C0-A6B4-40A7-9942-09F5AA7DE92F',
                            u'rank': u'normal'})], u'P1816': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'mp60152'},
                                          u'property': u'P1816',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$A70EF87C-33F4-4366-B0A7-000C5A3A43E5',
                            u'rank': u'normal'})], u'P3222': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'douglas-adams'},
                                          u'property': u'P3222',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$D41D834D-0BD4-411C-A671-2B7BE6053EB5',
                            u'rank': u'normal'})], u'P1015': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'90196888'},
                                          u'property': u'P1015',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$6583fdb7-4ffa-9fe1-4288-1a1cbb2950d0',
                            u'rank': u'normal'})], u'P1258': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'celebrity/douglas_adams'},
                                          u'property': u'P1258',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$4bc2af98-4182-3b11-0df3-80aac8e24081',
                            u'rank': u'normal'})], u'P2605': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'39534'},
                                          u'property': u'P2605',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$7398157a-409e-7d35-7d89-7351426cb36c',
                            u'rank': u'normal'})], u'P2604': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'246164'},
                                          u'property': u'P2604',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$ca83a88a-470c-b93a-2393-35a1de0a9c60',
                            u'rank': u'normal'})], u'P213': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 54919}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'759b2a264fff886006b6f49c3ef2f1acbfd1cef0',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'0000 0000 8045 6315'},
                                          u'property': u'P213',
                                          u'snaktype': u'value'},
                            u'id': u'q42$1CF5840B-A274-402B-9556-F202C2F9B831',
                            u'rank': u'normal'})], u'P1315': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'847711'},
                                          u'property': u'P1315',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$809C95C5-ED69-432B-91D8-FF7C8C9965A2',
                            u'rank': u'normal'})], u'P214': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1551807}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'14d2400e3b1d36332748dc330276f099eeaa8800',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'113230702'},
                                          u'property': u'P214',
                                          u'snaktype': u'value'},
                            u'id': u'q42$488251B2-6732-4D49-85B0-6101803C97AB',
                            u'rank': u'normal'})], u'P1953': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 14005}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}],
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002015-07-27T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}]},
                               u'hash': u'b2e93db8744c6c00360db0868706706c3d951d92',
                               u'snaks-order': [
                                   u'P248',
                                   u'P813']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'134923'},
                                          u'property': u'P1953',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$6C466225-DCB1-47B9-B868-C285F016E216',
                            u'rank': u'normal'})], u'P4193': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'Douglas_Noel_Adams_(1952-2001)'},
                                          u'property': u'P4193',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$769463b3-4b83-cf93-d5ef-0b4e98e1cf33',
                            u'rank': u'normal'})], u'P119': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-12-07T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P407': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1860}},
                                           u'property': u'P407',
                                           u'snaktype': u'value'}],
                                   u'P123': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 533697}},
                                           u'property': u'P123',
                                           u'snaktype': u'value'}],
                                   u'P1476': [
                                       {
                                           u'datatype': u'monolingualtext',
                                           u'datavalue': {
                                               u'type': u'monolingualtext',
                                               u'value': {
                                                   u'text': u'Who\u2019s here',
                                                   u'language': u'en'}},
                                           u'property': u'P1476',
                                           u'snaktype': u'value'}],
                                   u'P854': [
                                       {
                                           u'datatype': u'url',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'http://highgatecemetery.org/visit/who'},
                                           u'property': u'P854',
                                           u'snaktype': u'value'}]},
                               u'hash': u'8a052e1954b77ac5a7a865617768d7526599f913',
                               u'snaks-order': [
                                   u'P854',
                                   u'P407',
                                   u'P123',
                                   u'P813',
                                   u'P1476']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 533697}},
                                u'property': u'P119',
                                u'snaktype': u'value'},
                            u'id': u'q42$881F40DC-0AFE-4FEB-B882-79600D234273',
                            u'rank': u'normal'})], u'P5361': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P4656': [
                                       {
                                           u'datatype': u'url',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'https://www.wikidata.org/w/index.php?title=Wikidata:Property_proposal/BNB_person_ID&oldid=700383726'},
                                           u'property': u'P4656',
                                           u'snaktype': u'value'}]},
                               u'hash': u'133415593c921f4a8641abd7123e2c4d451cca0c',
                               u'snaks-order': [
                                   u'P4656']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'AdamsDouglas1952-2001'},
                                          u'property': u'P5361',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$E5FCDDD6-0021-4543-8815-ACC8C2877C9F',
                            u'rank': u'normal'})], u'P691': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 54919}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'759b2a264fff886006b6f49c3ef2f1acbfd1cef0',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'jn19990000029'},
                                          u'property': u'P691',
                                          u'snaktype': u'value'},
                            u'id': u'q42$704392C4-6E77-4E25-855F-7CF2D198DD6A',
                            u'rank': u'normal'})], u'P856': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'mainsnak': {u'datatype': u'url',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'http://douglasadams.com/'},
                                          u'property': u'P856',
                                          u'snaktype': u'value'},
                            u'rank': u'normal', u'qualifiers': {
                               u'P407': [{u'datatype': u'wikibase-item',
                                          u'datavalue': {
                                              u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 1860}},
                                          u'property': u'P407',
                                          u'hash': u'daf1c4fcb58181b02dff9cc89deb084004ddae4b',
                                          u'snaktype': u'value'}]},
                            u'qualifiers-order': [u'P407'],
                            u'type': u'statement',
                            u'id': u'Q42$D32EFF42-C5E2-482A-AE97-2159D6A99524'})],
                u'P5365': [Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                          {u'type': u'statement',
                                           u'references': [{
                                               u'snaks': {
                                                   u'P143': [
                                                       {
                                                           u'datatype': u'wikibase-item',
                                                           u'datavalue': {
                                                               u'type': u'wikibase-entityid',
                                                               u'value': {
                                                                   u'entity-type': u'item',
                                                                   u'numeric-id': 58679}},
                                                           u'property': u'P143',
                                                           u'snaktype': u'value'}]},
                                               u'hash': u'd0803e2b0f1149c9e82d42c919545a7e3fdb1442',
                                               u'snaks-order': [
                                                   u'P143']}],
                                           u'mainsnak': {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'42'},
                                               u'property': u'P5365',
                                               u'snaktype': u'value'},
                                           u'id': u'Q42$7894D1B9-2FB1-4F0D-BC65-D0736B68C179',
                                           u'rank': u'normal'})], u'P18': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"), {
                u'mainsnak': {u'datatype': u'commonsMedia',
                              u'datavalue': {u'type': u'string',
                                             u'value': u'Douglas adams portrait cropped.jpg'},
                              u'property': u'P18', u'snaktype': u'value'},
                u'rank': u'normal',
                u'qualifiers': {u'P2096': [{u'datatype': u'monolingualtext',
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
                                                u'value': {
                                                    u'text': u'Portrait de Douglas Adams.',
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
                                            u'datavalue': {
                                                u'type': u'monolingualtext',
                                                u'value': {
                                                    u'text': u'Portr\xe9t Douglase Adamse',
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
                                                u'type': u'monolingualtext',
                                                u'value': {
                                                    u'text': u'\u041f\u043e\u0440\u0442\u0440\u0435\u0442 \u0414\u0443\u0433\u043b\u0430\u0441\u0430 \u0410\u0434\u0430\u043c\u0441\u0430',
                                                    u'language': u'ru'}},
                                            u'property': u'P2096',
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
                                            u'datavalue': {
                                                u'type': u'monolingualtext',
                                                u'value': {
                                                    u'text': u'Douglas Adamsen erretratua.',
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
                u'id': u'Q42$44889d0f-474c-4fb9-1961-9a3366cbbb9e'})],
                u'P1559': [
                    Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                   {u'type': u'statement', u'mainsnak': {
                                       u'datatype': u'monolingualtext',
                                       u'datavalue': {
                                           u'type': u'monolingualtext',
                                           u'value': {u'text': u'Douglas Adams',
                                                      u'language': u'en'}},
                                       u'property': u'P1559',
                                       u'snaktype': u'value'},
                                    u'id': u'Q42$88CB3380-ADFB-427B-87E5-C8D537545FE8',
                                    u'rank': u'normal'})], u'P3373': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-12-07T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P407': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1860}},
                                           u'property': u'P407',
                                           u'snaktype': u'value'}],
                                   u'P123': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1373513}},
                                           u'property': u'P123',
                                           u'snaktype': u'value'}],
                                   u'P1476': [
                                       {
                                           u'datatype': u'monolingualtext',
                                           u'datavalue': {
                                               u'type': u'monolingualtext',
                                               u'value': {
                                                   u'text': u'Douglas Adams',
                                                   u'language': u'en'}},
                                           u'property': u'P1476',
                                           u'snaktype': u'value'}],
                                   u'P854': [
                                       {
                                           u'datatype': u'url',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'http://www.nndb.com/people/731/000023662/'},
                                           u'property': u'P854',
                                           u'snaktype': u'value'}]},
                               u'hash': u'9177d75c6061e9e1ab149c0aa01bee5a90e07415',
                               u'snaks-order': [
                                   u'P854',
                                   u'P407',
                                   u'P123',
                                   u'P813',
                                   u'P1476']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 14623673}},
                                u'property': u'P3373',
                                u'snaktype': u'value'},
                            u'id': u'Q42$A3B1288B-67A9-4491-A3AA-20F881C292B9',
                            u'rank': u'normal'})], u'P2048': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P854': [
                                       {
                                           u'datatype': u'url',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'https://books.google.ca/books?id=0oA8DwAAQBAJ&pg=PT80&lpg=PT80&dq=douglas+adams+1.96m&source=bl&ots=E6uXJtnh6b&sig=1Vt5jnRIeD5JnpG5AFRPQ6Aqphs&hl=en&sa=X&ved=0ahUKEwjJt-aUtdXYAhWJ6IMKHQQ7B9AQ6AEIXzAI#v=onepage&q=douglas%20adams%201.96m&f=false'},
                                           u'property': u'P854',
                                           u'snaktype': u'value'}]},
                               u'hash': u'c4a78b711b9ffddb611c43d69cee81ba070e60a0',
                               u'snaks-order': [
                                   u'P854']}],
                            u'mainsnak': {u'datatype': u'quantity',
                                          u'datavalue': {
                                              u'type': u'quantity',
                                              u'value': {
                                                  u'amount': u'+1.96',
                                                  u'lowerBound': None,
                                                  u'unit': u'http://www.wikidata.org/entity/Q11573',
                                                  u'upperBound': None}},
                                          u'property': u'P2048',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$b0bf3caf-481c-356b-03a2-e61174b8e6da',
                            u'rank': u'normal'})], u'P509': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-12-07T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P407': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1860}},
                                           u'property': u'P407',
                                           u'snaktype': u'value'}],
                                   u'P123': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 15290366}},
                                           u'property': u'P123',
                                           u'snaktype': u'value'}],
                                   u'P1476': [
                                       {
                                           u'datatype': u'monolingualtext',
                                           u'datavalue': {
                                               u'type': u'monolingualtext',
                                               u'value': {
                                                   u'text': u'Famous People - Douglas Adams',
                                                   u'language': u'en'}},
                                           u'property': u'P1476',
                                           u'snaktype': u'value'}],
                                   u'P854': [
                                       {
                                           u'datatype': u'url',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'http://www.historyorb.com/people/douglas-adams'},
                                           u'property': u'P854',
                                           u'snaktype': u'value'}]},
                               u'hash': u'61039b96706750437e9bfd3a6beaeb0bd1d16ef1',
                               u'snaks-order': [
                                   u'P854',
                                   u'P407',
                                   u'P123',
                                   u'P813',
                                   u'P1476']},
                               {
                                   u'snaks': {
                                       u'P123': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 11148}},
                                               u'property': u'P123',
                                               u'snaktype': u'value'}],
                                       u'P1476': [
                                           {
                                               u'datatype': u'monolingualtext',
                                               u'datavalue': {
                                                   u'type': u'monolingualtext',
                                                   u'value': {
                                                       u'text': u'Obituary: Douglas Adams',
                                                       u'language': u'en'}},
                                               u'property': u'P1476',
                                               u'snaktype': u'value'}],
                                       u'P407': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 1860}},
                                               u'property': u'P407',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002014-01-03T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.theguardian.com/news/2001/may/15/guardianobituaries.books'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}],
                                       u'P577': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002001-05-15T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P577',
                                               u'snaktype': u'value'}],
                                       u'P50': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 18145749}},
                                               u'property': u'P50',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'8ff79d35ac039707be382250be2789f2e21ee59f',
                                   u'snaks-order': [
                                       u'P1476',
                                       u'P123',
                                       u'P577',
                                       u'P407',
                                       u'P854',
                                       u'P813',
                                       u'P50']},
                               {
                                   u'snaks': {
                                       u'P123': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 192621}},
                                               u'property': u'P123',
                                               u'snaktype': u'value'}],
                                       u'P1476': [
                                           {
                                               u'datatype': u'monolingualtext',
                                               u'datavalue': {
                                                   u'type': u'monolingualtext',
                                                   u'value': {
                                                       u'text': u"Hitch Hiker's Guide author Douglas Adams dies aged 49",
                                                       u'language': u'en'}},
                                               u'property': u'P1476',
                                               u'snaktype': u'value'}],
                                       u'P407': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 1860}},
                                               u'property': u'P407',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002014-01-03T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.telegraph.co.uk/news/uknews/1330072/Hitch-Hikers-Guide-author-Douglas-Adams-dies-aged-49.html'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}],
                                       u'P577': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002001-05-13T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P577',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'a51c458cb5e6abe7176b570b062bd8989bae0821',
                                   u'snaks-order': [
                                       u'P1476',
                                       u'P123',
                                       u'P577',
                                       u'P407',
                                       u'P854',
                                       u'P813']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 12152}},
                                u'property': u'P509',
                                u'snaktype': u'value'},
                            u'id': u'q42$E651BD8A-EA3E-478A-8558-C956EE60B29F',
                            u'rank': u'normal'})], u'P345': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 48183}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'9a24f7c0208b05d6be97077d855671d1dfdbc0dd',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'nm0010930'},
                                          u'property': u'P345',
                                          u'snaktype': u'value'},
                            u'id': u'q42$231549F5-0296-4D87-993D-6CBE3F24C0D2',
                            u'rank': u'normal'})], u'P1006': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'068744307'},
                                          u'property': u'P1006',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$B7643D02-6EF0-4932-A36A-3A2D4DA3F578',
                            u'rank': u'normal'})], u'P349': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 48183}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'9a24f7c0208b05d6be97077d855671d1dfdbc0dd',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'00430962'},
                                          u'property': u'P349',
                                          u'snaktype': u'value'},
                            u'id': u'q42$31B1BC2A-D09F-4151-AD2B-5CEA229B9058',
                            u'rank': u'normal'})], u'P1005': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 54919}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'759b2a264fff886006b6f49c3ef2f1acbfd1cef0',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'68537'},
                                          u'property': u'P1005',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$35342507-3E6E-4F3C-9BB6-F05C9F7DBD95',
                            u'rank': u'normal'})], u'P1003': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'RUNLRAUTH770139180'},
                                          u'property': u'P1003',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$5644B49C-B3EA-4540-B2EB-78F3AC3B89BB',
                            u'rank': u'normal'})], u'P2611': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'douglas_adams'},
                                          u'property': u'P2611',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$3169835D-BBAB-48C0-B197-7428BDBAC28E',
                            u'rank': u'normal'})], u'P463': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 857679}},
                               u'property': u'P463', u'snaktype': u'value'},
                            u'id': u'Q42$45E1E647-4941-42E1-8428-A6F6C848276A',
                            u'rank': u'normal'})], u'P2191': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'NILF10014'},
                                          u'property': u'P2191',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$2DB4179B-D385-495D-B248-9D0A53041DD4',
                            u'rank': u'normal'})], u'P109': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'commonsMedia',
                               u'datavalue': {u'type': u'string',
                                              u'value': u'Douglas Adams signature.svg'},
                               u'property': u'P109', u'snaktype': u'value'},
                            u'id': u'Q42$e5b8e5d5-4243-43e3-3476-c8f1572f14fa',
                            u'rank': u'normal'})], u'P108': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 9531}},
                               u'property': u'P108', u'snaktype': u'value'},
                            u'id': u'Q42$853B16C8-1AB3-489A-831E-AEAD7E94AB87',
                            u'rank': u'normal'})], u'P106': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 214917}},
                               u'property': u'P106', u'snaktype': u'value'},
                            u'id': u'Q42$e0f736bd-4711-c43b-9277-af1e9b2fb85f',
                            u'rank': u'normal'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-12-07T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 193563}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}],
                                   u'P268': [
                                       {
                                           u'datatype': u'external-id',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'11888092r'},
                                           u'property': u'P268',
                                           u'snaktype': u'value'}]},
                               u'hash': u'f67142030dd221e1441a10a7438323ad44f35be8',
                               u'snaks-order': [
                                   u'P248',
                                   u'P268',
                                   u'P813']},
                               {
                                   u'snaks': {
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.jinni.com/tv/the-hitchhikers-guide-to-the-galaxy/cast-crew/'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'0fed87b3320338e0ed0587df9b43e47cfcf5b69f',
                                   u'snaks-order': [
                                       u'P854']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 28389}},
                                u'property': u'P106',
                                u'snaktype': u'value'},
                            u'id': u'q42$E13E619F-63EF-4B72-99D9-7A45C7C6AD34',
                            u'rank': u'normal'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 6625963}},
                               u'property': u'P106', u'snaktype': u'value'},
                            u'id': u'Q42$D6E21D67-05D6-4A0B-8458-0744FCEED13D',
                            u'rank': u'normal'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 4853732}},
                               u'property': u'P106', u'snaktype': u'value'},
                            u'id': u'Q42$7eb8aaef-4ddf-8b87-bd02-406f91a296bd',
                            u'rank': u'normal'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-12-07T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 193563}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}],
                                   u'P268': [
                                       {
                                           u'datatype': u'external-id',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'11888092r'},
                                           u'property': u'P268',
                                           u'snaktype': u'value'}]},
                               u'hash': u'f67142030dd221e1441a10a7438323ad44f35be8',
                               u'snaks-order': [
                                   u'P248',
                                   u'P268',
                                   u'P813']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 18844224}},
                                u'property': u'P106',
                                u'snaktype': u'value'},
                            u'id': u'q42$CBDC4890-D5A2-469C-AEBB-EFB682B891E7',
                            u'rank': u'normal'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 245068}},
                               u'property': u'P106', u'snaktype': u'value'},
                            u'id': u'Q42$58F0D772-9CE4-46AC-BF0D-FBBBAFA09603',
                            u'rank': u'normal'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 206855}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'288ab581e7d2d02995a26dfa8b091d96e78457fc',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 487596}},
                                u'property': u'P106',
                                u'snaktype': u'value'},
                            u'id': u'Q42$e469cda0-475d-8bb1-1dcd-f72c91161ebf',
                            u'rank': u'normal'})], u'P268': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 8447}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'd4bd87b862b12d99d26e86472d44f26858dee639',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'11888092r'},
                                          u'property': u'P268',
                                          u'snaktype': u'value'},
                            u'id': u'q42$BB4B67FE-FECA-4469-9DEE-3E8F03AC9F1D',
                            u'rank': u'normal'})], u'P269': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 54919}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'759b2a264fff886006b6f49c3ef2f1acbfd1cef0',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'026677636'},
                                          u'property': u'P269',
                                          u'snaktype': u'value'},
                            u'id': u'q42$D0E17F5E-4302-43F8-926B-5FE7AA8A4380',
                            u'rank': u'normal'})], u'P103': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 7979}},
                               u'property': u'P103', u'snaktype': u'value'},
                            u'id': u'Q42$b7526300-4ac5-a529-3a91-c8a0120673be',
                            u'rank': u'normal'})], u'P25': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-12-07T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P407': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1860}},
                                           u'property': u'P407',
                                           u'snaktype': u'value'}],
                                   u'P123': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1373513}},
                                           u'property': u'P123',
                                           u'snaktype': u'value'}],
                                   u'P1476': [
                                       {
                                           u'datatype': u'monolingualtext',
                                           u'datavalue': {
                                               u'type': u'monolingualtext',
                                               u'value': {
                                                   u'text': u'Douglas Adams',
                                                   u'language': u'en'}},
                                           u'property': u'P1476',
                                           u'snaktype': u'value'}],
                                   u'P854': [
                                       {
                                           u'datatype': u'url',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'http://www.nndb.com/people/731/000023662/'},
                                           u'property': u'P854',
                                           u'snaktype': u'value'}]},
                               u'hash': u'9177d75c6061e9e1ab149c0aa01bee5a90e07415',
                               u'snaks-order': [
                                   u'P854',
                                   u'P407',
                                   u'P123',
                                   u'P813',
                                   u'P1476']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 14623678}},
                                u'property': u'P25',
                                u'snaktype': u'value'},
                            u'id': u'q42$cf4cccbe-470e-e627-86a3-70ef115f601c',
                            u'rank': u'normal'})], u'P27': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 54919}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}],
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-12-07T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P214': [
                                       {
                                           u'datatype': u'external-id',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'113230702'},
                                           u'property': u'P214',
                                           u'snaktype': u'value'}]},
                               u'hash': u'2b369d0a4f1d4b801e734fe84a0b217e13dd2930',
                               u'snaks-order': [
                                   u'P248',
                                   u'P214',
                                   u'P813']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 145}},
                                u'property': u'P27',
                                u'snaktype': u'value'},
                            u'id': u'q42$DE2A0C89-6199-44D0-B727-D7A4BE031A2B',
                            u'rank': u'normal'})], u'P906': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1798125}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'3582332eaefe93a65e8d64b0f15f33e1094455c3',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'230807'},
                                          u'property': u'P906',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$D92DF8AE-786C-4C3E-8A33-BABD8CB06D31',
                            u'rank': u'normal'})], u'P21': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 54919}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}],
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-12-07T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P214': [
                                       {
                                           u'datatype': u'external-id',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'113230702'},
                                           u'property': u'P214',
                                           u'snaktype': u'value'}]},
                               u'hash': u'2b369d0a4f1d4b801e734fe84a0b217e13dd2930',
                               u'snaks-order': [
                                   u'P248',
                                   u'P214',
                                   u'P813']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 36578}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002015-07-07T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P227': [
                                           {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'119033364'},
                                               u'property': u'P227',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'a02f3a77ddd343e6b88be25696b055f5131c3d64',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P227',
                                       u'P813']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 20666306}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002015-10-10T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://data.bnf.fr/ark:/12148/cb11888092r'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'55d23126bca9913374faf69ba8fbd21474a74421',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P813',
                                       u'P854']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 6581097}},
                                u'property': u'P21',
                                u'snaktype': u'value'},
                            u'id': u'q42$39F4DE4F-C277-449C-9F99-512350971B5B',
                            u'rank': u'normal'})], u'P20': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 5375741}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}]},
                               u'hash': u'355b56329b78db22be549dec34f2570ca61ca056',
                               u'snaks-order': [
                                   u'P248']},
                               {
                                   u'snaks': {
                                       u'P123': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 9684}},
                                               u'property': u'P123',
                                               u'snaktype': u'value'}],
                                       u'P1476': [
                                           {
                                               u'datatype': u'monolingualtext',
                                               u'datavalue': {
                                                   u'type': u'monolingualtext',
                                                   u'value': {
                                                       u'text': u"Douglas Adams, Author of 'Hitchhiker's Guide to the Galaxy,' Dies at 49",
                                                       u'language': u'en'}},
                                               u'property': u'P1476',
                                               u'snaktype': u'value'}],
                                       u'P407': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 1860}},
                                               u'property': u'P407',
                                               u'snaktype': u'value'}],
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.nytimes.com/books/01/05/13/daily/adams-obit.html'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}],
                                       u'P577': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002001-05-12T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P577',
                                               u'snaktype': u'value'}],
                                       u'P50': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 26724169}},
                                               u'property': u'P50',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'defb9736023b969ef081bca13cc69d80c1e11f46',
                                   u'snaks-order': [
                                       u'P854',
                                       u'P577',
                                       u'P123',
                                       u'P50',
                                       u'P407',
                                       u'P1476']},
                               {
                                   u'snaks': {
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.eskimo.com/~rkj/weekly/aa051701a.htm'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'de76f366926e923ef61d60535280c65570d26cc2',
                                   u'snaks-order': [
                                       u'P854']},
                               {
                                   u'snaks': {
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.waymarking.com/waymarks/WMH912_Douglas_Adams_Highgate_East_Cemetery_London_UK'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'027c2e3272694f0292b8ed6efa7d26e4b27fa458',
                                   u'snaks-order': [
                                       u'P854']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 159288}},
                                u'property': u'P20',
                                u'snaktype': u'value'},
                            u'id': u'q42$C0DE2013-54C0-48F9-AD90-8A235248D8C7',
                            u'rank': u'normal'})], u'P22': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-12-07T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P407': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1860}},
                                           u'property': u'P407',
                                           u'snaktype': u'value'}],
                                   u'P123': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1373513}},
                                           u'property': u'P123',
                                           u'snaktype': u'value'}],
                                   u'P1476': [
                                       {
                                           u'datatype': u'monolingualtext',
                                           u'datavalue': {
                                               u'type': u'monolingualtext',
                                               u'value': {
                                                   u'text': u'Douglas Adams',
                                                   u'language': u'en'}},
                                           u'property': u'P1476',
                                           u'snaktype': u'value'}],
                                   u'P854': [
                                       {
                                           u'datatype': u'url',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'http://www.nndb.com/people/731/000023662/'},
                                           u'property': u'P854',
                                           u'snaktype': u'value'}]},
                               u'hash': u'9177d75c6061e9e1ab149c0aa01bee5a90e07415',
                               u'snaks-order': [
                                   u'P854',
                                   u'P407',
                                   u'P123',
                                   u'P813',
                                   u'P1476']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 14623675}},
                                u'property': u'P22',
                                u'snaktype': u'value'},
                            u'id': u'q42$9ac7fb72-4402-8d72-f588-a170ca5e715c',
                            u'rank': u'normal'})], u'P866': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'douglas-adams'},
                                          u'property': u'P866',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$A29644ED-0377-4F88-8BA6-FAAB7DE8C7BA',
                            u'rank': u'normal'})], u'P3106': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'books/douglasadams'},
                                          u'property': u'P3106',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$d8ebbd62-4229-1e3b-6494-ca96246286e3',
                            u'rank': u'normal'})], u'P172': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 42406}},
                               u'property': u'P172', u'snaktype': u'value'},
                            u'id': u'Q42$32e3f411-4934-9c3b-6be0-c53bff07b544',
                            u'rank': u'normal'})], u'P646': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 15241312}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}],
                                   u'P577': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-10-28T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P577',
                                           u'snaktype': u'value'}]},
                               u'hash': u'2b00cb481cddcac7623114367489b5c194901c4a',
                               u'snaks-order': [
                                   u'P248',
                                   u'P577']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'/m/0282x'},
                                          u'property': u'P646',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$48D9C731-BDA8-45D6-B593-437CD10A51B4',
                            u'rank': u'normal'})], u'P950': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 54919}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'759b2a264fff886006b6f49c3ef2f1acbfd1cef0',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'XX1149955'},
                                          u'property': u'P950',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$856BE41B-546B-4381-B671-07DC17E1F677',
                            u'rank': u'normal'})], u'P800': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 5375741}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}]},
                               u'hash': u'355b56329b78db22be549dec34f2570ca61ca056',
                               u'snaks-order': [
                                   u'P248']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 25169}},
                                u'property': u'P800',
                                u'snaktype': u'value'},
                            u'id': u'Q42$FA73986E-3D1D-4CAB-B358-424B58544620',
                            u'rank': u'normal'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 902712}},
                               u'property': u'P800', u'snaktype': u'value'},
                            u'id': u'Q42$61ce65a9-454a-5b97-e014-496299c1c03a',
                            u'rank': u'normal'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 7758404}},
                               u'property': u'P800', u'snaktype': u'value'},
                            u'id': u'Q42$1c92fbe2-4743-0b27-e4ac-16320efe7864',
                            u'rank': u'normal'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 578895}},
                               u'property': u'P800', u'snaktype': u'value'},
                            u'id': u'Q42$e4b3a5e3-422e-593a-5b7c-3b12b5a4a0bb',
                            u'rank': u'normal'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 721}},
                               u'property': u'P800', u'snaktype': u'value'},
                            u'id': u'Q42$f338abf5-43cb-f5eb-1d32-9cdb73c084b9',
                            u'rank': u'normal'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 1042294}},
                               u'property': u'P800', u'snaktype': u'value'},
                            u'id': u'Q42$a7ebf426-476d-5cd9-b489-d849c8e0a82d',
                            u'rank': u'normal'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 187655}},
                               u'property': u'P800', u'snaktype': u'value'},
                            u'id': u'Q42$586d443e-43ef-fdc2-223f-c4ff6c2b6531',
                            u'rank': u'normal'})], u'P373': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'string',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'Douglas Adams'},
                                          u'property': u'P373',
                                          u'snaktype': u'value'},
                            u'id': u'q42$7EC4631F-FB22-4768-9B75-61875CD6C854',
                            u'rank': u'normal'})], u'P648': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'OL272947A'},
                                          u'property': u'P648',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$0BC410B8-8A0F-4658-90B0-BB2AE1D6AA3F',
                            u'rank': u'normal'})], u'P2626': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'159696'},
                                          u'property': u'P2626',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$5a41f776-4135-80b1-e3fe-43156047ecb8',
                            u'rank': u'normal'})], u'P1233': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 48183}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'9a24f7c0208b05d6be97077d855671d1dfdbc0dd',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'122'},
                                          u'property': u'P1233',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$9F55FA72-F9E5-41E4-A771-041EB1D59C28',
                            u'rank': u'normal'})], u'P570': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-12-07T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 15222191}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}],
                                   u'P268': [
                                       {
                                           u'datatype': u'external-id',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'11888092r'},
                                           u'property': u'P268',
                                           u'snaktype': u'value'}]},
                               u'hash': u'2f26d70b1e8b8cb53882b83197d1859e226da12d',
                               u'snaks-order': [
                                   u'P268',
                                   u'P248',
                                   u'P813']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 5375741}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'355b56329b78db22be549dec34f2570ca61ca056',
                                   u'snaks-order': [
                                       u'P248']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 36578}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002015-07-07T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P227': [
                                           {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'119033364'},
                                               u'property': u'P227',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'a02f3a77ddd343e6b88be25696b055f5131c3d64',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P227',
                                       u'P813']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 20666306}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002015-10-10T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://data.bnf.fr/ark:/12148/cb11888092r'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'55d23126bca9913374faf69ba8fbd21474a74421',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P813',
                                       u'P854']},
                               {
                                   u'snaks': {
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002016-01-11T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 1139587}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P2168': [
                                           {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'271209'},
                                               u'property': u'P2168',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'3bc90af5225a0b1248b3362e911577073e904e20',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P2168',
                                       u'P813']},
                               {
                                   u'snaks': {
                                       u'P3430': [
                                           {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'w65h7md1'},
                                               u'property': u'P3430',
                                               u'snaktype': u'value'}],
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 29861311}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002017-10-09T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P1810': [
                                           {
                                               u'datatype': u'string',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'Douglas Adams'},
                                               u'property': u'P1810',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'b460d7e5cae668698a5dfe74198df6632fe7231d',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P3430',
                                       u'P1810',
                                       u'P813']},
                               {
                                   u'snaks': {
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002017-10-28T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'https://www.theguardian.com/uk/2001/may/13/books.booksnews'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'e9a6c72ac1c0c2bc336ff672ddaf89ecd17fff68',
                                   u'snaks-order': [
                                       u'P854',
                                       u'P813']},
                               {
                                   u'snaks': {
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'https://www.wired.com/2012/03/i-miss-douglas-adams/'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'28af4e1131157dbbb2a5bbae189519a22e7d2b79',
                                   u'snaks-order': [
                                       u'P854']},
                               {
                                   u'snaks': {
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'https://www.locusmag.com/2001/News/News05a.html'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'268aeb992f54257af5a86d9d7f0d9627214b628f',
                                   u'snaks-order': [
                                       u'P854']},
                               {
                                   u'snaks': {
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.nytimes.com/2001/05/15/arts/douglas-adams-49-author-of-hitchhiker-s-guide-spoofs.html'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'5f3599922f5bee23969e91300f9eb461c7903a4b',
                                   u'snaks-order': [
                                       u'P854']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 2629164}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002017-10-09T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P1810': [
                                           {
                                               u'datatype': u'string',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'Douglas Adams'},
                                               u'property': u'P1810',
                                               u'snaktype': u'value'}],
                                       u'P1233': [
                                           {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'122'},
                                               u'property': u'P1233',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'162d5556b3c48733c6c27b4cddcb99bc86f4bf70',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P1233',
                                       u'P1810',
                                       u'P813']},
                               {
                                   u'snaks': {
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.screenonline.org.uk/people/id/1233876/index.html'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'bab32d323b6c92d91ff7d0c4707346012900761b',
                                   u'snaks-order': [
                                       u'P854']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 63056}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002017-10-09T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P535': [
                                           {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'22814'},
                                               u'property': u'P535',
                                               u'snaktype': u'value'}],
                                       u'P1810': [
                                           {
                                               u'datatype': u'string',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'Douglas Noel Adams'},
                                               u'property': u'P1810',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'0d9f07c561f61776c61a026473508c535af28267',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P535',
                                       u'P1810',
                                       u'P813']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 55790874}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002017-10-09T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P1810': [
                                           {
                                               u'datatype': u'string',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'Douglas ADAMS'},
                                               u'property': u'P1810',
                                               u'snaktype': u'value'}],
                                       u'P5570': [
                                           {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'143'},
                                               u'property': u'P5570',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'43394c447fd319b57ea4caf8bc370c86af979872',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P5570',
                                       u'P1810',
                                       u'P813']}],
                            u'mainsnak': {u'datatype': u'time',
                                          u'datavalue': {
                                              u'type': u'time',
                                              u'value': {u'after': 0,
                                                         u'precision': 11,
                                                         u'time': u'+00000002001-05-11T00:00:00Z',
                                                         u'timezone': 0,
                                                         u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                         u'before': 0}},
                                          u'property': u'P570',
                                          u'snaktype': u'value'},
                            u'id': u'q42$65EA9C32-B26C-469B-84FE-FC612B71D159',
                            u'rank': u'normal'})], u'P271': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'DA07517784'},
                                          u'property': u'P271',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$f69cd1df-4655-d1fa-5978-e3454415e57e',
                            u'rank': u'normal'})], u'P2188': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'45993'},
                                          u'property': u'P2188',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$5215183d-42ec-a3e5-1745-0abd519d026a',
                            u'rank': u'normal'})], u'P31': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 54919}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}],
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-12-07T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P214': [
                                       {
                                           u'datatype': u'external-id',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'113230702'},
                                           u'property': u'P214',
                                           u'snaktype': u'value'}]},
                               u'hash': u'2b369d0a4f1d4b801e734fe84a0b217e13dd2930',
                               u'snaks-order': [
                                   u'P248',
                                   u'P214',
                                   u'P813']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 20666306}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002015-10-10T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://data.bnf.fr/ark:/12148/cb11888092r'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'55d23126bca9913374faf69ba8fbd21474a74421',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P813',
                                       u'P854']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 5}},
                                u'property': u'P31',
                                u'snaktype': u'value'},
                            u'id': u'Q42$F078E5B3-F9A8-480E-B7AC-D97778CBBEF9',
                            u'rank': u'normal'})], u'P5570': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'143'},
                                          u'property': u'P5570',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$4F5DCE7C-3839-4642-AB6D-72C14C18D768',
                            u'rank': u'normal'})], u'P409': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 54919}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'759b2a264fff886006b6f49c3ef2f1acbfd1cef0',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'35163268'},
                                          u'property': u'P409',
                                          u'snaktype': u'value'},
                            u'id': u'q42$506fc7c8-439d-b77f-5041-8ca85659ad57',
                            u'rank': u'normal'})], u'P2734': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'AdamsDouglas'},
                                          u'property': u'P2734',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$6646C637-00DF-47E1-A845-CFCAB27A559D',
                            u'rank': u'normal'})], u'P569': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-12-07T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 15222191}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}],
                                   u'P268': [
                                       {
                                           u'datatype': u'external-id',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'11888092r'},
                                           u'property': u'P268',
                                           u'snaktype': u'value'}]},
                               u'hash': u'2f26d70b1e8b8cb53882b83197d1859e226da12d',
                               u'snaks-order': [
                                   u'P268',
                                   u'P248',
                                   u'P813']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 5375741}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'355b56329b78db22be549dec34f2570ca61ca056',
                                   u'snaks-order': [
                                       u'P248']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 36578}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002015-07-07T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P227': [
                                           {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'119033364'},
                                               u'property': u'P227',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'a02f3a77ddd343e6b88be25696b055f5131c3d64',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P227',
                                       u'P813']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 20666306}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002015-10-10T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://data.bnf.fr/ark:/12148/cb11888092r'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'55d23126bca9913374faf69ba8fbd21474a74421',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P813',
                                       u'P854']},
                               {
                                   u'snaks': {
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002016-01-11T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 1139587}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P2168': [
                                           {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'271209'},
                                               u'property': u'P2168',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'3bc90af5225a0b1248b3362e911577073e904e20',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P2168',
                                       u'P813']},
                               {
                                   u'snaks': {
                                       u'P3430': [
                                           {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'w65h7md1'},
                                               u'property': u'P3430',
                                               u'snaktype': u'value'}],
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 29861311}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002017-10-09T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P1810': [
                                           {
                                               u'datatype': u'string',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'Douglas Adams'},
                                               u'property': u'P1810',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'b460d7e5cae668698a5dfe74198df6632fe7231d',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P3430',
                                       u'P1810',
                                       u'P813']},
                               {
                                   u'snaks': {
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'https://www.wired.com/2012/03/i-miss-douglas-adams/'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'28af4e1131157dbbb2a5bbae189519a22e7d2b79',
                                   u'snaks-order': [
                                       u'P854']},
                               {
                                   u'snaks': {
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.independent.co.uk/arts-entertainment/books/news/google-doodle-celebrates-life-of-hitchhikers-guide-to-the-galaxy-author-douglas-adams-8528856.html'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'fcdddce2cc4540a613b0b8c0e5d2bbd2cc5704a9',
                                   u'snaks-order': [
                                       u'P854']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 2629164}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002017-10-09T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P1810': [
                                           {
                                               u'datatype': u'string',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'Douglas Adams'},
                                               u'property': u'P1810',
                                               u'snaktype': u'value'}],
                                       u'P1233': [
                                           {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'122'},
                                               u'property': u'P1233',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'162d5556b3c48733c6c27b4cddcb99bc86f4bf70',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P1233',
                                       u'P1810',
                                       u'P813']},
                               {
                                   u'snaks': {
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.screenonline.org.uk/people/id/1233876/index.html'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'bab32d323b6c92d91ff7d0c4707346012900761b',
                                   u'snaks-order': [
                                       u'P854']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 63056}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002017-10-09T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P535': [
                                           {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'22814'},
                                               u'property': u'P535',
                                               u'snaktype': u'value'}],
                                       u'P1810': [
                                           {
                                               u'datatype': u'string',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'Douglas Noel Adams'},
                                               u'property': u'P1810',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'0d9f07c561f61776c61a026473508c535af28267',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P535',
                                       u'P1810',
                                       u'P813']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 55790874}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002017-10-09T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P1810': [
                                           {
                                               u'datatype': u'string',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'Douglas ADAMS'},
                                               u'property': u'P1810',
                                               u'snaktype': u'value'}],
                                       u'P5570': [
                                           {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'143'},
                                               u'property': u'P5570',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'43394c447fd319b57ea4caf8bc370c86af979872',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P5570',
                                       u'P1810',
                                       u'P813']}],
                            u'mainsnak': {u'datatype': u'time',
                                          u'datavalue': {
                                              u'type': u'time',
                                              u'value': {u'after': 0,
                                                         u'precision': 11,
                                                         u'time': u'+00000001952-03-11T00:00:00Z',
                                                         u'timezone': 0,
                                                         u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                         u'before': 0}},
                                          u'property': u'P569',
                                          u'snaktype': u'value'},
                            u'id': u'q42$D8404CDA-25E4-4334-AF13-A3290BCD9C0F',
                            u'rank': u'normal'})], u'P5019': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'adams-douglas-noel'},
                                          u'property': u'P5019',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$d12f42dc-456c-4c5f-19ee-b4dda178e50f',
                            u'rank': u'normal'})], u'P3630': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'2627'},
                                          u'property': u'P3630',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$15011D96-BB02-4B8F-9728-8FF88A3A938D',
                            u'rank': u'normal'})], u'P40': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-12-07T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P407': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1860}},
                                           u'property': u'P407',
                                           u'snaktype': u'value'}],
                                   u'P123': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1373513}},
                                           u'property': u'P123',
                                           u'snaktype': u'value'}],
                                   u'P1476': [
                                       {
                                           u'datatype': u'monolingualtext',
                                           u'datavalue': {
                                               u'type': u'monolingualtext',
                                               u'value': {
                                                   u'text': u'Douglas Adams',
                                                   u'language': u'en'}},
                                           u'property': u'P1476',
                                           u'snaktype': u'value'}],
                                   u'P854': [
                                       {
                                           u'datatype': u'url',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'http://www.nndb.com/people/731/000023662/'},
                                           u'property': u'P854',
                                           u'snaktype': u'value'}]},
                               u'hash': u'9177d75c6061e9e1ab149c0aa01bee5a90e07415',
                               u'snaks-order': [
                                   u'P854',
                                   u'P407',
                                   u'P123',
                                   u'P813',
                                   u'P1476']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 14623683}},
                                u'property': u'P40',
                                u'snaktype': u'value'},
                            u'id': u'q42$70b600fa-4c0a-b3e6-9e19-1486e71c99fb',
                            u'rank': u'normal'})], u'P244': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1551807}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'14d2400e3b1d36332748dc330276f099eeaa8800',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'n80076765'},
                                          u'property': u'P244',
                                          u'snaktype': u'value'},
                            u'id': u'q42$2D472379-EC67-4C71-9700-0F9D551BF5E6',
                            u'rank': u'normal'})], u'P2949': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'Adams-32825'},
                                          u'property': u'P2949',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$A4E52439-57DF-4C31-902C-E995D78488FA',
                            u'rank': u'normal'})], u'P2607': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 14005}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}]},
                               u'hash': u'706208b3024200fd0a39ad499808dd0d98d74065',
                               u'snaks-order': [
                                   u'P248']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'307812da-da11-4ee5-a906-31e5ce9694bb'},
                                          u'property': u'P2607',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$52EA4A30-C798-4ED3-AEA0-A2FEB4B0FB95',
                            u'rank': u'normal'})], u'P3430': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'w65h7md1'},
                                          u'property': u'P3430',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$76AD35E4-F222-418A-A3AC-CF6472790811',
                            u'rank': u'normal'})], u'P1580': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'a1221374'},
                                          u'property': u'P1580',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$50941274-91AC-438C-9B7C-F0105F9CD20F',
                            u'rank': u'normal'})], u'P1670': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 54919}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'759b2a264fff886006b6f49c3ef2f1acbfd1cef0',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'0052C2705'},
                                          u'property': u'P1670',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$2370b5b3-487b-89dd-ad93-b023a2a86ac4',
                            u'rank': u'normal'})], u'P2600': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'6000000050650155828'},
                                          u'property': u'P2600',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$101c1875-4027-37aa-3a72-c202e42276ab',
                            u'rank': u'normal'})], u'P1695': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 54919}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}],
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002015-03-07T00:00:00Z',
                                                   u'timezone': 60,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P214': [
                                       {
                                           u'datatype': u'external-id',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'113230702'},
                                           u'property': u'P214',
                                           u'snaktype': u'value'}]},
                               u'hash': u'26c14416670af4da8614d9db92859f07401e3b88',
                               u'snaks-order': [
                                   u'P214',
                                   u'P248',
                                   u'P813']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'A11573065'},
                                          u'property': u'P1695',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$9B5EED2E-C3F5-4634-8B85-4D4CC6F15C93',
                            u'rank': u'normal'})], u'P1442': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'commonsMedia',
                               u'datavalue': {u'type': u'string',
                                              u'value': u"Douglas Adams' gravestone.jpg"},
                               u'property': u'P1442', u'snaktype': u'value'},
                            u'id': u'Q42$db1ba2ba-47b9-3650-e6c4-db683abf788c',
                            u'rank': u'normal'})], u'P2019': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'p279442'},
                                          u'property': u'P2019',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$b0322bc3-497a-8ef4-8eed-e4927b805d87',
                            u'rank': u'normal'})], u'P551': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"), {
                u'mainsnak': {u'datatype': u'wikibase-item',
                              u'datavalue': {u'type': u'wikibase-entityid',
                                             u'value': {u'entity-type': u'item',
                                                        u'numeric-id': 159288}},
                              u'property': u'P551',
                              u'snaktype': u'value'}, u'rank': u'deprecated',
                u'qualifiers': {u'P582': [
                    {u'datatype': u'time', u'datavalue': {u'type': u'time',
                                                          u'value': {
                                                              u'after': 0,
                                                              u'precision': 11,
                                                              u'time': u'+00000002001-05-11T00:00:00Z',
                                                              u'timezone': 0,
                                                              u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                              u'before': 0}},
                     u'property': u'P582',
                     u'hash': u'8798597f326000b4ffd9948d42771308bdb23133',
                     u'snaktype': u'value'}]}, u'qualifiers-order': [u'P582'],
                u'type': u'statement',
                u'id': u'Q42$E88EA363-419C-4FEA-BC63-F32669255382'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 84}},
                               u'property': u'P551', u'snaktype': u'value'},
                            u'id': u'Q42$9D3B2F23-36F4-4212-983B-DC15D47FC01E',
                            u'rank': u'normal'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"), {
                u'mainsnak': {u'datatype': u'wikibase-item',
                              u'datavalue': {u'type': u'wikibase-entityid',
                                             u'value': {u'entity-type': u'item',
                                                        u'numeric-id': 909993}},
                              u'property': u'P551',
                              u'snaktype': u'value'}, u'rank': u'normal',
                u'qualifiers': {u'P580': [
                    {u'datatype': u'time', u'datavalue': {u'type': u'time',
                                                          u'value': {
                                                              u'after': 0,
                                                              u'precision': 9,
                                                              u'time': u'+00000001957-00-00T00:00:00Z',
                                                              u'timezone': 0,
                                                              u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                              u'before': 0}},
                     u'property': u'P580',
                     u'hash': u'c786a8b39f62b37eb45745acf99302b5409f2e26',
                     u'snaktype': u'value'}]}, u'qualifiers-order': [u'P580'],
                u'type': u'statement',
                u'id': u'Q42$21492F88-0043-439D-B733-C7211D2283F7'})],
                u'P396': [
                    Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                   {u'type': u'statement', u'references': [{
                                       u'snaks': {
                                           u'P143': [
                                               {
                                                   u'datatype': u'wikibase-item',
                                                   u'datavalue': {
                                                       u'type': u'wikibase-entityid',
                                                       u'value': {
                                                           u'entity-type': u'item',
                                                           u'numeric-id': 54919}},
                                                   u'property': u'P143',
                                                   u'snaktype': u'value'}]},
                                       u'hash': u'759b2a264fff886006b6f49c3ef2f1acbfd1cef0',
                                       u'snaks-order': [
                                           u'P143']}],
                                    u'mainsnak': {u'datatype': u'external-id',
                                                  u'datavalue': {
                                                      u'type': u'string',
                                                      u'value': u'IT\\ICCU\\RAVV\\034417'},
                                                  u'property': u'P396',
                                                  u'snaktype': u'value'},
                                    u'id': u'Q42$b4c088b8-4bd9-c037-6b4e-7a0be3730947',
                                    u'rank': u'normal'})], u'P26': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"), {
                u'mainsnak': {u'datatype': u'wikibase-item',
                              u'datavalue': {u'type': u'wikibase-entityid',
                                             u'value': {u'entity-type': u'item',
                                                        u'numeric-id': 14623681}},
                              u'property': u'P26',
                              u'snaktype': u'value'}, u'rank': u'normal',
                u'qualifiers': {u'P580': [
                    {u'datatype': u'time', u'datavalue': {u'type': u'time',
                                                          u'value': {
                                                              u'after': 0,
                                                              u'precision': 11,
                                                              u'time': u'+00000001991-11-25T00:00:00Z',
                                                              u'timezone': 0,
                                                              u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                              u'before': 0}},
                     u'property': u'P580',
                     u'hash': u'cccb5ca124ec4121900c8beb41b777148829fa49',
                     u'snaktype': u'value'}], u'P582': [{u'datatype': u'time',
                                                         u'datavalue': {
                                                             u'type': u'time',
                                                             u'value': {
                                                                 u'after': 0,
                                                                 u'precision': 11,
                                                                 u'time': u'+00000002001-05-11T00:00:00Z',
                                                                 u'timezone': 0,
                                                                 u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                                 u'before': 0}},
                                                         u'property': u'P582',
                                                         u'hash': u'8798597f326000b4ffd9948d42771308bdb23133',
                                                         u'snaktype': u'value'}]},
                u'qualifiers-order': [u'P580', u'P582'],
                u'references': [{u'snaks': {u'P813': [
                    {u'datatype': u'time', u'datavalue': {u'type': u'time',
                                                          u'value': {
                                                              u'after': 0,
                                                              u'precision': 11,
                                                              u'time': u'+00000002013-12-07T00:00:00Z',
                                                              u'timezone': 0,
                                                              u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                              u'before': 0}},
                     u'property': u'P813', u'snaktype': u'value'}], u'P407': [
                    {u'datatype': u'wikibase-item',
                     u'datavalue': {u'type': u'wikibase-entityid',
                                    u'value': {u'entity-type': u'item',
                                               u'numeric-id': 1860}},
                     u'property': u'P407', u'snaktype': u'value'}], u'P123': [
                    {u'datatype': u'wikibase-item',
                     u'datavalue': {u'type': u'wikibase-entityid',
                                    u'value': {u'entity-type': u'item',
                                               u'numeric-id': 1373513}},
                     u'property': u'P123', u'snaktype': u'value'}], u'P1476': [
                    {u'datatype': u'monolingualtext',
                     u'datavalue': {u'type': u'monolingualtext',
                                    u'value': {
                                        u'text': u'Douglas Adams',
                                        u'language': u'en'}},
                     u'property': u'P1476', u'snaktype': u'value'}],
                    u'P854': [{u'datatype': u'url',
                               u'datavalue': {
                                   u'type': u'string',
                                   u'value': u'http://www.nndb.com/people/731/000023662/'},
                               u'property': u'P854',
                               u'snaktype': u'value'}]},
                    u'hash': u'9177d75c6061e9e1ab149c0aa01bee5a90e07415',
                    u'snaks-order': [u'P854',
                                     u'P407',
                                     u'P123',
                                     u'P813',
                                     u'P1476']}],
                u'type': u'statement',
                u'id': u'q42$b88670f8-456b-3ecb-cf3d-2bca2cf7371e'})],
                u'P5408': [Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                          {u'type': u'statement',
                                           u'mainsnak': {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'a/douglas-adams'},
                                               u'property': u'P5408',
                                               u'snaktype': u'value'},
                                           u'id': u'Q42$37B09D07-EE5D-4944-80B0-27BB6D41D87F',
                                           u'rank': u'normal'})], u'P734': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 36578}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}],
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002015-07-07T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P227': [
                                       {
                                           u'datatype': u'external-id',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'119033364'},
                                           u'property': u'P227',
                                           u'snaktype': u'value'}]},
                               u'hash': u'a02f3a77ddd343e6b88be25696b055f5131c3d64',
                               u'snaks-order': [
                                   u'P248',
                                   u'P227',
                                   u'P813']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 351735}},
                                u'property': u'P734',
                                u'snaktype': u'value'},
                            u'id': u'Q42$24df999a-4629-c679-e1f0-199bcefabbf3',
                            u'rank': u'normal'})],
        u'P735': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"), {
                u'mainsnak': {u'datatype': u'wikibase-item',
                              u'datavalue': {u'type': u'wikibase-entityid',
                                             u'value': {u'entity-type': u'item',
                                                        u'numeric-id': 463035}},
                              u'property': u'P735',
                              u'snaktype': u'value'}, u'rank': u'preferred',
                u'qualifiers': {u'P1545': [
                    {u'datatype': u'string',
                     u'datavalue': {u'type': u'string', u'value': u'1'},
                     u'property': u'P1545',
                     u'hash': u'2a1ced1dca90648ea7e306acbadd74fc81a10722',
                     u'snaktype': u'value'}]}, u'qualifiers-order': [u'P1545'],
                u'references': [{
                    u'snaks': {
                        u'P248': [
                            {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 36578}},
                                u'property': u'P248',
                                u'snaktype': u'value'}],
                        u'P813': [
                            {
                                u'datatype': u'time',
                                u'datavalue': {
                                    u'type': u'time',
                                    u'value': {
                                        u'after': 0,
                                        u'precision': 11,
                                        u'time': u'+00000002015-07-07T00:00:00Z',
                                        u'timezone': 0,
                                        u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                        u'before': 0}},
                                u'property': u'P813',
                                u'snaktype': u'value'}],
                        u'P227': [
                            {
                                u'datatype': u'external-id',
                                u'datavalue': {
                                    u'type': u'string',
                                    u'value': u'119033364'},
                                u'property': u'P227',
                                u'snaktype': u'value'}]},
                    u'hash': u'a02f3a77ddd343e6b88be25696b055f5131c3d64',
                    u'snaks-order': [
                        u'P248',
                        u'P227',
                        u'P813']},
                    {
                        u'snaks': {
                            u'P143': [
                                {
                                    u'datatype': u'wikibase-item',
                                    u'datavalue': {
                                        u'type': u'wikibase-entityid',
                                        u'value': {
                                            u'entity-type': u'item',
                                            u'numeric-id': 328}},
                                    u'property': u'P143',
                                    u'snaktype': u'value'}]},
                        u'hash': u'fa278ebfc458360e5aed63d5058cca83c46134f1',
                        u'snaks-order': [
                            u'P143']}],
                u'type': u'statement',
                u'id': u'Q42$1d7d0ea9-412f-8b5b-ba8d-405ab9ecf026'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"), {
                u'mainsnak': {u'datatype': u'wikibase-item',
                              u'datavalue': {u'type': u'wikibase-entityid',
                                             u'value': {u'entity-type': u'item',
                                                        u'numeric-id': 19688263}},
                              u'property': u'P735',
                              u'snaktype': u'value'}, u'rank': u'normal',
                u'qualifiers': {u'P1545': [
                    {u'datatype': u'string',
                     u'datavalue': {u'type': u'string', u'value': u'2'},
                     u'property': u'P1545',
                     u'hash': u'7241753c62a310cf84895620ea82250dcea65835',
                     u'snaktype': u'value'}]}, u'qualifiers-order': [u'P1545'],
                u'references': [{
                    u'snaks': {
                        u'P248': [
                            {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 36578}},
                                u'property': u'P248',
                                u'snaktype': u'value'}],
                        u'P813': [
                            {
                                u'datatype': u'time',
                                u'datavalue': {
                                    u'type': u'time',
                                    u'value': {
                                        u'after': 0,
                                        u'precision': 11,
                                        u'time': u'+00000002015-07-07T00:00:00Z',
                                        u'timezone': 0,
                                        u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                        u'before': 0}},
                                u'property': u'P813',
                                u'snaktype': u'value'}],
                        u'P227': [
                            {
                                u'datatype': u'external-id',
                                u'datavalue': {
                                    u'type': u'string',
                                    u'value': u'119033364'},
                                u'property': u'P227',
                                u'snaktype': u'value'}]},
                    u'hash': u'a02f3a77ddd343e6b88be25696b055f5131c3d64',
                    u'snaks-order': [
                        u'P248',
                        u'P227',
                        u'P813']}],
                u'type': u'statement',
                u'id': u'Q42$1e106952-4b58-6067-c831-8593ce3d70f5'})],
                u'P1477': [Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                          {u'type': u'statement',
                                           u'references': [{
                                               u'snaks': {
                                                   u'P123': [
                                                       {
                                                           u'datatype': u'wikibase-item',
                                                           u'datavalue': {
                                                               u'type': u'wikibase-entityid',
                                                               u'value': {
                                                                   u'entity-type': u'item',
                                                                   u'numeric-id': 11148}},
                                                           u'property': u'P123',
                                                           u'snaktype': u'value'}],
                                                   u'P1476': [
                                                       {
                                                           u'datatype': u'monolingualtext',
                                                           u'datavalue': {
                                                               u'type': u'monolingualtext',
                                                               u'value': {
                                                                   u'text': u'Obituary: Douglas Adams',
                                                                   u'language': u'en'}},
                                                           u'property': u'P1476',
                                                           u'snaktype': u'value'}],
                                                   u'P407': [
                                                       {
                                                           u'datatype': u'wikibase-item',
                                                           u'datavalue': {
                                                               u'type': u'wikibase-entityid',
                                                               u'value': {
                                                                   u'entity-type': u'item',
                                                                   u'numeric-id': 1860}},
                                                           u'property': u'P407',
                                                           u'snaktype': u'value'}],
                                                   u'P813': [
                                                       {
                                                           u'datatype': u'time',
                                                           u'datavalue': {
                                                               u'type': u'time',
                                                               u'value': {
                                                                   u'after': 0,
                                                                   u'precision': 11,
                                                                   u'time': u'+00000002013-12-07T00:00:00Z',
                                                                   u'timezone': 0,
                                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                                   u'before': 0}},
                                                           u'property': u'P813',
                                                           u'snaktype': u'value'}],
                                                   u'P854': [
                                                       {
                                                           u'datatype': u'url',
                                                           u'datavalue': {
                                                               u'type': u'string',
                                                               u'value': u'http://www.theguardian.com/news/2001/may/15/guardianobituaries.books'},
                                                           u'property': u'P854',
                                                           u'snaktype': u'value'}],
                                                   u'P577': [
                                                       {
                                                           u'datatype': u'time',
                                                           u'datavalue': {
                                                               u'type': u'time',
                                                               u'value': {
                                                                   u'after': 0,
                                                                   u'precision': 11,
                                                                   u'time': u'+00000002001-05-15T00:00:00Z',
                                                                   u'timezone': 0,
                                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                                   u'before': 0}},
                                                           u'property': u'P577',
                                                           u'snaktype': u'value'}],
                                                   u'P50': [
                                                       {
                                                           u'datatype': u'wikibase-item',
                                                           u'datavalue': {
                                                               u'type': u'wikibase-entityid',
                                                               u'value': {
                                                                   u'entity-type': u'item',
                                                                   u'numeric-id': 18145749}},
                                                           u'property': u'P50',
                                                           u'snaktype': u'value'}]},
                                               u'hash': u'67b9be98c538c1186a117125edcb254f4f351812',
                                               u'snaks-order': [
                                                   u'P1476',
                                                   u'P123',
                                                   u'P577',
                                                   u'P407',
                                                   u'P854',
                                                   u'P813',
                                                   u'P50']}],
                                           u'mainsnak': {
                                               u'datatype': u'monolingualtext',
                                               u'datavalue': {
                                                   u'type': u'monolingualtext',
                                                   u'value': {
                                                       u'text': u'Douglas Noel Adams',
                                                       u'language': u'en-gb'}},
                                               u'property': u'P1477',
                                               u'snaktype': u'value'},
                                           u'id': u'Q42$45220d20-40d2-299e-f4cc-f6cce89f2f42',
                                           u'rank': u'normal'})], u'P1368': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 54919}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'759b2a264fff886006b6f49c3ef2f1acbfd1cef0',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'000057405'},
                                          u'property': u'P1368',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$11725e9f-4f81-e0fd-b00a-b885fe7a75ac',
                            u'rank': u'normal'})], u'P140': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P407': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1860}},
                                           u'property': u'P407',
                                           u'snaktype': u'value'}],
                                   u'P813': [
                                       {
                                           u'datatype': u'time',
                                           u'datavalue': {
                                               u'type': u'time',
                                               u'value': {
                                                   u'after': 0,
                                                   u'precision': 11,
                                                   u'time': u'+00000002013-12-07T00:00:00Z',
                                                   u'timezone': 0,
                                                   u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                   u'before': 0}},
                                           u'property': u'P813',
                                           u'snaktype': u'value'}],
                                   u'P1476': [
                                       {
                                           u'datatype': u'monolingualtext',
                                           u'datavalue': {
                                               u'type': u'monolingualtext',
                                               u'value': {
                                                   u'text': u'Douglas Adams and God. Portrait of a radical atheist',
                                                   u'language': u'en'}},
                                           u'property': u'P1476',
                                           u'snaktype': u'value'}],
                                   u'P854': [
                                       {
                                           u'datatype': u'url',
                                           u'datavalue': {
                                               u'type': u'string',
                                               u'value': u'http://www.douglasadams.eu/douglas-adams-and-god-portrait-of-a-radical-atheist/'},
                                           u'property': u'P854',
                                           u'snaktype': u'value'}]},
                               u'hash': u'ba8b8e4808de217c0a0d4a1276a78297b01b1ea1',
                               u'snaks-order': [
                                   u'P854',
                                   u'P813',
                                   u'P1476',
                                   u'P407']},
                               {
                                   u'snaks': {
                                       u'P123': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 15290435}},
                                               u'property': u'P123',
                                               u'snaktype': u'value'}],
                                       u'P1476': [
                                           {
                                               u'datatype': u'monolingualtext',
                                               u'datavalue': {
                                                   u'type': u'monolingualtext',
                                                   u'value': {
                                                       u'text': u"Douglas Adams' Interview with American Atheists",
                                                       u'language': u'en'}},
                                               u'property': u'P1476',
                                               u'snaktype': u'value'}],
                                       u'P407': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 1860}},
                                               u'property': u'P407',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002013-12-07T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.nichirenbuddhist.org/Religion/Atheists/DouglasAdams/Interview-American-Atheists.html'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}],
                                       u'P577': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 9,
                                                       u'time': u'+00000002002-01-01T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P577',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'6f594ed7391250cb94bc94aaa94d855184a7bdf5',
                                   u'snaks-order': [
                                       u'P854',
                                       u'P123',
                                       u'P577',
                                       u'P813',
                                       u'P1476',
                                       u'P407']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 7066}},
                                u'property': u'P140',
                                u'snaktype': u'value'},
                            u'id': u'q42$8419C20C-8EF8-4EC0-80D6-AF1CA55E7557',
                            u'rank': u'normal'})], u'P1207': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 54919}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'759b2a264fff886006b6f49c3ef2f1acbfd1cef0',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'n94004172'},
                                          u'property': u'P1207',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$00ddd8cf-48fa-609f-dd4e-977e9672c96f',
                            u'rank': u'normal'})], u'P3417': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'Douglas-Adams-4'},
                                          u'property': u'P3417',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$edea25d2-4736-b539-ec8d-d3f82e1f7100',
                            u'rank': u'normal'})], u'P4431': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'douglas-adams-61st-birthday'},
                                          u'property': u'P4431',
                                          u'snaktype': u'value'},
                            u'rank': u'normal', u'qualifiers': {
                               u'P585': [{u'datatype': u'time',
                                          u'datavalue': {u'type': u'time',
                                                         u'value': {u'after': 0,
                                                                    u'precision': 11,
                                                                    u'time': u'+00000002013-03-11T00:00:00Z',
                                                                    u'timezone': 0,
                                                                    u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                                    u'before': 0}},
                                          u'property': u'P585',
                                          u'hash': u'52ee0260174795772f9cfbfa8ec3b7561ef4e7bc',
                                          u'snaktype': u'value'}]},
                            u'qualifiers-order': [u'P585'],
                            u'references': [{u'snaks': {u'P854': [
                                {u'datatype': u'url',
                                 u'datavalue': {u'type': u'string',
                                                u'value': u'http://www.google.com/doodles/douglas-adams-61st-birthday'},
                                 u'property': u'P854',
                                 u'snaktype': u'value'}]},
                                u'hash': u'a403d90550be4608a47c62ec6d9fd69e0c707d1c',
                                u'snaks-order': [
                                    u'P854']}],
                            u'type': u'statement',
                            u'id': u'Q42$520b13d1-47df-2d1c-f56d-7106f383a3b6'})],
                u'P5337': [Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                          {u'type': u'statement',
                                           u'mainsnak': {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'CAAqJQgKIh9DQkFTRVFvSUwyMHZNREk0TW5nU0JXVnVMVWRDS0FBUAE'},
                                               u'property': u'P5337',
                                               u'snaktype': u'value'},
                                           u'id': u'Q42$966e692e-4516-de45-356c-7e098273a79a',
                                           u'rank': u'normal'})], u'P69': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"), {
                u'mainsnak': {u'datatype': u'wikibase-item',
                              u'datavalue': {u'type': u'wikibase-entityid',
                                             u'value': {u'entity-type': u'item',
                                                        u'numeric-id': 691283}},
                              u'property': u'P69',
                              u'snaktype': u'value'}, u'rank': u'normal',
                u'qualifiers': {u'P580': [
                    {u'datatype': u'time', u'datavalue': {u'type': u'time',
                                                          u'value': {
                                                              u'after': 0,
                                                              u'precision': 9,
                                                              u'time': u'+00000001971-00-00T00:00:00Z',
                                                              u'timezone': 0,
                                                              u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                              u'before': 0}},
                     u'property': u'P580',
                     u'hash': u'847c4c912d3781dc83eabd7135d6403c473c0daf',
                     u'snaktype': u'value'}], u'P582': [{u'datatype': u'time',
                                                         u'datavalue': {
                                                             u'type': u'time',
                                                             u'value': {
                                                                 u'after': 0,
                                                                 u'precision': 9,
                                                                 u'time': u'+00000001974-01-01T00:00:00Z',
                                                                 u'timezone': 0,
                                                                 u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                                 u'before': 0}},
                                                         u'property': u'P582',
                                                         u'hash': u'cf63122733bae275108bbf5d043d46669f782697',
                                                         u'snaktype': u'value'}],
                    u'P512': [
                        {u'datatype': u'wikibase-item',
                         u'datavalue': {u'type': u'wikibase-entityid',
                                        u'value': {u'entity-type': u'item',
                                                   u'numeric-id': 1765120}},
                         u'property': u'P512',
                         u'hash': u'e1bbba02ae21a15bcef937d017c8142e5cf73a88',
                         u'snaktype': u'value'}],
                    u'P812': [{u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 186579}},
                               u'property': u'P812',
                               u'hash': u'e03f82fd83e940fdf0020ded271f0edf11977d72',
                               u'snaktype': u'value'}]},
                u'qualifiers-order': [u'P582', u'P812', u'P512', u'P580'],
                u'references': [{u'snaks': {
                    u'P248': [{u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 5375741}},
                               u'property': u'P248',
                               u'snaktype': u'value'}]},
                    u'hash': u'355b56329b78db22be549dec34f2570ca61ca056',
                    u'snaks-order': [
                        u'P248']},
                    {u'snaks': {
                        u'P813': [
                            {
                                u'datatype': u'time',
                                u'datavalue': {
                                    u'type': u'time',
                                    u'value': {
                                        u'after': 0,
                                        u'precision': 11,
                                        u'time': u'+00000002013-12-07T00:00:00Z',
                                        u'timezone': 0,
                                        u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                        u'before': 0}},
                                u'property': u'P813',
                                u'snaktype': u'value'}],
                        u'P407': [
                            {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 1860}},
                                u'property': u'P407',
                                u'snaktype': u'value'}],
                        u'P123': [
                            {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 1373513}},
                                u'property': u'P123',
                                u'snaktype': u'value'}],
                        u'P1476': [
                            {
                                u'datatype': u'monolingualtext',
                                u'datavalue': {
                                    u'type': u'monolingualtext',
                                    u'value': {
                                        u'text': u'Douglas Adams',
                                        u'language': u'en'}},
                                u'property': u'P1476',
                                u'snaktype': u'value'}],
                        u'P854': [
                            {
                                u'datatype': u'url',
                                u'datavalue': {
                                    u'type': u'string',
                                    u'value': u'http://www.nndb.com/people/731/000023662/'},
                                u'property': u'P854',
                                u'snaktype': u'value'}]},
                        u'hash': u'9177d75c6061e9e1ab149c0aa01bee5a90e07415',
                        u'snaks-order': [
                            u'P854',
                            u'P407',
                            u'P123',
                            u'P813',
                            u'P1476']}],
                u'type': u'statement',
                u'id': u'q42$0E9C4724-C954-4698-84A7-5CE0D296A6F2'}),
            Claim.fromJSON(DataSite("wikidata", "wikidata"), {
                u'mainsnak': {u'datatype': u'wikibase-item',
                              u'datavalue': {u'type': u'wikibase-entityid',
                                             u'value': {u'entity-type': u'item',
                                                        u'numeric-id': 4961791}},
                              u'property': u'P69',
                              u'snaktype': u'value'}, u'rank': u'normal',
                u'qualifiers': {u'P580': [
                    {u'datatype': u'time', u'datavalue': {u'type': u'time',
                                                          u'value': {
                                                              u'after': 0,
                                                              u'precision': 9,
                                                              u'time': u'+00000001959-00-00T00:00:00Z',
                                                              u'timezone': 0,
                                                              u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                              u'before': 0}},
                     u'property': u'P580',
                     u'hash': u'923f84fcbf398253e1ef1a8a13f1da430b87d7bb',
                     u'snaktype': u'value'}], u'P582': [{u'datatype': u'time',
                                                         u'datavalue': {
                                                             u'type': u'time',
                                                             u'value': {
                                                                 u'after': 0,
                                                                 u'precision': 9,
                                                                 u'time': u'+00000001970-00-00T00:00:00Z',
                                                                 u'timezone': 0,
                                                                 u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                                 u'before': 0}},
                                                         u'property': u'P582',
                                                         u'hash': u'5c5b90187b61a0af83711c9495e5529940747577',
                                                         u'snaktype': u'value'}]},
                u'qualifiers-order': [u'P582', u'P580'], u'type': u'statement',
                u'id': u'Q42$32490F12-D9B5-498A-91A8-839F9149F600'})],
                u'P227': [
                    Claim.fromJSON(DataSite("wikidata", "wikidata"),
                                   {u'type': u'statement', u'references': [{
                                       u'snaks': {
                                           u'P143': [
                                               {
                                                   u'datatype': u'wikibase-item',
                                                   u'datavalue': {
                                                       u'type': u'wikibase-entityid',
                                                       u'value': {
                                                           u'entity-type': u'item',
                                                           u'numeric-id': 1551807}},
                                                   u'property': u'P143',
                                                   u'snaktype': u'value'}]},
                                       u'hash': u'14d2400e3b1d36332748dc330276f099eeaa8800',
                                       u'snaks-order': [
                                           u'P143']},
                                       {
                                           u'snaks': {
                                               u'P143': [
                                                   {
                                                       u'datatype': u'wikibase-item',
                                                       u'datavalue': {
                                                           u'type': u'wikibase-entityid',
                                                           u'value': {
                                                               u'entity-type': u'item',
                                                               u'numeric-id': 1419226}},
                                                       u'property': u'P143',
                                                       u'snaktype': u'value'}]},
                                           u'hash': u'dd3ff7346d2dbe78013c48629bb46c53fdb951b2',
                                           u'snaks-order': [
                                               u'P143']}],
                                    u'mainsnak': {u'datatype': u'external-id',
                                                  u'datavalue': {
                                                      u'type': u'string',
                                                      u'value': u'119033364'},
                                                  u'property': u'P227',
                                                  u'snaktype': u'value'},
                                    u'id': u'q42$8AA8CCC1-86CE-4C66-88FC-267621A81EA0',
                                    u'rank': u'normal'})], u'P949': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'000163846'},
                                          u'property': u'P949',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$2D50AE02-2BD8-4F82-9DFD-B3166DEFDEC1',
                            u'rank': u'normal'})], u'P947': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P143': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 1048694}},
                                           u'property': u'P143',
                                           u'snaktype': u'value'}]},
                               u'hash': u'e13240e63b2eb76c57e8e26db9d04e0065d1d336',
                               u'snaks-order': [
                                   u'P143']}],
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'000002833'},
                                          u'property': u'P947',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$cf5f61ec-440d-60d4-7847-e95f75171f2f',
                            u'rank': u'normal'})], u'P1617': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement',
                            u'mainsnak': {u'datatype': u'external-id',
                                          u'datavalue': {
                                              u'type': u'string',
                                              u'value': u'aa075cb6-75bf-46d8-b0bf-9751d6c04c93'},
                                          u'property': u'P1617',
                                          u'snaktype': u'value'},
                            u'id': u'Q42$545d5c9a-4bde-ee8b-089f-1a11ba699301',
                            u'rank': u'normal'})], u'P19': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'references': [{
                               u'snaks': {
                                   u'P248': [
                                       {
                                           u'datatype': u'wikibase-item',
                                           u'datavalue': {
                                               u'type': u'wikibase-entityid',
                                               u'value': {
                                                   u'entity-type': u'item',
                                                   u'numeric-id': 5375741}},
                                           u'property': u'P248',
                                           u'snaktype': u'value'}]},
                               u'hash': u'355b56329b78db22be549dec34f2570ca61ca056',
                               u'snaks-order': [
                                   u'P248']},
                               {
                                   u'snaks': {
                                       u'P1476': [
                                           {
                                               u'datatype': u'monolingualtext',
                                               u'datavalue': {
                                                   u'type': u'monolingualtext',
                                                   u'value': {
                                                       u'text': u'Obituary: Douglas Adams',
                                                       u'language': u'en'}},
                                               u'property': u'P1476',
                                               u'snaktype': u'value'}],
                                       u'P407': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 1860}},
                                               u'property': u'P407',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002013-12-07T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P1433': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 11148}},
                                               u'property': u'P1433',
                                               u'snaktype': u'value'}],
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.theguardian.com/news/2001/may/15/guardianobituaries.books'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}],
                                       u'P577': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002001-05-15T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P577',
                                               u'snaktype': u'value'}],
                                       u'P50': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 18145749}},
                                               u'property': u'P50',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'3f4d26cf841e20630c969afc0e48e5e3ef0c5a49',
                                   u'snaks-order': [
                                       u'P854',
                                       u'P577',
                                       u'P813',
                                       u'P1433',
                                       u'P50',
                                       u'P1476',
                                       u'P407']},
                               {
                                   u'snaks': {
                                       u'P123': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 192621}},
                                               u'property': u'P123',
                                               u'snaktype': u'value'}],
                                       u'P1476': [
                                           {
                                               u'datatype': u'monolingualtext',
                                               u'datavalue': {
                                                   u'type': u'monolingualtext',
                                                   u'value': {
                                                       u'text': u"Hitch Hiker's Guide author Douglas Adams dies aged 49",
                                                       u'language': u'en'}},
                                               u'property': u'P1476',
                                               u'snaktype': u'value'}],
                                       u'P407': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 1860}},
                                               u'property': u'P407',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002015-01-03T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P854': [
                                           {
                                               u'datatype': u'url',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'http://www.telegraph.co.uk/news/uknews/1330072/Hitch-Hikers-Guide-author-Douglas-Adams-dies-aged-49.html'},
                                               u'property': u'P854',
                                               u'snaktype': u'value'}],
                                       u'P577': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002001-05-13T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P577',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'51a934797fd7f7d3ee91d4d541356d4c5974075b',
                                   u'snaks-order': [
                                       u'P1476',
                                       u'P577',
                                       u'P123',
                                       u'P407',
                                       u'P854',
                                       u'P813']},
                               {
                                   u'snaks': {
                                       u'P248': [
                                           {
                                               u'datatype': u'wikibase-item',
                                               u'datavalue': {
                                                   u'type': u'wikibase-entityid',
                                                   u'value': {
                                                       u'entity-type': u'item',
                                                       u'numeric-id': 36578}},
                                               u'property': u'P248',
                                               u'snaktype': u'value'}],
                                       u'P813': [
                                           {
                                               u'datatype': u'time',
                                               u'datavalue': {
                                                   u'type': u'time',
                                                   u'value': {
                                                       u'after': 0,
                                                       u'precision': 11,
                                                       u'time': u'+00000002015-07-07T00:00:00Z',
                                                       u'timezone': 0,
                                                       u'calendarmodel': u'http://www.wikidata.org/entity/Q1985727',
                                                       u'before': 0}},
                                               u'property': u'P813',
                                               u'snaktype': u'value'}],
                                       u'P227': [
                                           {
                                               u'datatype': u'external-id',
                                               u'datavalue': {
                                                   u'type': u'string',
                                                   u'value': u'119033364'},
                                               u'property': u'P227',
                                               u'snaktype': u'value'}]},
                                   u'hash': u'a02f3a77ddd343e6b88be25696b055f5131c3d64',
                                   u'snaks-order': [
                                       u'P248',
                                       u'P227',
                                       u'P813']}],
                            u'mainsnak': {
                                u'datatype': u'wikibase-item',
                                u'datavalue': {
                                    u'type': u'wikibase-entityid',
                                    u'value': {
                                        u'entity-type': u'item',
                                        u'numeric-id': 350}},
                                u'property': u'P19',
                                u'snaktype': u'value'},
                            u'id': u'q42$3D284234-52BC-4DA3-83A3-7C39F84BA518',
                            u'rank': u'normal'})], u'P1196': [
            Claim.fromJSON(DataSite("wikidata", "wikidata"),
                           {u'type': u'statement', u'mainsnak': {
                               u'datatype': u'wikibase-item',
                               u'datavalue': {u'type': u'wikibase-entityid',
                                              u'value': {
                                                  u'entity-type': u'item',
                                                  u'numeric-id': 3739104}},
                               u'property': u'P1196', u'snaktype': u'value'},
                            u'id': u'Q42$2CF6704F-527F-46F7-9A89-41FC0C9DF492',
                            u'rank': u'normal'})]},
    u'labels': {u'sco': u'Douglas Adams', u'scn': u'Douglas Adams',
                u'sr-ec': u'\u0414\u0430\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                u'wuu': u'\u9053\u683c\u62c9\u65af\xb7\u4e9a\u5f53\u65af',
                u'tcy': u'\u0ca1\u0cbe\u0c97\u0ccd\u0cb2\u0cb8\u0ccd \u0c86\u0ca1\u0cae\u0ccd\u0cb8\u0ccd',
                u'sr-el': u'Daglas Adams',
                u'gu': u'\u0aa1\u0a97\u0acd\u0ab2\u0abe\u0ab8 \u0a8f\u0aa1\u0aae\u0acd\u0ab8',
                u'zh-hk': u'\u9053\u683c\u62c9\u65af\xb7\u4e9e\u7576\u65af',
                u'gd': u'Douglas Adams', u'pt-br': u'Douglas Adams',
                u'ga': u'Douglas Adams', u'gl': u'Douglas Adams',
                u'lb': u'Douglas Adams',
                u'vep': u'Adams Duglas', u'la': u'Duglassius Adams',
                u'tr': u'Douglas Adams', u'li': u'Douglas Adams',
                u'lv': u'Duglass Adamss',
                u'tl': u'Douglas Adams', u'vec': u'Douglas Adams',
                u'th': u'\u0e14\u0e31\u0e4a\u0e01\u0e25\u0e32\u0e2a \u0e2d\u0e14\u0e31\u0e21\u0e2a\u0e4c',
                u'te': u'\u0c21\u0c17\u0c4d\u0c32\u0c38\u0c4d \u0c06\u0c21\u0c2e\u0c4d\u0c38\u0c4d',
                u'pcd': u'Douglas Adams',
                u'ta': u'\u0b9f\u0b95\u0bcd\u0bb3\u0bb8\u0bcd \u0b86\u0b9f\u0bae\u0bcd\u0bb8\u0bcd',
                u'de': u'Douglas Adams', u'da': u'Douglas Adams',
                u'rwr': u'\u0921\u0917\u094d\u0932\u0938 \u0905\u200d\u0921\u092e\u094d\u0938',
                u'vls': u'Douglas Adams', u'is': u'Douglas Adams',
                u'bar': u'Douglas Adams',
                u'zh-hans': u'\u9053\u683c\u62c9\u65af\xb7\u4e9a\u5f53\u65af',
                u'de-ch': u'Douglas Adams',
                u'zh-hant': u'\u9053\u683c\u62c9\u65af\xb7\u4e9e\u7576\u65af',
                u'el': u'\u039d\u03c4\u03ac\u03b3\u03ba\u03bb\u03b1\u03c2 \u0386\u03bd\u03c4\u03b1\u03bc\u03c2',
                u'eo': u'Douglas Adams', u'en': u'Douglas Adams',
                u'zh': u'\u9053\u683c\u62c9\u65af\xb7\u4e9a\u5f53\u65af',
                u'pms': u'Douglas Adams',
                u'arz': u'\u062f\u0648\u062c\u0644\u0627\u0633 \u0627\u062f\u0627\u0645\u0632',
                u'lfn': u'Douglas Adams', u'eu': u'Douglas Adams',
                u'et': u'Douglas Adams',
                u'wo': u'Douglas Adams', u'es': u'Douglas Adams',
                u'en-gb': u'Douglas Adams',
                u'ru': u'\u0414\u0443\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                u'zh-cn': u'\u9053\u683c\u62c9\u65af\xb7\u4e9a\u5f53\u65af',
                u'si': u'\u0da9\u0d9c\u0dca\u0dbd\u0dc3\u0dca \u0d87\u0da9\u0db8\u0dca\u0dc3\u0dca',
                u'rm': u'Douglas Adams', u'ro': u'Douglas Adams',
                u'bn': u'\u09a1\u0997\u09b2\u09be\u09b8 \u0985\u09cd\u09af\u09be\u09a1\u09be\u09ae\u09b8',
                u'be': u'\u0414\u0443\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                u'bg': u'\u0414\u044a\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                u'uk': u'\u0414\u0443\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                u'wa': u'Douglas Adams', u'ast': u'Douglas Adams',
                u'zh-sg': u'\u9053\u683c\u62c9\u65af\xb7\u4e9a\u5f53\u65af',
                u'jv': u'Douglas Adams', u'br': u'Douglas Adams',
                u'bs': u'Douglas Adams',
                u'ja': u'\u30c0\u30b0\u30e9\u30b9\u30fb\u30a2\u30c0\u30e0\u30ba',
                u'oc': u'Douglas Adams',
                u'be-tarask': u'\u0414\u0443\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0437',
                u'de-at': u'Douglas Adams', u'nds': u'Douglas Adams',
                u'yue': u'\u9053\u683c\u62c9\u65af\u4e9e\u7576\u65af',
                u'or': u'\u0b21\u0b17\u0b4d\u200c\u0b32\u0b3e\u0b38\u0b4d\u200c \u0b06\u0b26\u0b3e\u0b2e\u0b4d\u200c\u0b38',
                u'co': u'Douglas Adams', u'ca': u'Douglas Adams',
                u'lmo': u'Douglas Adams',
                u'cy': u'Douglas Adams', u'cs': u'Douglas Adams',
                u'pt': u'Douglas Adams',
                u'zh-tw': u'\u9053\u683c\u62c9\u65af\xb7\u4e9e\u7576\u65af',
                u'lt': u'Douglas Adams', u'frp': u'Douglas Adams',
                u'en-ca': u'Douglas Adams', u'war': u'Douglas Adams',
                u'pl': u'Douglas Adams',
                u'hy': u'\u0534\u0578\u0582\u0563\u056c\u0561\u057d \u0531\u0564\u0561\u0574\u057d',
                u'nrm': u'Douglas Adams', u'hr': u'Douglas Adams',
                u'zh-my': u'\u9053\u683c\u62c9\u65af\xb7\u4e9a\u5f53\u65af',
                u'hu': u'Douglas Adams',
                u'hi': u'\u0921\u0917\u094d\u0932\u0938 \u0905\u200d\u0921\u092e\u094d\u0938',
                u'zh-mo': u'\u9053\u683c\u62c9\u65af\xb7\u4e9e\u7576\u65af',
                u'an': u'Douglas Adams',
                u'he': u'\u05d3\u05d0\u05d2\u05dc\u05e1 \u05d0\u05d3\u05de\u05e1',
                u'mg': u'Douglas Adams', u'fur': u'Douglas Adams',
                u'ml': u'\u0d21\u0d17\u0d4d\u0d32\u0d38\u0d4d \u0d06\u0d21\u0d02\u0d38\u0d4d',
                u'azb': u'\u062f\u0627\u0642\u0644\u0627\u0633 \u0622\u062f\u0627\u0645\u0632',
                u'mk': u'\u0414\u0430\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                u'ur': u'\u0688\u06af\u0644\u0633 \u0627\u06cc\u0688\u0645',
                u'ms': u'Douglas Adams',
                u'mr': u'\u0921\u0917\u094d\u0932\u0938 \u0905\u0945\u0921\u092e\u094d\u0938',
                u'bho': u'\u0921\u0917\u0932\u0938 \u090f\u0921\u092e\u094d\u0938',
                u'af': u'Douglas Adams', u'vi': u'Douglas Adams',
                u'ak': u'Doglas Adams',
                u'it': u'Douglas Adams', u'vo': u'Douglas Adams',
                u'ar': u'\u062f\u0648\u063a\u0644\u0627\u0633 \u0622\u062f\u0645\u0632',
                u'io': u'Douglas Adams', u'zu': u'Douglas Adams',
                u'ia': u'Douglas Adams',
                u'az': u'Duqlas Noel Adams', u'ie': u'Douglas Adams',
                u'id': u'Douglas Adams', u'nds-nl': u'Douglas Adams',
                u'nl': u'Douglas Adams', u'nn': u'Douglas Adams',
                u'min': u'Douglas Adams',
                u'pa': u'\u0a21\u0a17\u0a32\u0a38 \u0a10\u0a21\u0a2e\u0a1c\u0a3c',
                u'nb': u'Douglas Adams', u'nan': u'Douglas Adams',
                u'ne': u'\u0921\u0917\u0932\u0938 \u090f\u0921\u092e\u094d\u0938',
                u'lij': u'Douglas Adams', u'nap': u'Douglas Adams',
                u'fr': u'Douglas Adams',
                u'sv': u'Douglas Adams',
                u'fa': u'\u062f\u0627\u06af\u0644\u0627\u0633 \u0622\u062f\u0627\u0645\u0632',
                u'fi': u'Douglas Adams', u'fo': u'Douglas Adams',
                u'ka': u'\u10d3\u10d0\u10d2\u10da\u10d0\u10e1 \u10d0\u10d3\u10d0\u10db\u10e1\u10d8',
                u'kg': u'Douglas Adams', u'gsw': u'Douglas Adams',
                u'ckb': u'\u062f\u06d5\u06af\u0644\u0627\u0633 \u0626\u0627\u062f\u0645\u0632',
                u'sr': u'\u0414\u0430\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                u'sq': u'Douglas Adams',
                u'ko': u'\ub354\uae00\ub7ec\uc2a4 \uc560\ub364\uc2a4',
                u'kn': u'\u0ca1\u0c97\u0ccd\u0cb2\u0cb8\u0ccd \u0c86\u0ca1\u0cae\u0ccd\u0cb8\u0ccd',
                u'kl': u'Douglas Adams', u'sk': u'Douglas Adams',
                u'ext': u'Douglas Adams',
                u'sh': u'Douglas Adams',
                u'mrj': u'\u0410\u0434\u0430\u043c\u0441',
                u'sl': u'Douglas Adams', u'sc': u'Douglas Adams',
                u'ky': u'\u0414\u0443\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                u'sw': u'Douglas Adams'},
    u'sitelinks': {u'fiwiki': u'Douglas Adams',
                   u'fawiki': u'\u062f\u0627\u06af\u0644\u0627\u0633 \u0622\u062f\u0627\u0645\u0632',
                   u'thwikiquote': u'\u0e14\u0e31\u0e4a\u0e01\u0e25\u0e32\u0e2a \u0e2d\u0e14\u0e31\u0e21\u0e2a\u0e4c',
                   u'viwiki': u'Douglas Adams',
                   u'glwiki': u'Douglas Adams',
                   u'elwikiquote': u'\u039d\u03c4\u03ac\u03b3\u03ba\u03bb\u03b1\u03c2 \u0386\u03bd\u03c4\u03b1\u03bc\u03c2',
                   u'eowikiquote': u'Douglas Adams',
                   u'huwiki': u'Douglas Adams',
                   u'zhwikiquote': u'\u9053\u683c\u62c9\u65af\xb7\u4e9e\u7576\u65af',
                   u'kywiki': u'\u0414\u0443\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                   u'bnwiki': u'\u09a1\u0997\u09b2\u09be\u09b8 \u0985\u09cd\u09af\u09be\u09a1\u09be\u09ae\u09b8',
                   u'mgwiki': u'Douglas Adams',
                   u'nlwiki': u'Douglas Adams',
                   u'mrjwiki': u'\u0410\u0434\u0430\u043c\u0441, \u0414\u0443\u0433\u043b\u0430\u0441',
                   u'fiwikiquote': u'Douglas Adams',
                   u'ptwikiquote': u'Douglas Adams',
                   u'slwiki': u'Douglas Adams',
                   u'lvwiki': u'Duglass Adamss',
                   u'srwiki': u'\u0414\u0430\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                   u'hywiki': u'\u0534\u0578\u0582\u0563\u056c\u0561\u057d \u0531\u0564\u0561\u0574\u057d',
                   u'nowiki': u'Douglas Adams',
                   u'lfnwiki': u'Douglas Adams',
                   u'eswikiquote': u'Douglas Adams',
                   u'frwikiquote': u'Douglas Adams',
                   u'azbwiki': u'\u062f\u0627\u0642\u0644\u0627\u0633 \u0622\u062f\u0627\u0645\u0632',
                   u'ukwiki': u'\u0414\u0443\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                   u'simplewikiquote': u'Douglas Adams',
                   u'plwikiquote': u'Douglas Adams',
                   u'glwikiquote': u'Douglas Adams',
                   u'hewikiquote': u'\u05d3\u05d0\u05d2\u05dc\u05e1 \u05d0\u05d3\u05de\u05e1',
                   u'ptwiki': u'Douglas Adams',
                   u'hywikiquote': u'\u0534\u0578\u0582\u0563\u056c\u0561\u057d \u0531\u0564\u0561\u0574\u057d',
                   u'dewikiquote': u'Douglas Adams',
                   u'huwikiquote': u'Douglas Adams',
                   u'iowiki': u'Douglas Adams',
                   u'jvwiki': u'Douglas Adams',
                   u'rowiki': u'Douglas Adams',
                   u'ocwiki': u'Douglas Adams',
                   u'frwiki': u'Douglas Adams',
                   u'simplewiki': u'Douglas Adams',
                   u'be_x_oldwiki': u'\u0414\u0443\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0437',
                   u'svwiki': u'Douglas Adams',
                   u'kawiki': u'\u10d3\u10d0\u10d2\u10da\u10d0\u10e1 \u10d0\u10d3\u10d0\u10db\u10e1\u10d8',
                   u'etwikiquote': u'Douglas Adams',
                   u'enwikiquote': u'Douglas Adams',
                   u'vepwiki': u'Adams Duglas',
                   u'lawiki': u'Duglassius Adams',
                   u'cawiki': u'Douglas Adams',
                   u'wuuwiki': u'\u9053\u683c\u62c9\u65af\xb7\u4e9a\u5f53\u65af',
                   u'bgwiki': u'\u0414\u044a\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                   u'ltwiki': u'Douglas Adams',
                   u'liwikiquote': u'Douglas Adams',
                   u'bswikiquote': u'Douglas Adams',
                   u'azwikiquote': u'Duqlas Noel Adams',
                   u'jawiki': u'\u30c0\u30b0\u30e9\u30b9\u30fb\u30a2\u30c0\u30e0\u30ba',
                   u'nnwiki': u'Douglas Adams',
                   u'bgwikiquote': u'\u0414\u044a\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                   u'warwiki': u'Douglas Adams',
                   u'eswiki': u'Douglas Adams',
                   u'skwiki': u'Douglas Adams',
                   u'scowiki': u'Douglas Adams',
                   u'mkwiki': u'\u0414\u0430\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                   u'gawiki': u'Douglas Adams',
                   u'trwikiquote': u'Douglas Adams',
                   u'zhwiki': u'\u9053\u683c\u62c9\u65af\xb7\u4e9a\u5f53\u65af',
                   u'bswiki': u'Douglas Adams',
                   u'scwiki': u'Douglas Adams',
                   u'svwikiquote': u'Douglas Adams',
                   u'dawiki': u'Douglas Adams',
                   u'afwiki': u'Douglas Adams',
                   u'idwiki': u'Douglas Adams',
                   u'cswiki': u'Douglas Adams',
                   u'itwikiquote': u'Douglas Adams',
                   u'dewiki': u'Douglas Adams',
                   u'urwiki': u'\u0688\u06af\u0644\u0633 \u0627\u06cc\u0688\u0645\u0633',
                   u'euwiki': u'Douglas Adams',
                   u'itwiki': u'Douglas Adams',
                   u'hrwiki': u'Douglas Adams',
                   u'iswiki': u'Douglas Adams',
                   u'eowiki': u'Douglas Adams',
                   u'pawiki': u'\u0a21\u0a17\u0a32\u0a38 \u0a10\u0a21\u0a2e\u0a38',
                   u'skwikiquote': u'Douglas Adams',
                   u'shwiki': u'Douglas Adams',
                   u'elwiki': u'\u039d\u03c4\u03ac\u03b3\u03ba\u03bb\u03b1\u03c2 \u0386\u03bd\u03c4\u03b1\u03bc\u03c2',
                   u'azwiki': u'Duqlas Adams',
                   u'arzwiki': u'\u062f\u0648\u062c\u0644\u0627\u0633 \u0627\u062f\u0627\u0645\u0632',
                   u'astwiki': u'Douglas Adams',
                   u'enwiki': u'Douglas Adams',
                   u'ruwiki': u'\u0410\u0434\u0430\u043c\u0441, \u0414\u0443\u0433\u043b\u0430\u0441',
                   u'kowiki': u'\ub354\uae00\ub7ec\uc2a4 \uc560\ub364\uc2a4',
                   u'etwiki': u'Douglas Adams',
                   u'ruwikiquote': u'\u0414\u0443\u0433\u043b\u0430\u0441 \u041d\u043e\u044d\u043b\u044c \u0410\u0434\u0430\u043c\u0441',
                   u'ltwikiquote': u'Douglas Adamsas',
                   u'zh_yuewiki': u'\u9053\u683c\u62c9\u65af\u4e9e\u7576\u65af',
                   u'bewiki': u'\u0414\u0443\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441',
                   u'sqwiki': u'Douglas Adams',
                   u'barwiki': u'Douglas Adams',
                   u'fawikiquote': u'\u062f\u0627\u06af\u0644\u0627\u0633 \u0622\u062f\u0627\u0645\u0632',
                   u'tawiki': u'\u0b9f\u0b95\u0bcd\u0bb3\u0bb8\u0bcd \u0b86\u0b9f\u0bae\u0bcd\u0bb8\u0bcd',
                   u'arwiki': u'\u062f\u0648\u063a\u0644\u0627\u0633 \u0622\u062f\u0645\u0632',
                   u'mrwiki': u'\u0921\u0917\u094d\u0932\u0938 \u0905\u200d\u0945\u0921\u092e\u094d\u0938',
                   u'plwiki': u'Douglas Adams',
                   u'mlwiki': u'\u0d21\u0d17\u0d4d\u0d32\u0d38\u0d4d \u0d06\u0d21\u0d02\u0d38\u0d4d',
                   u'cywiki': u'Douglas Adams',
                   u'zh_min_nanwiki': u'Douglas Adams',
                   u'nlwikiquote': u'Douglas Adams',
                   u'cswikiquote': u'Douglas Adams',
                   u'trwiki': u'Douglas Adams',
                   u'hewiki': u'\u05d3\u05d0\u05d2\u05dc\u05e1 \u05d0\u05d3\u05de\u05e1'},
    u'descriptions': {
        u'el': u'\u0386\u03b3\u03b3\u03bb\u03bf\u03c2 \u03c3\u03c5\u03b3\u03b3\u03c1\u03b1\u03c6\u03ad\u03b1\u03c2',
        u'eo': u'angla a\u016dtoro de sciencfikcio-romanoj kaj humoristo',
        u'en': u'author and humorist', u'zh': u'\u82f1\u56fd\u4f5c\u5bb6',
        u'sr-ec': u'\u0435\u043d\u0433\u043b\u0435\u0441\u043a\u0438 \u043f\u0438\u0441\u0430\u0446 \u043d\u0430\u0443\u0447\u043d\u0435 \u0444\u0430\u043d\u0442\u0430\u0441\u0442\u0438\u043a\u0435 \u0438 \u0445\u0443\u043c\u043e\u0440\u0438\u0441\u0442\u0430',
        u'bho': u'\u0905\u0902\u0917\u094d\u0930\u0947\u091c\u0940 \u092d\u093e\u0937\u093e \u0915\u0947 \u092c\u094d\u0930\u093f\u091f\u093f\u0936 \u0932\u0947\u0916\u0915',
        u'af': u'Engelse skrywer en humoris',
        u'vi': u'Nh\xe0 v\u0103n v\xe0 nh\xe0 so\u1ea1n h\xe0i k\u1ecbch ng\u01b0\u1eddi Anh',
        u'ca': u'escriptor angl\xe8s', u'it': u'scrittore ed umorista',
        u'sv': u'brittisk f\xf6rfattare', u'zh-hk': u'\u82f1\u570b\u4f5c\u5bb6',
        u'cy': u'awdur a dychanwr Seisnig', u'gd': u'sgr\xecobhadair Sasannach',
        u'pt-br': u'escritor e humorista ingl\xeas',
        u'mk': u'\u0430\u043d\u0433\u043b\u0438\u0441\u043a\u0438 \u043f\u0438\u0441\u0430\u0442\u0435\u043b \u0438 \u0445\u0443\u043c\u043e\u0440\u0438\u0441\u0442',
        u'cs': u'anglick\xfd spisovatel, humorista a dramatik',
        u'et': u'inglise ulmekirjanik',
        u'gl': u'escritor e guionista brit\xe1nico',
        u'zh-mo': u'\u82f1\u570b\u4f5c\u5bb6',
        u'es': u'escritor y humorista brit\xe1nico',
        u'en-gb': u'English writer and humourist',
        u'ru': u'\u0430\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0439 \u043f\u0438\u0441\u0430\u0442\u0435\u043b\u044c, \u0434\u0440\u0430\u043c\u0430\u0442\u0443\u0440\u0433 \u0438 \u0441\u0446\u0435\u043d\u0430\u0440\u0438\u0441\u0442, \u0430\u0432\u0442\u043e\u0440 \u0441\u0435\u0440\u0438\u0438 \u043a\u043d\u0438\u0433 \xab\u0410\u0432\u0442\u043e\u0441\u0442\u043e\u043f\u043e\u043c \u043f\u043e \u0433\u0430\u043b\u0430\u043a\u0442\u0438\u043a\u0435\xbb',
        u'he': u'\u05e1\u05d5\u05e4\u05e8 \u05d5\u05d4\u05d5\u05de\u05d5\u05e8\u05d9\u05e1\u05d8\u05df \u05d1\u05e8\u05d9\u05d8\u05d9',
        u'nl': u'Engelse schrijver',
        u'pt': u'escritor e comediante brit\xe2nico',
        u'zh-tw': u'\u82f1\u570b\u4f5c\u5bb6',
        u'nb': u'engelsk science fiction-forfatter og humorist',
        u'tr': u'\u0130ngiliz bilim kurgu ve mizah yazar\u0131',
        u'ne': u'\u0905\u0919\u094d\u0917\u094d\u0930\u0947\u091c\u0940 \u0932\u0947\u0916\u0915 \u0930 \u0935\u094d\u092f\u0919\u094d\u0917\u094d\u092f\u0915\u093e\u0930',
        u'lv': u'ang\u013cu zin\u0101tnisk\u0101s fantastikas rakstnieks un humorists',
        u'zh-cn': u'\u82f1\u56fd\u4f5c\u5bb6',
        u'tl': u'taga-Inglatera na manunulat at tagapagpatawa',
        u'pa': u'\u0a05\u0a70\u0a17\u0a30\u0a47\u0a1c\u0a3c\u0a40 \u0a32\u0a47\u0a16\u0a15',
        u'th': u'\u0e19\u0e31\u0e01\u0e40\u0e02\u0e35\u0e22\u0e19\u0e41\u0e25\u0e30\u0e1c\u0e39\u0e49\u0e40\u0e25\u0e48\u0e32\u0e40\u0e23\u0e37\u0e48\u0e2d\u0e07\u0e2d\u0e32\u0e23\u0e21\u0e13\u0e4c\u0e02\u0e31\u0e19\u0e0a\u0e32\u0e27\u0e2d\u0e31\u0e07\u0e01\u0e24\u0e29',
        u'gu': u'\u0a85\u0a82\u0a97\u0acd\u0ab0\u0ac7\u0a9c\u0ac0 \u0ab2\u0ac7\u0a96\u0a95 \u0a85\u0aa8\u0ac7 \u0ab9\u0abe\u0ab8\u0acd\u0aaf\u0a95\u0abe\u0ab0',
        u'ro': u'scriitor, dramaturg englez',
        u'sr-el': u'engleski pisac nau\u010dne fantastike i humorista',
        u'pl': u'brytyjski pisarz',
        u'ta': u'\u0b86\u0b99\u0bcd\u0b95\u0bbf\u0bb2 \u0b8e\u0bb4\u0bc1\u0ba4\u0bcd\u0ba4\u0bbe\u0bb3\u0bb0\u0bcd \u0bae\u0bb1\u0bcd\u0bb1\u0bc1\u0bae\u0bcd \u0ba8\u0b95\u0bc8\u0b9a\u0bcd\u0b9a\u0bc1\u0bb5\u0bc8\u0baf\u0bbe\u0bb3\u0bb0\u0bcd',
        u'fr': u'\xe9crivain anglais de science-fiction',
        u'bg': u'\u0430\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438 \u043f\u0438\u0441\u0430\u0442\u0435\u043b \u0438 \u0445\u0443\u043c\u043e\u0440\u0438\u0441\u0442',
        u'ast': u'escritor y humorista ingl\xe9s',
        u'zh-sg': u'\u82f1\u56fd\u4f5c\u5bb6',
        u'de': u'britischer Schriftsteller',
        u'zh-my': u'\u82f1\u56fd\u4f5c\u5bb6',
        u'ko': u'\uc601\uad6d\uc758 \uc791\uac00', u'da': u'engelsk forfatter',
        u'fa': u'\u0641\u06cc\u0644\u0645\u0646\u0627\u0645\u0647\u200c\u0646\u0648\u06cc\u0633 \u0648 \u0646\u0648\u06cc\u0633\u0646\u062f\u0647 \u0628\u0631\u06cc\u062a\u0627\u0646\u06cc\u0627\u06cc\u06cc',
        u'br': u'skrivagner saoznek',
        u'fi': u'englantilainen kirjailija ja humoristi',
        u'hy': u'\u0561\u0576\u0563\u056c\u056b\u0561\u0581\u056b \u0563\u0580\u0578\u0572, \u0564\u0580\u0561\u0574\u0561\u057f\u0578\u0582\u0580\u0563, \u057d\u0581\u0565\u0576\u0561\u0580\u056b\u057d\u057f, \xab\u0531\u057e\u057f\u0578\u057d\u057f\u0578\u057a\u0578\u057e \u0566\u0562\u0578\u057d\u0561\u0577\u0580\u057b\u056b\u056f\u056b \u0574\u056b\u057b\u0563\u0561\u056c\u0561\u056f\u057f\u056b\u056f\u0561\u056f\u0561\u0576 \u0578\u0582\u0572\u0565\u0581\u0578\u0582\u0575\u0581\xbb \u057e\u0565\u057a\u0565\u0580\u056b \u0577\u0561\u0580\u0584',
        u'hu': u'angol \xedr\xf3',
        u'ja': u'\u30a4\u30f3\u30b0\u30e9\u30f3\u30c9\u306e\u4f5c\u5bb6',
        u'en-ca': u'English writer',
        u'ka': u'\u10d8\u10dc\u10d2\u10da\u10d8\u10e1\u10d4\u10da\u10d8 \u10db\u10ec\u10d4\u10e0\u10d0\u10da\u10d8 \u10d3\u10d0 \u10d8\u10e3\u10db\u10dd\u10e0\u10d8\u10e1\u10e2\u10d8',
        u'te': u'\u0c07\u0c02\u0c17\u0c4d\u0c32\u0c40\u0c37\u0c41 \u0c30\u0c1a\u0c2f\u0c3f\u0c24, \u0c39\u0c3e\u0c38\u0c4d\u0c2f\u0c15\u0c3e\u0c30\u0c41\u0c21\u0c41',
        u'bar': u'a englischer Science-Fiction-Schriftsteller',
        u'nn': u'engelsk sciencefictionforfattar og humorist',
        u'gsw': u'britischer Schriftsteller',
        u'zh-hans': u'\u82f1\u56fd\u4f5c\u5bb6',
        u'sr': u'\u0435\u043d\u0433\u043b\u0435\u0441\u043a\u0438 \u043f\u0438\u0441\u0430\u0446 \u043d\u0430\u0443\u0447\u043d\u0435 \u0444\u0430\u043d\u0442\u0430\u0441\u0442\u0438\u043a\u0435 \u0438 \u0445\u0443\u043c\u043e\u0440\u0438\u0441\u0442\u0430',
        u'sq': u'autor dhe humorist anglez', u'sw': u'mwandishi Mwingereza',
        u'kn': u'\u0c87\u0c82\u0c97\u0ccd\u0cb2\u0cbf\u0cb7\u0ccd \u0cad\u0cbe\u0cb7\u0cc6\u0caf \u0cac\u0cb0\u0cb9\u0c97\u0cbe\u0cb0 \u0cb9\u0cbe\u0c97\u0cc2 \u0cb9\u0cbe\u0cb8\u0ccd\u0caf \u0cb2\u0cc7\u0c96\u0c95',
        u'de-ch': u'britischer Schriftsteller',
        u'zh-hant': u'\u82f1\u570b\u4f5c\u5bb6',
        u'hr': u'britanski radijski dramaturg i pisac znanstvene fantastike',
        u'si': u'\u0d89\u0d82\u0d9c\u0dca\u200d\u0dbb\u0dd3\u0dc3\u0dd2 \u0d9a\u0dc0\u0dd2\u0dba\u0dd9\u0d9a\u0dca',
        u'ar': u'\u0643\u0627\u062a\u0628 \u0625\u0646\u062c\u0644\u064a\u0632\u064a \u0641\u0643\u0627\u0647\u064a',
        u'sk': u'anglick\xfd spisovate\u013e',
        u'uk': u'\u0431\u0440\u0438\u0442\u0430\u043d\u0441\u044c\u043a\u0438\u0439 \u043a\u043e\u043c\u0456\u0447\u043d\u0438\u0439 \u0440\u0430\u0434\u0456\u043e\u0434\u0440\u0430\u043c\u0430\u0442\u0443\u0440\u0433, \u043f\u0438\u0441\u044c\u043c\u0435\u043d\u043d\u0438\u043a',
        u'sl': u'angle\u0161ki pisatelj, humorist in dramatik',
        u'de-at': u'britischer Schriftsteller',
        u'nds': u'englischer Schriftsteller',
        u'eu': u'idazle eta umorista britaniarra'},
    u'aliases': {u'el': [
        u'\u039d\u03c4\u03ac\u03b3\u03ba\u03bb\u03b1\u03c2 \u039d\u03cc\u03b5\u03bb \u0386\u03bd\u03c4\u03b1\u03bc\u03c2'],
        u'en': [
            u'Douglas No\xebl Adams',
            u'Douglas Noel Adams',
            u'Douglas N. Adams'],
        u'zh': [
            u'\u4e9e\u7576\u65af'],
        u'bho': [
            u'\u0921\u0917\u094d\u0932\u0938 \u0905\u0921\u092e\u094d\u0938',
            u'\u0921\u0917\u094d\u0932\u0938 \u090f\u0921\u092e\u094d\u0938'],
        u'ko': [
            u'\ub354\uae00\ub77c\uc2a4 \uc560\ub364\uc2a4',
            u'\ub354\uae00\ub7ec\uc2a4 \ub178\uc5d8 \uc560\ub364\uc2a4'],
        u'it': [
            u'Douglas Noel Adams',
            u'Douglas N. Adams'],
        u'cs': [
            u'Douglas No\xebl Adams',
            u'Douglas Noel Adams',
            u'Douglas N. Adams'],
        u'ar': [
            u'\u062f\u0648\u063a\u0644\u0627\u0633 \u0646\u0648\u064a\u0644 \u0622\u062f\u0645\u0632',
            u'\u062f\u0648\u063a\u0644\u0627\u0633 \u0646. \u0622\u062f\u0645\u0632',
            u'\u062f\u0648\u063a\u0644\u0627\u0633 \u0622\u062f\u0627\u0645\u0632',
            u'\u062f\u0648\u062c\u0644\u0627\u0633 \u0622\u062f\u0645\u0632'],
        u'pt-br': [
            u'Douglas No\xebl Adams',
            u'Douglas Noel Adams'],
        u'eu': [
            u'Douglas Noel Adams',
            u'Douglas No\xebl Adams'],
        u'et': [
            u'Douglas No\xebl Adams'],
        u'gl': [
            u'Douglas No\xebl Adams'],
        u'es': [
            u'Douglas Noel Adams',
            u'Douglas No\xebl Adams'],
        u'ru': [
            u'\u0410\u0434\u0430\u043c\u0441, \u0414\u0443\u0433\u043b\u0430\u0441'],
        u'nl': [
            u'Douglas Noel Adams',
            u'Douglas No\xebl Adams'],
        u'pt': [
            u'Douglas No\xebl Adams',
            u'Douglas Noel Adams'],
        u'la': [
            u'Duglassius No\xeblus Adams'],
        u'nb': [
            u'Douglas No\xebl Adams',
            u'Douglas N. Adams'],
        u'tr': [
            u'Douglas Noel Adams',
            u'Douglas N. Adams'],
        u'tl': [
            u'Douglas No\xebl Adams',
            u'Douglas Noel Adams'],
        u'pa': [
            u'\u0a21\u0a17\u0a32\u0a38 \u0a28\u0a4b\u0a0f\u0a32 \u0a10\u0a21\u0a2e\u0a1c\u0a3c'],
        u'fr': [
            u'Douglas Noel Adams',
            u'Douglas No\xebl Adams'],
        u'hy': [
            u'\u0531\u0564\u0561\u0574\u057d, \u0534\u0578\u0582\u0563\u056c\u0561\u057d'],
        u'hr': [
            u'Douglas No\xebl Adams',
            u'Douglas N. Adams',
            u'Douglas Noel Adams'],
        u'de': [
            u'Douglas No\xebl Adams',
            u'Douglas Noel Adams'],
        u'ja': [
            u'\u30c0\u30b0\u30e9\u30b9\u30fb\u30a2\u30c0\u30e0\u30b9'],
        u'he': [
            u'\u05d3\u05d2\u05dc\u05e1 \u05d0\u05d3\u05de\u05e1'],
        u'sw': [
            u'Douglas Noel Adams',
            u'Douglas No\xebl Adams'],
        u'be-tarask': [
            u'\u0414\u0443\u0433\u043b\u0430\u0441 \u0410\u0434\u0430\u043c\u0441'],
        u'uk': [
            u'\u0414\u0443\u0433\u043b\u0430\u0441 \u041d\u043e\u0435\u043b \u0410\u0434\u0430\u043c\u0441']}}

print(itempage['sitelinks'])
