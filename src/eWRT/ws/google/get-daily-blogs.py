# Blog search Script
# Author: reinhard.fischer@modul.ac.at
# Date: 2008-10
#
# Performs a blog search engine search on the given keywords
# and writes them into a database/text file
# designed for daily use ;-)
#

# for the parameters
import optparse, logging
import string 
import urllib
import os,sys,re
import pg
import time
import urllib
import datetime
from xml.dom.minidom import parse, parseString
from eWRT.ws.technorati import Technorati

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout )

# sets the parameters
def get_my_parameters():
  usage = "usage: %prog [options] keywords (enclosed in apostrophes if word groups)"
  p = optparse.OptionParser(usage=usage)
  p.add_option('-s', '--sampleid', help="the sample-id for which the URLs are retrieved", action="store", dest="sampleid", default="-1")
  p.add_option('-t', '--technorati', help="set if you want to search using technorati blog search", action="store_true", dest="search_technorati")
  p.add_option('-g', '--google', help="set if you want to search using google blog search", action="store_true", dest="search_google")  
  p.add_option('--nodb', help="use if URLs should NOT be written into the database", action="store_true", dest="db_no_insert")
  p.add_option('-e', '--email', help="email-address which gets error message if any occur", action="store", dest="email")
  p.add_option('-m', '--max-results', help="max number of results per keyword, default=1000", action="store", dest="max_results", default="10")
  p.add_option('-f', '--filename', help="file to write urls into, default=urllist.txt", action="store", dest="file_urls", default="urllist.txt")
  (options, arguments) = p.parse_args()
  
  # Set list of keywords
  my_debug("Keywords: ", "keywords")
  my_debug(arguments, "keywords")
  return (options, arguments)

# For debugging
# In order not to print out everything all the time
def my_debug(text, priority_name, priority = 1, write_mail_anyway = 0):
  global debug_priority_array
  global debug_priority_limit
  global log_text
  
  logging.debug(text)
  
# TODO: check if I need something from here
#  #log_text = log_text + str(text) + "\n"
#
#  for print_priority in debug_priority_array:
#    if (priority_name == print_priority) and (priority >= debug_priority_limit):
#      print "[%s][%d]" % (priority_name, priority), text
#      break
#  if write_mail_anyway != 0:
#    #print "remembering"
#    remember_to_write_mail(write_mail_anyway)
#  #else:
#    #print "not remembering"

# For debugging
# Just remember whether we should write a mail anyway
def remember_to_write_mail(tellme = 0, remember_me=[0]):
  if tellme != 0:
    remember_me[0] = 1
  if remember_me[0] != 0:
    return 1
  return 0

# Search using a generic Blog Search Engine
# Currently works with Google (Web) and Technorati (API)
def search_any_provider_minidom(engine_name, max_results, keyword_list, sampleid, search_url, start_url_part, limit_url_part, page_result_limit, number_of_tries, item_tag, url_tag, result_number_tag, authority_tag, abstract_tag):
  url_list = []

  # one search per keyword
  my_debug("Starting with %s" %engine_name, "minidom")
  for keyword in keyword_list:
    my_debug("Keyword %s " % keyword, "minidom")
    my_debug("Looking for %d results" % max_results, "minidom")
    result_start = 1
    result_page_data = parseString('<?xml version="1.0" encoding="utf-8"?><query>climate change</query>');
    last_result_page = result_page_data
    # We retrieve several result pages
    # we have to stop if
    # 1) an empty page is retrieved
    # 2) We got the needed number of results
    # 3) The page has the same result as the last one (Technorati-specific-stuff) - means that there are no more results
    while (max_results > 0):
      my_debug("Result number %s" % result_start, "minidom")
      current_result_page = search_url + urllib.quote_plus(keyword) + start_url_part + str(result_start) + limit_url_part + str(page_result_limit)
      my_debug("URL: %s" % current_result_page, "minidom")
