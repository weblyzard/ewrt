'''
Created on 29.05.2013

This modules help increasing the expiry time of the access token and returns 
a new one. 

:author: heinz-peterlang
'''
import urlparse

from eWRT.access.http import Retrieve
from eWRT.config import (FACEBOOK_APPLICATION_ID, FACEBOOK_SECRET_KEY, 
                         FACEBOOK_ACCESS_KEY)

API_URL = 'https://graph.facebook.com/oauth/access_token?client_id={client_id}&client_secret={client_secret}&grant_type=fb_exchange_token&fb_exchange_token={access_token}'

def get_new_access_token(client_id=FACEBOOK_APPLICATION_ID,
                         client_secret=FACEBOOK_SECRET_KEY,
                         access_token=FACEBOOK_ACCESS_KEY):
    ''' '''
    url = API_URL.format(client_id=client_id,
                         client_secret=client_secret,
                         access_token=access_token)
    
    retrieve = Retrieve('fb')
    x = retrieve.open(url)
    result = x.read() 
    new_access_token = access_token
    
    for key, param in urlparse.parse_qs(result).iteritems():
        print key, param
        if key == 'access_token':
            if isinstance(param, list):
                param = param[0]
            
            if param == access_token:
                print 'access token still the same'
            else: 
                print 'got new access_token %s' % param
                new_access_token = param
                
    return new_access_token
            
if __name__ == '__main__':
    get_new_access_token()
