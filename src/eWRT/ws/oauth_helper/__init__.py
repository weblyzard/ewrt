'''
Created on 31.10.2014

@author: heinz-peterlang
'''


import pickle
import requests
import httplib2

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

from flask import render_template, redirect, request

http = httplib2.Http()
http.disable_ssl_certificate_validation = True

class OAuthHelper(object):
    
    def __init__(self, client_id=None, 
                 client_secret=None, scope=None, redirect_uri=None, 
                 auth_uri=None, token_uri=None, **kwargs):
        self.client_id = client_id
        self.client_secret = client_secret

        self.scope = scope
        self.redirect_uri = redirect_uri
        self.auth_uri = auth_uri
        self.token_uri = token_uri
        
    def run(self, auth_code=None):
        text = None
        redirect_url = None
        flow =  OAuth2WebServerFlow(client_id=self.client_id, 
                                    client_secret=self.client_secret, 
                                    scope=self.scope, 
                                    redirect_uri=self.redirect_uri,
                                    auth_uri=self.auth_uri,
                                    token_uri=self.token_uri)
        if not auth_code: 
            redirect_url = flow.step1_get_authorize_url()
        else: 
            credentials = flow.step2_exchange(auth_code)
            text = 'Thanks ... your credentials %s' % credentials
            
        return text, redirect_url
    
    @classmethod
    def authorize_app(cls, **credentials):
        
        auth_code = request.args.get(credentials.get('response_type'), None)
    
        oauth = cls(**credentials)
        text, redirect_url = oauth.run(auth_code=auth_code)
        if redirect_url: 
            return redirect(redirect_url)
        else: 
            return render_template('index.html', text=text)
        
        
        
    