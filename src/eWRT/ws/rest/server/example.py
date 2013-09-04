'''
Created on 12.06.2013

@author: streifdaniel
'''

from eWRT.ws.rest.server.service import WeblyzardService

class HelloWorld(WeblyzardService):
    
    DEFAULT_PATH = "helloworld";
    
    isLeaf = True
    
    def __init__(self, cfg=None):
        WeblyzardService.__init__(self, self.hello_world)

    def hello(self):
        return "Hello"
    
    def hello_world(self, name = "World"):
        ''' Returns "Hello [name]"
            
            @param name: the name to say hi to
            @return: greetings
        '''
        return "Hello " + name

if __name__ == '__main__':
    from twisted.web import server
    from twisted.internet import reactor
    
    root = HelloWorld()
    root.putChild(HelloWorld.DEFAULT_PATH, HelloWorld())
    server = server.Site(root)
    reactor.listenTCP(8123, server)
    reactor.run()