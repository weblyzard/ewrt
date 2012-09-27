#!/usr/bin/env python
# coding: UTF-8
'''
Created on Oct 6, 2010

@author: johannes
'''

import unittest
import re
import logging
from urlparse import urlparse

import atom

import gdata.youtube
import gdata.youtube.service

CONTENT_TYPE= 'text/wl-plain'
YOUTUBE_MAX_RESULTS_PER_QUERY = 50
YOUTUBE_FEED_LIMIT = 1000 # number of feeds we can collect
AT_RELEVANT_LOCATIONS = ['Vienna, Austria', 'Wien', 'Salzburg', 'Linz',
                         'Klagenfurt', 'Graz', 'Bregenz', 'Eisenstadt',
                         'Innsbruck', 'Bregenz', 'Österreich', 'Niederösterreich',
                         'Oberösterreich', 'Burgenland', 'Steiermark', 'Kärnten',
                         'Tirol', 'Vorarlberg', 'Austria']
logger = logging.getLogger('jonas.youtube')

class YoutubeSchemaHandler(object):
    ''' Class YoutubeSchemaHandler '''

    schemaIdentifier = 'youtube'

    def searchHandler(self, schema_Url):
        ''' generate results for a given schema_Url
        @schema_Url .. the configuration for the search
        @schema_Url['url'] .. includes the search term
        @schema_Url['max_doc'] .. max number of videos to return 
        @schema_Url['max_age'] .. either 'today', 'this_week', 'this_month' or 'all_time' 
        @schema_Url['location_filter'] ..  if given,
            does the location_filter term occur in the videos title, content or keywords? - else skip the vid
        @schema_Url['do_check_relevance'] .. do the relevance check, ie:
            does the search_term occur in the videos title, content or keywords? 

        remark: the API location does not work, because the python api client only supports v1 ---> wait for v2
                see: http://code.google.com/apis/youtube/2.0/migration.html#Location
        '''

        result = [] # all result data in here 
        foundVideoIDs = [] # collect videoIDs to ensure unique results

        self.source_id = schema_Url['source_id']
        self.max_doc = int(schema_Url['max_doc'])
        self.max_age = schema_Url['max_age']
        
        if self.max_age == 0:
            self.max_age = 'all_time'
        elif self.max_age <= 1440:
            self.max_age = 'today'
        elif self.max_age > 1440 and self.max_age <= 10080:
            self.max_age = 'this_week'
        else: 
            self.max_age = 'this_month'
        
        self.do_check_relevance = schema_Url['do_check_relevance']
        #relevance_filter = schema_Url['relevance_filter']

        # urlparse for getting query-term from url 
        search_term = urlparse(schema_Url['url']).path
        search_term = search_term.split('=',1)[1]

        # extract location from url if exists
        pos = search_term.find(' & location=')
        if pos >= 0:
            print 'pos, search_term', pos, search_term
            self.location_filter = search_term[pos + len(' & location='):]
            if self.location_filter.lower()=='austria':
                self.location_filter = AT_RELEVANT_LOCATIONS
            else:
                self.location_filter = [self.location_filter]


            search_term = search_term[:pos]
        else:
            self.location_filter = [] 

        if search_term.find('AND') > 0:
            print "AND is not yet supported"
            # see http://code.google.com/apis/youtube/1.0/reference.html#Query_parameter_definitions
            # on how to add "AND" (vq)
            raise Exception("AND is not yet supported")

        split_terms = re.split('\sOR\s', re.sub('[\(|\)]', '', search_term))
        print "split_terms", split_terms
        # for an OR you need to join the terms with and url-enc "|" symbol 
        # see http://code.google.com/apis/youtube/1.0/reference.html#Query_parameter_definitions
        search_term = "%7C".join(split_terms)
        search_term = "|".join(split_terms)

        print "YoutubeSchemaHandler.searchHandler(): *********** search_term *******", search_term
        print "YoutubeSchemaHandler.searchHandler(): *********** location_filter *******", self.location_filter

        # get yt service instance
        yt_service = gdata.youtube.service.YouTubeService()

        '''construct the youtube query'''
        query = gdata.youtube.service.YouTubeVideoQuery()
        query.vq = search_term
        query.max_results = YOUTUBE_MAX_RESULTS_PER_QUERY 
        query.orderby = 'relevance'
        query.time = self.max_age
        # location is not yet working properly --> see in doc_string
        #query.location = '-77.02,38.53'  
        #query.location = '51.49757766723633,-0.12958288192749023'
        #query.location = 'Washington'
        #query.location_radius = '10000km'

        # start values for iterative generation of result-set
        start_index, counter = 1, 0
        query.start_index = start_index
        continue_querying = True

        # while we have results and counter<self.max_doc
        while continue_querying:

            '''execute the query'''
            feed = yt_service.YouTubeQuery(query)

            if feed.entry:

                '''feed containing video data'''
                for f in feed.entry:
            
                    videoData = self.extract_data_from_feed(f)

                    # uniqueness check 
                    if videoData['id'] in foundVideoIDs:
                        continue # we already got this vid, skip
                    foundVideoIDs.append(videoData['id'])

                    # location filter check ?
                    if self.location_filter and not self.check_occurs(videoData, self.location_filter):
                        continue # skip this vid ..

                    # relevance check ?
                    if self.do_check_relevance and not self.check_occurs(videoData, split_terms):
                        continue # skip this vid ..

                    # --------- all good -------- we will use this data -------------------- ##
                    # get and append comments
                    try: 
                        comment_feed = yt_service.GetYouTubeVideoCommentFeed(video_id=videoData['id'])
                    except Exception,e:
                        print "ERROR on fetching GetYouTubeVideoCommentFeed for id %s, will skip it" % videoData['id']
                        continue
                    for cf in comment_feed.entry:
                        videoData['comments'].append(cf.content.text)


                    # append video data to result
                    result.append(videoData)

                    # new vid added, increase counter
                    counter += 1
                    print "Current number of feeds: %d" % counter 

                    if counter>=self.max_doc:
                        print "Stopping because counter (%d) > max_doc(%d)" % (counter, self.max_doc)
                        return result # CAUTION -- return in here


                # raise start index for next batch of results    
                start_index += 50
                query.start_index = start_index
                print "Set start index to %d" % start_index

                if start_index >= YOUTUBE_FEED_LIMIT:
                    continue_querying = False

            else:
                print "No more results found, current start_index: %d" % start_index
                continue_querying = False

        return result

    def extract_data_from_feed(self, f): 
        ''' save all the relevant data from the video into the videoData dict 
            @param f  ... the video feed
        '''


        print "\n-------------- in extract_data_from_feed() ------------------"

        videoData = {}

        # extract first thumbnail as picture
        try:
            # info: <ns0:thumbnail height="90" time="00:02:17" url="http://i.ytimg.com/vi/m5f_lth7zdA/2.jpg" width="120" xmlns:ns0="http://search.yahoo.com/mrss/" /
            videoData['picture'] = f.media.thumbnail[0].url
        except:
            videoData['picture'] = ''

        duration = int(f.media.duration.seconds)
        if duration>0:
            # transform to min:sec
            videoData['duration'] = "%d:%02d" % (duration/60, duration%60)
            print "xxxxxxxxxxxxxX", duration, videoData['duration']

        # capture some basic data
        videoData['source_id'] = self.source_id 
        videoData['content_type'] = CONTENT_TYPE
        videoData['source'] = self.schemaIdentifier 
        videoData['encoding'] = 'utf8' 
        videoData['max_doc'] = self.max_doc 
        videoData['max_age'] = self.max_age
        videoData['location'] = []
        videoData['comments'] = []
        videoData['content'] = f.media.description.text

        if type(f.media.description.text) != type(''):
            print "INFO, content is not of type text. content: ", f.media.description.text
            videoData['content'] = ""

        videoData['id'] = f.id.text.split('/')[-1]
        videoData['url'] = "http://www.youtube.com/watch?v=" + videoData['id']
        videoData['title'] = f.title.text
        videoData['updated'] = f.updated.text
        videoData['last_modified'] = f.updated.text
        videoData['published'] = f.published.text
        videoData['user_name'] = f.author[0].name.text
        videoData['yt_source'] = f.source 
        videoData['source'] = self.schemaIdentifier
        videoData['rights'] = f.rights
        videoData['summary'] = f.summary
        videoData['keywords'] = []

        # extension_elements ...
        for el in f.extension_elements:
            if el.tag == 'location':
                videoData['location'].append(el.text)
            #if el.tag == 'description':
            #    videoData['description'] = el.text

        # get the related videos feed url
        for i in f.link:
            if i.href.endswith('related'):
                videoData['related_url'] = i.href


        # get statistics
        if not f.statistics is None:
            videoData['statistics_viewcount'] = f.statistics.view_count
            videoData['statistics_favoritecount'] = f.statistics.favorite_count

        # get rating stuff
        if not f.rating is None:
            videoData['rating_average'] = f.rating.average
            videoData['rating_max'] = f.rating.max
            videoData['rating_min'] = f.rating.min
            videoData['rating_numraters'] = f.rating.num_raters

        # extract keywords
        for category in f.category:
            if 'http://gdata.youtube.com/schemas' not in category.term:
                videoData['keywords'].append(category.term)

        return videoData

 
    def check_occurs(self, videoData, search_terms):
        '''
        check the relevance of a videoData entry -- does the search_term occur in the videos title, content or keywords?
        @param videoData 
        @param search_terms: list of searching term
        @returns Boolean
        '''
        for search_term in search_terms:

            if isinstance(videoData['title'], str):
                videoData['title'] = videoData['title'].decode(videoData['encoding'])
    
            if search_term.lower() in videoData['title'].lower():
                print 'check_occurs(): title (%s) includes search_term (%s)' % (videoData['title'], search_term)
                return True
            
            
            if videoData.has_key('content') and videoData['content']:
                
                if isinstance(videoData['content'], str):
                    videoData['content'] = videoData['content'].decode(videoData['encoding'])
                
                if search_term.lower() in videoData['content'].lower():
                    print 'check_occurs(): content (%s) includes search_term (%s) ' % (videoData['content'], search_term)
                    return True

            for word in videoData['keywords']:
                
                if isinstance(word, str):
                    word = word.decode(videoData['encoding'])
                
                if search_term.lower() in word.lower():
                    print 'check_occurs(): keywords (%s) include search_term (%s)' % (videoData['keywords'], search_term)
                    return True

        print 'check_occurs(): did not find one of terms (%s) in title, content or keywords' % str(search_terms)
        return False


    def recurse_into_related_videos(self, related_url):
        """def get_related_contents(self, related_url, yt_service, source_id, self.max_doc, max_age, content_type):
        @param url: url to related contents, as RSS Feed
        CAUTION -- this is not fully implemented -- just a pre-alpha version! 
        """
   
        feeds = feedparser.parse(related_url)

        for entry in feeds.entries:
                keyword_list = []
                for k,v in entry.iteritems():
                    #print k
                    if k == 'id':
                        print k, v
                        vid = v
                    elif k == 'title':
                        print k, v
                        title = v
                    elif k == 'author':
                        print k, v
                        author = v
                    elif k == 'published':
                        print k, v
                        published = v
                    elif k == 'yt_location':
                        print k, v
                        yt_location = v
                    elif k == 'media_keywords':
                        print k, v
                        media_keywords = v
                    elif k == 'media_description':
                        print k, v
                        content = v
                            
                    try:
                        for i in v:
                            if type(i) == feedparser.FeedParserDict:
                                related_link =  i['href']
                                #print related_link
                                if 'feature=youtube_gdata' in str(related_link):
                                    print 'URL:', str(related_link)
                                    link = str(related_link).split('http://www.youtube.com/watch?v=')
                                    link[1] = str(link[1]).split('&feature')
                                    comment_feed = yt_service.GetYouTubeVideoCommentFeed(video_id = link[1][0])
                                    print 'Comments:'
    
                                    for cf in comment_feed.entry:
                                        comments.append(cf.content.text.encode('utf8'))        
                                    print self.comments
                    except:
                        pass
                    
                if(self.check_vid(vid,self.result) == True):
                    print 'None'
                    self.result.append({'source_id': source_id, 'vid': vid, 'max_doc': self.max_doc,'title': title, 'content_type': CONTENT_TYPE, 
                        'url': related_link ,'last_modified': published,'content': comments, 'type':'youtube',
                        'encoding': 'utf8', 'screen_name': author, 'media_keywords': media_keywords, 'yt_location': yt_location, 'content': content})
                      
        return self.result             



