'''
Created on 31.10.2014

@author: heinz-peterlang
'''
try: 
    from flask import Flask, render_template, request
    from flask_wtf import Form
    from wtforms import StringField
except: 
    print 'install flask to use this feature'

from eWRT.ws.oauth_helper import OAuthHelper

class CredentialsForm(Form):
    
    @classmethod
    def get_form(cls, service_name, parameters):
        ''' returns the form with the given parameters '''
        cls.service_name = StringField('service_name', 
                                       default=service_name)
        
        for parameter, value in parameters: 
            setattr(cls, parameter, StringField(parameter, default=value)) 
            
        return cls(csrf_enabled=False)

class OauthConfig(object):
    
    def __init__(self, service_name, client_id=None, client_secret=None, 
                 scope=None, auth_uri=None, token_uri=None, 
                 redirect_uri=None, response_type=None):
        self.service_name = service_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope 
        self.auth_uri = auth_uri 
        self.token_uri = token_uri
        self.redirect_uri = redirect_uri 
        self.response_type = response_type 

    def get_form(self):
        parameters = [('client_id', self.client_id), 
                      ('client_secret', self.client_secret),
                      ('scope', self.scope), 
                      ('auth_uri', self.auth_uri), 
                      ('token_uri', self.token_uri),
                      ('redirect_uri', self.redirect_uri),
                      ('response_type', self.response_type)]
        return CredentialsForm.get_form(service_name=self.service_name, 
                                        parameters=parameters)

SERVICES = {
    'instagram': OauthConfig(service_name='instagram', 
                             scope='basic', 
                             auth_uri='https://api.instagram.com/oauth/authorize', 
                             token_uri='https://api.instagram.com/oauth/access_token', 
                             redirect_uri='http://localhost:5000/auth/instagram', 
                             response_type='code'),
    'other': OauthConfig('other'), 
}

app = Flask(__name__)
            
@app.route('/')
def index():
    content = ''
    return render_template('index.html', content=content)

@app.route('/auth/', methods=['POST'])
@app.route('/auth/<service_name>', methods=['GET', 'POST'])
def authorize(service_name=None):
    ''' presents a form to enter the credentials '''
    
    access_token = request.args.get('code', None)
    
    if request.method == 'POST':
        return OAuthHelper.authorize_app(**request.form.to_dict())
    elif access_token:
        return render_template('index.html', 
                               service_name=service_name,
                               access_token=access_token) 
    elif service_name: 
        form = SERVICES[service_name].get_form()
        return render_template('auth.html', service_name=service_name, form=form)
    else: 
        return render_template('index.html', error='select a service')
    
    