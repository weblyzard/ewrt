#!/usr/bin/env python

## create a iterable ResultSet for storing values of the Webservices 
class ResultSet:

    ## Constructor
    # @parameter id (optional) integer
    # @parameter name (optional) String
    # @parameter content (optional) a Result or ResultSet
    def __init__(self, id=None, name=None, content=None): 
        self.id = id
        self.name = name
        self.setContent(content) 
        self.idx = 0 

    ## returns the next item in the ResultSet
    # @result or ResultSet
    # @return content = Result, ResultSet 
    def next(self): 
        #if self.idx > self.content.count:
        if self.idx >= len(self.content): 
            self.refresh()
            raise StopIteration 
        result = self.content[self.idx]
        self.idx += 1 
        return result
    ## function for the iterator
    def __iter__(self): 
        return self 

    ## sets the pointer of the index to 0
    def refresh(self): 
        self.idx = 0 

    ## sets the content to the new content
    # overrides the content 
    # @parameter content = Result, ResultSet 
    def setContent(self, content):
        if content is None:
            self.content = []
        else:
            self.content = content

    ## adds new content to the existing one
    # @parameter newContent = Result or ResultSet
    def addContent(self, newContent):
        self.content.append(newContent)
        """ todo: needs to be implemented """

    ## return the ID of the ResultSet
    # @return ID integer
    def getId(self):
        return self.id

    ## return the Name of the ResultSet
    # @return Name String
    def getName(self):
        return self.name

    ## prints the items stored in the ResultSet
    @staticmethod
    def printRS(resultSet, filler = 0):
        print resultSet.getName(),':'

        for result in resultSet:
            if cmp(result.__class__.__name__, 'ResultSet') == 0:
                # filler = filler + 1
                ResultSet.printRS(result, filler)
            else:
                print result.getId(), result.getName()


if __name__ == "__main__":
    
    from Result import Result

    a = Result(1, 'foobar1')
    b = Result(2, 'foobar2')
    c = Result(3, 'foobar3')
    d = Result(4, 'foobar4')
    e = Result(5, 'foobar5')
    f = Result(6, 'foobar6')
    g = Result(7, 'foobar7')
    h = Result(8, 'foobar8')
    i = Result(9, 'foobar9')

    content = [a, b, c, d]
    rs = ResultSet(1, 'RS1')
    rs.addContent(a)
    rs.addContent(b)
    rs.addContent(c)
    rs.addContent(d)

    rs2 = ResultSet(1, 'RS2')
    rs2.addContent(rs)
    rs2.addContent(e)
    rs2.addContent(f)

    rs2.printRS(rs2)
