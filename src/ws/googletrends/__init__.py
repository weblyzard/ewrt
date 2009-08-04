from eWRTlibs.googleTrends.pyGTrends import pyGTrends
from config import GOOGLE_USER, GOOGLE_PASS

## Documentation for the Class Google Trends
#
# fetches the Google trends for a set of keywords
class GoogleTrends(object):

    ## Constructor establishes the connection
    # @param user
    # @param password
    def __init__(self, user=GOOGLE_USER, password=GOOGLE_PASS):
        """ Constructor establishes the connection """
        self.connector = pyGTrends(user, password)

    ## getTrends fetches the trends
    # @param keywords
    # @param date to filter 
    # @param section
    # @return 
    def getTrends(self, keywords, date=None, section=None):
        if date == None:
            self.connector.download_report(keywords)
        else:
            self.connector.download_report(keywords, date)

        if section == None:
            trends = self.connector.csv()
        else:
            trends = self.connector.csv()

        return trends

if __name__ == "__main__":
    a = GoogleTrends()
    print a.getTrends(('Terminator', 'Rambo'))
    print a.getTrends(('Apple', 'Microsoft'))
