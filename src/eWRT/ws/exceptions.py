'''
Exceptions for more fine-grained errors that can occurr in web service clients.
'''

class AuthenticationError(Exception):
    '''
    Raise this exception if a request fails due to authentication issues.
    '''
    pass
