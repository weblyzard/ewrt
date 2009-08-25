#!/usr/bin/env python

## Result is an item of ResultSet
class Result:

    ## constructor 
    # @parameter id, name
    def __init__(self, id, name):
        self.id = id
        self.name = name

    ## get the ID of Result
    # @return Id
    def getId(self):
        return self.id

    ## get the Name of the Result
    # @return Name
    def getName(self):
        return self.name

    def getAttributes(self):
        """ todo: return attributes of Result """

