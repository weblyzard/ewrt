import unittest

from eWRT.ws.googlealert import EmailParser


class TestEmailParserGoogleAlert(unittest.TestCase):
    
    def setUp(self):
        with open('test1', 'r') as file_conn:
            self.test_email = file_conn.read()
    
    def test_parse_urls(self):
        extracted_data = EmailParser.parse(self.test_email)
        self.assertEquals(extracted_data['urls'], ['http://www.militaryaerospace.com/articles/2013/03/DARPA-machine-learning.html'])
    
    def test_parse_body(self):
        extracted_data = EmailParser.parse(self.test_email)
        self.assertEquals(extracted_data['email_payload'], '=== News - 1 new result for [Machine Learning] ===\n\nDARPA launches PPAML artificial intelligence program to move machine ...\nMilitary & Aerospace Electronics\nThe goal of PPAML is to advance machine learning by using probabilistic\nprogramming to increase the number of people who can build machine learning\napplications; make machine learning experts more effective; and enable new\napplications that are ...\nSee all stories on this topic:\n\nThis as-it-happens Google Alert is brought to you by Google.\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDelete this Google Alert:\n\nCreate another Google Alert:\n\nSign in to manage your alerts:')

    def test_parse_recipient(self):
        extracted_data = EmailParser.parse(self.test_email)
        self.assertEquals(extracted_data['email_recipient'], 
                          'bicycle_repair_man@gmail.com')

    def test_parse_subject(self):
        extracted_data = EmailParser.parse(self.test_email)
        self.assertEquals(extracted_data['email_subject'], 
                          'Google Alert - Machine Learning')
    
class TestEmailParserSeveralUrls(unittest.TestCase):
    
    def setUp(self):
        with open('test3', 'r') as file_conn:
            self.test_email = file_conn.read()
            
    def test_parse_urls(self):
        extracted_urls = EmailParser.parse(self.test_email)
        self.assertEquals(extracted_urls['urls'], ['http://www.coventrytelegraph.net/news/coventry-news/2013/03/26/look-willenhall-man-s-python-nearly-ate-friend-92746-33060856/', 'http://careers.hereisthecity.com/job/senior-developer--researcher--ccpython-green---field-systematic-trading-platform-384325/'])
    
    def test_parse_body(self):
        extracted_data = EmailParser.parse(self.test_email)
        self.assertEquals(extracted_data['email_payload'], '''=== News - 2 new results for [Python] ===\n\nLOOK: Willenhall man's stolen python nearly ate friend\nCoventry Telegraph\nA MAN ended up in court after buying a 10ft stolen python during a drinking\nsession. Dwayne Matthews agreed to buy the African rock snake off a\ntraveller and thought he would sell it on. But in the cold light of day\nwhen he woke up the next morning he ...\nSee all stories on this topic:\n\nSenior Developer / Researcher (C#/C++/Python) Green - Field Systematic ...\nHere Is The City\nSENIOR DEVELOPER/RESEARCHER(C#/C++/PYTHON) GREEN-FIELD SYSTEMATIC TRADING\nPLATFORM BOUTIQUE SYSTEMATIC FUND MANAGER / LIECHTENSTEIN (CANDIDATES FROM\nALL EUROPEAN LOCATIONS CONSIDERED) ...\nSee all stories on this topic:\n''')
    
if __name__ == '__main__':
    unittest.main()