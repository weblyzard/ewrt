'''
Created on Feb 3, 2012

@author: heinz-peterlang
'''

from json import loads
from inspect import getargspec

from twisted.web import resource

from compiler.ast import Function

class WeblyzardService(resource.Resource):
    '''
    The Weblyzard RESTless service base class
    '''

    children = {}

    # deprecated
    VALID_ARGS = None

    def __init__(self, function=None):
        '''
        @param get_function: the function to call for get requests
        '''
        argspec = getargspec(function)
        self.func_args = argspec.args
        self.func_required_args = self.func_args if not argspec.defaults \
                  else self.func_args[:-len(argspec.defaults)]
        self.func_required_args.remove('self')
        self.function = function
    
    def render_GET(self, request):
        args = { key: value[0] for key, value in request.args.items() }
        return self.call(self.function, args)
    
    def render_POST(self, request):
        args = loads( request.content.read() )
        return self.call(self.function, args)
    
    @classmethod
    def check_arguments(cls, request):
        """ @deprecated: use call instead """
        
        for arg in cls.VALID_ARGS:
            if not arg in request.args:
                return MissingArgumentErrorMsg(cls.check_arguments, arg)()
        
        return True
    
    def call(self, function, args):
        """ calls the given function if all required arguments have been
            supplied, or output its docstring otherwise.
            
            @param Function: the function to call
            @param request:  the twisted request object
            @return: the functions return value
        """
        for required_arg in self.func_required_args:
            if required_arg not in args:
                return MissingArgumentErrorMsg(function, required_arg)()
        
        #print self.func_required_args
        
        for arg in args:
            if arg not in self.func_args:
                return UnknownArgumentErrorMsg(function, arg)()
        
        return self.function(**args)
