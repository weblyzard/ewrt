'''
Created on 31.10.2014

@author: heinz-peterlang
'''

if __name__ == '__main__':
    from argparse import ArgumentParser
    from eWRT.ws.oauth_helper.webapp import app
    
    parser = ArgumentParser()
    parser.add_argument('--debug', action='store_true', default=False, 
                        help='enables debugging')
    args = parser.parse_args()
    app.run(debug=True)