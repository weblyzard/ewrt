class TagInfoService(object):
    """ Class for fetching assigned tags """
    
    def getTagInfo( self, tags ):
        """ returns the count for the given tags
            @param list/tuple of tags
            @returns number of counts """ 
        return NotImplemented        

    def getRelatedTags( self, tags ):
        """ returns a the count of related tags 
            @param list/tuple of tags 
            @returns list of related tags with a count of their occurence """
