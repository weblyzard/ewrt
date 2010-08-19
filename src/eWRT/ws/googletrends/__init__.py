from eWRT.config import GOOGLE_USER, GOOGLE_PASS

try:
    from eWRTlibs.googleTrends.pyGTrends import pyGTrends
    LOADED = True
except ImportError:
    from warnings import warn
    from sys import exit
    warn("This module requires google Trends ")
    LOADED = False
    
class GoogleTrends(object):
    ''' ## Documentation for the Class Google Trends
        fetches the Google trends for a set of keywords '''

    
    def __init__(self, user=GOOGLE_USER, password=GOOGLE_PASS):
        ''' Constructor establishes the connection
            @param user
            @param password
        '''
        self.connector = pyGTrends(user, password)
        
 
    def getTrends(self, keywords, date=None, section=None):
        ''' getTrends fetches the trends
            @param keywords
            @param date to filter 
            @param section
            @return trends 
        '''
        if date == None:
            self.connector.download_report(keywords)
        else:
            self.connector.download_report(keywords, date)

        print self.connector.header_dictionary

        if section == None:
            trends = self.connector.csv()
        else:
            trends = self.connector.csv()

        return trends

if __name__ == "__main__":
    a = GoogleTrends()
    print a.getTrends(('Apple', 'Microsoft'))