# Retrieve the page with the results
      # We have to check several times as technorati sometimes gives back pages without results
      result_number = 1
      for current_try in range(1,number_of_tries):
        try:
          result_page_raw = str(urllib.urlopen(current_result_page).read())
          result_page = result_page_raw.replace("\n", " ").strip()
        except:
          break
        # Check if we found someting
        try:
          result_page_data = parseString(result_page)
        except:
          my_debug("Could not parse XML doc passed", "minidom", 100,1)
          break
        my_debug("Parsing worked", "minidom")
        try:
          print result_page_data.toxml() # wohlg -- moved this inside the try-except clause
          result_number_array = result_page_data.getElementsByTagName(result_number_tag)
        except:
          my_debug("XML Doc does not seem alright", "minidom", 100,1)
          break
        if len(result_number_array) > 0:
          results_c = re.compile("\d+")
          result_number = int(results_c.findall(result_number_array[0].firstChild.data.replace(",", ""))[0])
          my_debug("Number of results (check): %s" % result_number, "minidom")
          break
        else:
          time.sleep(1 * current_try ** 2)
          my_debug("Problems getting page - try %d of %d" % (current_try, number_of_tries), "error", 10)
          continue
      my_debug("Retrieved URL %s" % current_result_page, "minidom")
      # check repeating pages --> if yes, we can stop (no more new results)
      if last_result_page == result_page_data:
        my_debug("No more results (page comparison)", "minidom")
        max_results = 0
      elif (result_start > result_number):
        my_debug("No more results (Start %s, Count %s)." % (result_start, result_number), "minidom")
        max_results = 0
      else:
        # Nothing went wrong --> we can parse out the results
        for item in result_page_data.getElementsByTagName(item_tag):
          url = item.getElementsByTagName(url_tag)[0].firstChild.data
          my_debug("URL: %s" % url, "minidom")
          if url:
            current_url = {}
            current_url_no_u = {}
            current_url['url'] = url[len(url) -1]
            current_url['url'] = url
            current_url['source'] = engine_name + ' - Keyword "%s"' % keyword
            my_abstract = item.getElementsByTagName(abstract_tag)[0].firstChild.data
            current_url['abstract'] = my_abstract[0:99]
            #my_debug("Abstract: %s" % my_abstract[0:99], "minidom")
            if len(authority_tag) > 0 :
              current_url['authority'] = item.getElementsByTagName(authority_tag)[0].firstChild.data
              my_debug("Authority: %s" % item.getElementsByTagName(authority_tag)[0].firstChild.data, "minidom")
            else:
              current_url['authority'] = "-1"
            current_url['reach'] = '0'
            current_url['sampleid'] = sampleid
            max_results -= 1
            my_debug(current_url, "minidom")
            my_debug("Still looking for %d results" % max_results, "crawl-detail")
            for key in current_url.keys():
              if isinstance(current_url[key], unicode):
                current_url_no_u[key] = current_url[key].encode('utf-8', 'ignore').strip()
              else:
                current_url_no_u[key] = current_url[key].strip()
            my_debug(current_url, "minidom")
            url_list.append(current_url_no_u)
            if max_results < 1:
              break
          else: #no url found
            my_debug("Not found", "crawl-detail")
        my_debug("Next page", "minidom")
        result_start += page_result_limit
        last_result_page = result_page_data
    if len(url_list) == 0:
      my_debug("Number of results for Keyword: %s" % len(url_list), "minidom", 100, 1)
    else:
      my_debug("Number of results for Keyword: %s" % len(url_list), "minidom")
  return url_list


