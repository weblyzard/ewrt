#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
EmailParser
===========
EmailParser supplies the following methods:
* EmailParser.parse(): extract the recipient, the subject, the payload and all
  valid urls from an email string.
  
*Note*: Please always follow PEP8.

@author: Philipp Konrad
'''
import email
import unittest
import re
import doctest

class EmailParser(object):
    '''Please refer to the classmethod `EmailParser.parse()`.'''
    
    @classmethod
    def parse(cls, string_message):
        '''
        EmailParser.parse()
        ===================
        The classmethod takes a string representing an email and returns
        all containing urls in a list::
        
        >>> email_string = open('test_googlealert/test1', 'r').read()
        >>> parsed_data = EmailParser.parse(email_string)
        >>> parsed_data['urls']
        ['http://www.militaryaerospace.com/articles/2013/03/DARPA-machine-learning.html']
        
        Another possibility is to parse a whole email and it's content.
        The library returns a dictionary with the fields `urls` and 
        `email_body`::
        
        >>> email_string = open('test_googlealert/test2', 'r').read()
        >>> parsed_data = EmailParser.parse(email_string)
        >>> parsed_data['urls']
        ['http://www.wu.ac.at', 'http://www.tuwien.ac.at/en/']
        >>> parsed_data['email_payload']
        'This is an email body.'
        
        Finally, the classmethod's returned dictionary contains an 
        `email_subject` key and an `email_recipient`::
        
        >>> email_string = open('test_googlealert/test3', 'r').read()
        >>> parsed_data = EmailParser.parse(email_string)
        >>> parsed_data['email_subject']
        'Very important news!'
        
        >>> parsed_data['email_recipient']
        'bicycle_repair_man@pythonmail.com'
        '''
        parsed_message = email.message_from_string(string_message)
        returned_data = dict()
        valid_urls = None
        
        if cls._is_email(parsed_message):
            email_payload = parsed_message.get_payload()
            valid_urls = cls._find_valid_urls(email_payload)
            
            returned_data['email_subject'] = parsed_message['subject']
            returned_data['email_recipient'] = parsed_message['To']
            returned_data['urls'] = valid_urls
            returned_data['email_payload'] = cls._clean_payload(email_payload,
                                                                valid_urls)
        else:
            raise TypeError('The supplied string is not a valid email.')

        assert len(returned_data) == 4
        return returned_data
    
    @classmethod
    def _is_email(cls, possible_email_obj):        
        try:
            if '@' in possible_email_obj['To']:
                is_email = True     
        except TypeError, e:
            is_email = False
                
        return is_email
    
    @classmethod
    def _url_is_from_google(cls, url):        
        return url.startswith('http://news.google') or \
                url.startswith('http://www.google')
    
    @classmethod
    def _find_valid_urls(cls, email_payload):
        found_urls = re.findall('(http://.*)', email_payload)
        
        retval = []
        for url in found_urls:
            if not cls._url_is_from_google(url):
                if url.endswith('>'):
                    retval.append(url.rstrip('>'))
                else:                      
                    retval.append(url)
                
        return retval

    @classmethod
    def _clean_payload(cls, email_payload, urls_to_clean):
        
        returned_string = []
        
        # iterate over email payload and only add lines without url to 
        # returned body.
        for line in email_payload.splitlines():
            
            for url in urls_to_clean:
                if url in line or 'http://' in line:
                    break
            else:
                returned_string.append(line)
                
        return '\n'.join(returned_string)

if __name__ == '__main__':
    doctest.testmod()
    