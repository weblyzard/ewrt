# #!/usr/bin/python
# # -*- coding: utf-8 -*-
# import unittest
# import json
#
# from eWRT.util.loggerProfile import get_file_logger
# from eWRT.ws.conceptnet.lookup_result import LookupResult
# from eWRT.ws.conceptnet.util import ground_term
# from eWRT.ws.conceptnet import Result
#
#
# LOGGER = get_file_logger(name='eWRT.ws.conceptnet.unittest',
#                          filename='eWRT.ws.conceptnet.unittest.log')
#
#
# class TestConceptNet(unittest.TestCase):
#
#     def test_lookup_result(self):
#         l = LookupResult("dog")
#
#     def test_concept_grounding(self):
#         concept = ground_term(
#             'battery', ['life', 'extensive', 'too', 'short', 'electricity'])
#         LOGGER.debug("Grounded concept: %s.", concept)
#
#     def test_get_vsm(self):
#         json_string = json.dumps(eval("""{'edges': [{u'features': [u'/c/en/look_at /r/DerivedFrom -', u'/c/en/look_at - /c/en/look/v', u'- /r/DerivedFrom /c/en/look/v'], u'weight': 1.5, u'text': [u'look', u'look at'], u'dataset': u'/d/wiktionary/en/en', u'sources': [u'/s/rule/wiktioary_monolingual_definitions', u'/s/web/en.wiktionary.org'], u'id': u'/e/8d03305cbe5d3aa19cf4e35cf56b9cfa4578c7ce', u'surfaceText': u'[[look at]] DerivedFrom [[look]]', u'endLemmas': u'look', u'end': u'/c/en/look/v', u'license': u'/l/CC/By-SA', u'startLemmas': u'look at', u'uri': u'/a/[/r/DerivedFrom/,/c/en/look_at/,/c/en/look/v/]', u'rel': u'/r/DerivedFrom', u'start': u'/c/en/look_at', u'score': 9.476239, u'context': u'/ctx/all', u'timestamp': u'2013-03-05T06:36:23.081Z', u'nodes': [u'/c/en/look/v', u'/c/en/look_at', u'/r/DerivedFrom']}]}"""))
#
#         r = Result(json_string)
#         assert len(r.get_vsm(stopword_list=[])) == 2
#         assert 'look' in r.get_vsm(stopword_list=[])
#         assert 'at' in r.get_vsm(stopword_list=[])
#
#         assert len(r.get_vsm(stopword_list=['look', 'at'])) == 0
#
#
# if __name__ == '__main__':
#     unittest.main()