# Search using a generic Blog Search Engine
# Currently works with Google (Web) and Technorati (API)
def search_any_provider(engine_name, max_results, keyword_list, sampleid, search_url, start_url_part, limit_url_part, page_result_limit, number_of_tries, split_regexp, url_regexp, result_number_regexp, authority_regexp, abstract_regexp):
  
  # Initialize needed values
  url_regexp_c = re.compile(url_regexp)
  split_regexp_c = re.compile(split_regexp)
  result_number_regexp_c = re.compile(result_number_regexp)
  if len(authority_regexp) > 0 : authority_regexp_c = re.compile(authority_regexp)
  abstract_regexp_c = re.compile(abstract_regexp)
  
  page_list = []
  url_list = []

  # one search per keyword
  my_debug("Starting with %s" %engine_name, "raw")
  for keyword in keyword_list:
    my_debug("Keyword %s " % keyword, "raw")
    my_debug("Looking for %d results" % max_results, "raw")
    result_start = 1
    last_result_page = ""
    # We retrieve several result pages
    # we have to stop if
    # 1) an empty page is retrieved
    # 2) We got the needed number of results
    # 3) The page has the same result as the last one (Technorati-specific-stuff) - means that there are no more results
    while (max_results > 0): 
      my_debug("Result number %s" % result_start, "raw")
      current_result_page = search_url + urllib.quote_plus(keyword) + start_url_part + str(result_start) + limit_url_part + str(page_result_limit)
      
      
      #print "Retrieving URL %s" % current_result_page
      # Retrieve the page with the results
      # We have to check several times as technorati sometimes gives back pages without results
      for current_try in range(1,number_of_tries+1):
        my_debug("Downloading - try %d of %d" % (current_try, number_of_tries), "raw", 10)
        result_number = 1
        time.sleep(1 * current_try ** 2)
        result_page_file = urllib.urlopen(current_result_page)
        result_page_data_temp = result_page_file.read()
        if isinstance(result_page_data_temp, unicode):
          my_debug("UTF: %s " % [result_page_data_temp], "raw", 10)
          result_page_data = result_page_data_temp.encode('utf-8', 'ignore').strip()
        else:
          my_debug("Normal: %s " % [result_page_data_temp], "raw", -1)
          result_page_data = result_page_data_temp.decode('utf-8', 'ignore').strip()
        result_number_array = result_number_regexp_c.findall(result_page_data)
        my_debug(result_number_array, "raw")
        my_debug("Document length: %d" % len(result_page_data), "raw")
        if len(result_number_array) > 0:
          my_debug("Google Check: %s" % result_number_array[0], "raw")
          results_regexp_c = re.compile("\d+")
          result_number = int(results_regexp_c.findall(result_number_array[0].replace(",", ""))[0])
          my_debug("Number of results (check): %s" % result_number, "raw")
          break
        else:
          my_debug("Problems receiving page - try %d of %d" % (current_try, number_of_tries), "raw")
      my_debug("Retrieved URL %s" % current_result_page, "raw")
      # check repeating pages --> if yes, we can stop (no more new results)
      if last_result_page == result_page_data:
        my_debug("No more results (page comparison).", "raw")
        max_results = 0
        break
      elif (result_start > result_number):
        my_debug("No more results (Start %s)." % result_start, "raw")
        my_debug("No more results (Count %s)." % result_number, "raw")
        max_results = 0
        break
      else:
        # Nothing went wrong --> we can parse out the results
        # . does not match \n in regexps by default
        result_page_data = result_page_data.replace("\n", " ");
        # Get the single entries
        search_results = split_regexp_c.findall(result_page_data)
        #return url_list
        my_debug("splitting %s" % split_regexp, "raw")
        #print result_page_data
        #print search_results
        my_debug(len(search_results), "raw")
        for item in search_results:
          #print item
          url = url_regexp_c.findall(item)
          if url:
            current_url = {}
            current_url_no_u = {}
            current_url['url'] = url[len(url) -1]
            current_url['source'] = engine_name + ' - Keyword "%s"' % keyword
            my_abstract = abstract_regexp_c.findall(item)[0]
            current_url['abstract'] = my_abstract[0:99]
            if len(authority_regexp) > 0 :
              current_url['authority'] = authority_regexp_c.findall(item)[0]
            else:
              current_url['authority'] = "-1"
            current_url['reach'] = '0'
            current_url['sampleid'] = sampleid
            max_results -= 1
            my_debug(current_url, "raw")
            my_debug("Still looking for %d results" % max_results, "raw")
            for key in current_url.keys():
              if isinstance(current_url[key], unicode):
                my_debug("UTF: %s " % [current_url[key]], "raw", 10)
                current_url_no_u[key] = current_url[key].encode('utf-8', 'ignore').strip()
              else:
                my_debug("Normal: %s " % [current_url[key]], "raw", 10)
                current_url_no_u[key] = current_url[key].decode('utf-8', 'ignore').strip()
            url_list.append(current_url_no_u)
            if max_results < 1:
              break
          else:
            my_debug("Not found", "raw")
        result_start += page_result_limit
        last_result_page = result_page_data
        #print "Still looking for %d results" % max_results
    my_debug("Number of results for Keyword: %s" % len(url_list), "raw")
  return url_list

