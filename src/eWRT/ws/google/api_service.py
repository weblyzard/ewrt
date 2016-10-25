#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle

from oauth2client.client import OAuth2WebServerFlow


class GoogleService(object):
    
    def __init__(self, client_id, client_secret, oauth_scope, redirect_url,
                 cred_filename):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_scope = oauth_scope
        self.redirect_url = redirect_url
        self.cred_filename = cred_filename
                     
    def register_service(self, auth_code=None):
        '''
        Run through the OAuth flow and retrieve credentials
        The retrieved OAuth token is saved in a pickle object.

        :param auth_code: A Google Authentication Code for a Service.
        '''
        flow = OAuth2WebServerFlow(self.client_id, self.client_secret,
                                   self.oauth_scope, self.redirect_url)
        authorize_url = flow.step1_get_authorize_url()

        if not auth_code:
            print 'Go to the following link in your browser: ' + authorize_url
            auth_code = raw_input('Enter verification code: ').strip()
        credentials = flow.step2_exchange(auth_code)
#         if not os.path.exists(self.cred_file_dir): os.makedirs(self.cred_file_dir)
        pickle.dump(credentials, open(self.cred_filename, 'w'))
       
if __name__ == '__main__':
    GOOGLE_CREDS = {
        "client_id":"437502718962-sihuiinggol59ev3s44ok2lsaah48tvl.apps.googleusercontent.com",
        "project_id":"angular-expanse-118116",
        "auth_uri":"https://accounts.google.com/o/oauth2/auth",
        "token_uri":"https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
        "client_secret":"K8ucV1NcvFUmiGVVr4g1-vuZ",
        "redirect_url":"urn:ietf:wg:oauth:2.0:oob"}
    
    GOOGLE_CREDS = {
        "client_id":"437502718962-mni1uv7s21dvkrjcrvrdedtv98jv7nen.apps.googleusercontent.com",
        "project_id":"angular-expanse-118116",
        "auth_uri":"https://accounts.google.com/o/oauth2/auth",
        "token_uri":"https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
        "client_secret":"Olc6MOX4uSK7Z4h8sMRAK8Ac",
        "redirect_url":"urn:ietf:wg:oauth:2.0:oob"}
    
    cred_filename = '/tmp/google_analytics'
    oauth_scope = 'https://www.googleapis.com/auth/analytics.readonly'
    client = GoogleService(client_id=GOOGLE_CREDS['client_id'], 
                           client_secret=GOOGLE_CREDS['client_secret'], 
                           oauth_scope=oauth_scope, 
                           redirect_url=GOOGLE_CREDS['redirect_url'], 
                           cred_filename=cred_filename)
    client.register_service()