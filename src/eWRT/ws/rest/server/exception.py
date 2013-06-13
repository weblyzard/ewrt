'''
Created on Feb 3, 2012

@author: heinz-peterlang
'''

class ArgumentErrorMsg(object):
    def __init__(self, function):
        self.function = function
        self.error_msg = ""
     
    def __call__(self):
        return "<h1>%s</h1><font color='red'>%s</font><p/><pre>%s</pre>" % \
             (self.function.__name__, self.error_msg, self.function.__doc__)

class MissingArgumentErrorMsg(ArgumentErrorMsg):

    def __init__(self, function, argument):
        ArgumentErrorMsg.__init__(self, function)
        self.error_msg = "Missing argument: '%s'." % (argument) 
    
class UnknownArgumentErrorMsg(ArgumentErrorMsg):

    def __init__(self, function, argument):
        ArgumentErrorMsg.__init__(self, function)
        self.error_msg = "Unknown argument: '%s'." % (argument)    