# Writes the retrieved URLs into the log file
def write_urls_file(write_filename, url_list, write_append):
  global error_text
  if write_append != 0:
    write_mode = "a"
  else:
    write_mode = "w"
  try:
    write_file = open(write_filename, write_mode)
    for url in url_list:
      mytimestamp = datetime.datetime.now()
      url['timestamp'] = mytimestamp.strftime("%y-%m-%d %H:%M")
      write_file.write(str(url) + "\n")
  except IOError:
    error_text += "Error:  Couldn\'t write file.\n"
    return 1
  my_debug("File successfully written: %s lines." % len(url_list), "file", 10)
  write_file.close()
  return 0

# Writes the retrieved URLs into the DB
def write_urls_database(url_list, sampleId=0):
  global error_text
  # Try to connect
  try:
    pg_con = pg.connect('weblyzard', 'gecko3.wu-wien.ac.at', 5432, None, None, 'rfischer', 'xAoo320lx')
    #conn=psycopg2.connect("server='gecko3.wu-wien.ac.at' dbname='weblyzard' user='rfischer' password='xAoo320lx'")
  except:
    error_text += "I am unable to connect to the database, exiting.\n"
    return 1
  counter = 0
  for url in url_list:
      
    if not url.has_key('sampleid'):
        url['sampleid'] = sampleId
      
    try:
      counter += 1
      # Check if url is already in db
      my_debug(("SELECT * FROM url_stack_for_mirroring WHERE url='%s' AND abstract='%s' " % ( pg.escape_string(str(url['url'])), pg.escape_string(str(url['abstract']) ))), "database", 4)
      check_existing_url = pg_con.query("SELECT * FROM url_stack_for_mirroring WHERE url='%s' AND abstract='%s' " % ( pg.escape_string(str(url['url'])), pg.escape_string(str(url['abstract']) )))
      #my_debug("check existing 1", "database")
      my_debug("Checking if we got a result", "database", 4)
      if check_existing_url.ntuples() > 0:
        my_debug("[%s] Check - Found: %s" % (counter, url['url']), "database", 6)
        continue
      else:
        my_debug("[%s] Check - NOT Found: %s" % (counter, url['url']), "database", 6)
      #else:
        #my_debug("check existing 3a", "database")
      print url
#      sql_insert = "INSERT INTO url_stack_for_mirroring (url, date, source, authority, reach, sample_id, abstract) VALUES ('%s', LOCALTIMESTAMP, '%s', '%s', '%s', '%s', '%s')" % ( pg.escape_string(url['url']), pg.escape_string(url['source']), pg.escape_string(url['authority']), pg.escape_string(url['reach']), pg.escape_string(url['sampleid']), pg.escape_string(str(url['abstract'])) )
      sql_insert = "INSERT INTO url_stack_for_mirroring (url, date, source, authority, reach, sample_id, abstract) VALUES ('%s', LOCALTIMESTAMP, '%s', '%s', '%s', '%s', '%s')"
      sql_insert = sql_insert % ( url['url'], url['source'], url['authority'], url['reach'], url['sampleid'], str(url['abstract']) )
      logging.debug(sql_insert)
      pg_con.query(sql_insert)
    except:
#      error_text += "Cannot write into database: %s .\n" % sys.exc_type
      logging.error("Cannot write into database : %s .\n" % sys.exc_type)
      print sys.exc_info()
      return 1
  my_debug("SQL successfully updated\n", "database", 7)
  return 0

# Writes an email to the email address specified in the options if errors occur
def write_error_mail(options, err_msg):
  global error_text
  global log_text
  
  SENDMAIL = "/usr/sbin/sendmail" # sendmail location
  p = os.popen("%s -t" % SENDMAIL, "w")
  p.write("To: %s \n" % options.email)
  p.write("Subject: Daily Blog Crawl Error\n")
  p.write("\n") # blank line separating headers from body
  p.write(err_msg)
  p.write("\n" + log_text)
  sts = p.close()
  if sts > 0:
    logging.error("Sendmail exit status " + sts)
    return 1
  my_debug("Email successfully sent\n", "error", 3)
  return 0

