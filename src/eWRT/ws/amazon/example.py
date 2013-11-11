#!/usr/bin/env python

""" an example script querying book reviews from the amazon
    database """

# (C)opyrights 2008 by Albert Weichselbraun <albert@weichselbraun.net>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

MAX_PAGES_TO_PARSE = 10
from eWRT.ws.amazon import AmazonWS, ResultList

def getReview( asin_list ):
	""" returns the reviews for the given asins """
	a=AmazonWS()

	for asin in asin_list:
		result=[]
		for page in xrange(MAX_PAGES_TO_PARSE):
			xmlOutput = a.queryReview( asin, ReviewPage=str(page+1) )
			xmlParser  = ResultList("ItemLookupResponse/Items/Item/CustomerReviews/Review", hunt=("TotalReviewPages",))
			xmlParser.parse( xmlOutput )
			result.extend( xmlParser.xmlResult )

			print("%s: page %s/%s" % (asin, page+1,xmlParser.huntValue.get('TotalReviewPages',0)))
			if page+1 >= int(xmlParser.huntValue.get('TotalReviewPages',0)):
				break


		for review in result:
			review['Summary']=review['Summary'].replace("'", "\\'")
			review['Content']=review['Content'].replace("'", "\\'")
			if not "CustomerId" in review: 
				print("Skipping record\n")
				continue
			print "INSERT INTO Review (asin,customerId,rating,helpfulVotes,totalVotes,date,summary,content) VALUES('%(ASIN)s', '%(CustomerId)s', %(Rating)s, %(HelpfulVotes)s, %(TotalVotes)s, '%(Date)s', '%(Summary)s', '%(Content)s');" % (review)

def exportTopBooks( number  ):
	""" exports the top 'number' books from amazon """

	a = AmazonWS()
	result=[]
	for page in xrange(number/10):
		xmlOutput = a.searchItem( ItemPage=str(page+1) )
		xmlParser = ResultList("ItemSearchResponse/Items/Item")
		xmlParser.parse( xmlOutput )
		result.extend( xmlParser.xmlResult )
	
	for dataSet in result:
		dataSet['Title'] = dataSet['Title'].replace("'", "\\'")
		if len(dataSet['ASIN'])<10: continue
		assert( len(dataSet['ASIN'])==10 )
		print "INSERT INTO Book2 (asin,salesrank,title,detailPageUrl) VALUES ('%(ASIN)s', %(SalesRank)s, '%(Title)s', '%(DetailPageURL)s');" % (dataSet)
	

# retrieve the reviews for the given asins
asin_list = ('0385523416', '1592764053', 'B0013HA824') 
getReview( asin_list )

# exports the 10 top books from amazon
exportTopBooks(10)