class Test(unittest.TestCase):

    def setUp(self):
        self.youtube = YoutubeSchemaHandler()

    def testGetHeinzVideo(self):
        ''' check if we get Heinz' very amazing video '''

        url = {'url':'youtube://search?term=m5f_lth7zdA', 'source_id':123, 'max_doc':10, 'max_age':'all_time', 'do_check_relevance': False}
        result = self.youtube.searchHandler(url)
        assert len(result) == 1

    def testGet_5_Obama_Video_From_Today(self):
        """ test getting exactly 5 videos for "obama" with max_age=='today' and do_check_relevance==True """

        url = {'url':'youtube://search?term=obama', 'source_id':123, 'max_doc':5, 'max_age': 'today', 'do_check_relevance': True}
        assert len(self.youtube.searchHandler(url)) == 5

    def testGet_5_Obama_Video_From_today_with_location(self):
        """ test getting exactly 5 videos for "obama" with max_age=='today' and do_check_relevance==True """

        url = {'url':'youtube://search?term=obama & location=USA', 'source_id':123, 'max_doc':5, 'max_age': 'today', 'do_check_relevance': True}
        assert len(self.youtube.searchHandler(url)) == 5

        url = {'url':'youtube://search?term=obama & location=Washington', 'source_id':123, 'max_doc':5, 'max_age': 'today', 'do_check_relevance': True}
        assert len(self.youtube.searchHandler(url)) == 5
        
    def testGet_wkw_with_location(self):
        """ test getting exactly 5 videos for "obama" with max_age=='today' and do_check_relevance==True """

        url = {'url':'youtube://search?term=(polizei OR bildung) & location=Austria', 'source_id':123, 'max_doc':5, 'max_age': 'this_month', 'do_check_relevance': True}
        res = self.youtube.searchHandler(url)
        print res
        assert len(res) == 5

        url = {'url':'youtube://search?term=(wirtschaftskammer wien OR bildung)', 'source_id':123, 'max_doc':5, 'max_age': 'this_month', 'do_check_relevance': True}
        assert len(self.youtube.searchHandler(url)) >= 1

 
    def testCheckRelevanceFunction(self):
        ''' make sure the check_relevance function works '''

        # test for found
        videoData = {'title': 'bla', 'content': ' Open Office von Prof. Rony Flatscher', 'keywords': ['nerds']}
        search_terms = ['rony flatscher']
        assert self.youtube.check_occurs(videoData, search_terms)

        # test for not found
        videoData = {'title': 'bla', 'content': 'nix', 'keywords': ['nerds']}
        search_terms = ['rony flatscher']
        assert self.youtube.check_occurs(videoData, search_terms) == False


    #def testGetRelatedContents(self):
    #    ''' related url functionality not in use atm '''
    #    print 'start getrelatedcontents test'
    #    self.testGetData()
    #    related_url = 'http://gdata.youtube.com/feeds/videos/T13ZAdne6TU/related'
    #    yt_service = gdata.youtube.service.YouTubeService()
    #    source_id = '123'
    #    max_doc = '11'
    #    max_age = '100'
    #    content_type = 'text/wl-plain'
    #    results = self.youtube.get_related_contents(related_url, yt_service, source_id, max_doc, max_age, content_type)
    #    print 'related_results', results
    #    assert len(results) > 0'''


if __name__ == "__main__":
    unittest.main()