# Writes the retrieved URLs into the log file
def write_error_file(write_filename, error_msg):
  write_mode = "w+"
  try:
    write_file = open(write_filename, write_mode)
    write_file.write(error_msg + "\n")
  except IOError:
    my_debug("Error:  Couldn\'t write file.\n", "error", 100)
    return 1
  write_file.close()
  return 0

def mainNew():
    ''' new method for retrieving the daily blogs '''

    global error_text
    global log_text
    global debug_priority_array
    global debug_priority_limit

    (options, arguments) = get_my_parameters()
#    print arguments
    url_list = Technorati.get_blog_links(arguments[0], maxResults=int(options.max_results))
    succ = 0
    if len(url_list) == 0:
        
        logging.error('Did not fetch any URLs')
        
#        try:
#            raise SNMPException("webLyzard.experimental", "Error fetching URLs of daily blogs.", level="warning")
#        except SNMPException:
#            logging.error('Did not fetch any URLs!')
#        
    elif options.db_no_insert != 1:
        succ += write_urls_database(url_list, options.sampleid)
        
    logging.info("Finishing: Blogs found: %d " % len(url_list))


#def main():
#  try:
#    global error_text
#    global log_text
#    global debug_priority_array
#    global debug_priority_limit
#    
#    # debug_priority contains the priority strings which will be printed
#    debug_priority_array = ("keywords", "abstract", "database", "crawl-detail", "minidom", "error", "raw")
#    #debug_priority_array = ("error", "raw")
#    debug_priority_limit = 0
#    
#    succ = 0
#    error_text = ""
#    log_text = ""
#    url_list = []
#    
#    # Get parameters, set variables
#    (options, arguments) = get_my_parameters()
#    
#    if options.search_technorati == True:
#      url_list.extend(search_any_provider_minidom("Technorati Blog Search (API)", int(options.max_results), arguments, options.sampleid, "http://api.technorati.com/tag?key=1eb5dd8869e7e5b5742da05aae33e07e&tag=", "&start=", "&limit=", 100, 5, "item", "permalink", "postsmatched", "inboundlinks", "excerpt" ))    
#    if options.search_google == True:
#      url_list.extend(search_any_provider("Google Blog Search (Web)", int(options.max_results), arguments, options.sampleid, "http://blogsearch.google.com/blogsearch?hl=en&lr=&ie=UTF-8&sa=N&q=", "&start=", "&num=", 100, 2, '(<a href=.*?</a>.*?<a href=.*?</a></font></td></tr></table><p class=g>)', "<a href=\"([^\"]*)\"", '<td align=right class=rsb><font color="" size="-1">Results <b>[0-9\,]*</b> - <b>[0-9\,]*</b> of about <b>([0-9\,]*)</b>', "", "<br><font size=-1>(.*?)<br></font>" ))
#  
#    # if there are results
#    #url_list = set(url_list)
#    if len(url_list) > 0:
#      # write results into file just in case
#      succ = write_urls_file(options.file_urls, url_list, 1)
#      if options.db_no_insert != 1:
#        succ += write_urls_database(url_list)
#      my_debug("Finishing: Blogs found: %d " % len(url_list), "error", 100)
#    else:
#      my_debug("Finishing: no URLs found", "error", 100, 1)
#    if succ > 0:
#      my_debug("Checking if I have to write mails...", "error", 100, succ)
#      if remember_to_write_mail() > 0:
#        if len(options.email) > 0:
#          write_error_mail(options, error_text)
#        write_error_file('/home/rfischer/daily-blog-crawl/error.txt', error_text)
#        my_debug(error_text, "error", 100)
#  except:
#    if len(options.email) > 0:
#      error_text += str(sys.exc_info()[0])
#      write_error_mail(options, error_text)
#    write_error_file('/home/rfischer/daily-blog-crawl/error.txt', error_text)
#    my_debug(error_text, "error", 100)
#    raise

if __name__ == '__main__':
  mainNew()
