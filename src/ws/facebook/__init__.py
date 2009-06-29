#!/usr/bin/env python
import sys
from config_facebook import FACEBOOK_API_KEY, FACEBOOK_SECRET_KEY, FACEBOOK_SESSION_KEY
from lib.Webservice import Webservice 
from lib.Result import Result
from lib.ResultSet import ResultSet
from externalLibs.facebook.facebook_api import Facebook

class FacebookWS(Webservice):
    """ class for fetching and storing the data of a user
    requires that the facebook API key and the facebook secret key are
    set in the configuration file. These can be retrieved from facebook
    todo: add url
    issues: the loginprocess opens a browser window every time the pragram is started
    todo: describe usage of Result and ResultSet
    """

    albums = None
    friends = None
    groups = None

    def __init__(self):
        """ init """       
        self.login()


    def login(self):
        """ opens a browserwindow to login at facebook """
        # FACEBOOK_SESSION_KEY = ''
        if FACEBOOK_SESSION_KEY == '':
            self.facebook = Facebook(FACEBOOK_API_KEY, FACEBOOK_SECRET_KEY)
            self.facebook.auth.createToken()
            self.facebook.login()
        else:
            print 'Infinite session key found'
            self.facebook = Facebook(FACEBOOK_API_KEY, FACEBOOK_SECRET_KEY)
            self.facebook.session_key = FACEBOOK_SESSION_KEY

 
    def loadAlbums(self, userID=None, loadPhotos=0):    
        """ fetches all albums for a user """

        if userID is None:
            userID = self.facebook.uid

        self.albums = ResultSet(None, 'Albums')

        loadedAlbums = self.facebook.photos.getAlbums(userID)

        for album in loadedAlbums:
            id = album['aid']
            name = album['name']
            newAlbum = ResultSet(id, name)
            self.albums.addContent(newAlbum)

            if loadPhotos is 1:
                self.loadPhotos(newAlbum)


    #def loadPhotos(self, albumID, userID=None):
    def loadPhotos(self, album):
        """ fetches all photos in an album """
        
        photos = self.facebook.photos.get(album.getId())

        for photo in photos:
            
            newPhoto = ResultSet(photo['pid'], photo['name'], photo['tags'])

            album.addContent(newPhoto)       


    def getFriends(self):
        """ get friends """
        self.friends = ResultSet(None, 'Friends')

        friendList = self.facebook.friends.get()

        friendList = self.facebook.users.getInfo(friendList[0:5])

        for friend in friendList:

            friendItem = Result(friend['uid'], friend['name'])
            self.friends.addContent(friendItem)
        

    def getGroups(self):
        """ fetches the groups of the user """
        self.groups = ResultSet(None, 'Groups')

        groupList = self.facebook.groups.get()

        for group in groupList:

            newGroup = Result(group['gid'], group['name'])
            self.groups.addContent(newGroup)

    
    def loadAllData(self):
        """ runs all functions to fetch all data """
        self.getFriends()
        self.loadAlbums(1)
        self.getGroups()

    def printAllData(self):
        self.loadAllData()
        ResultSet.printRS(self.friends)
        ResultSet.printRS(self.albums)
        ResultSet.printRS(self.groups)

if __name__ == "__main__":

    
    facebook = FacebookWS()
    facebook.printAllData()

