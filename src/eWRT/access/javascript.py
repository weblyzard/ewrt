#!/usr/bin/env python
'''

'''
import logging
import pyvirtualdisplay

from time import sleep
from selenium import webdriver

from eWRT.access import abstract_retrieve

__version__ = '0.0.8'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SetUpOpenAndTearDown(object):

    def __init__(self, set_up_func, tear_down_func):
        self.set_up_func = set_up_func
        self.tear_down_func = tear_down_func

    def __call__(self, function):
        def _wrapper(*args, **kwargs):

            self.set_up_func(*args, **kwargs)
            function(*args, **kwargs)
            self.tear_down_func(*args, **kwargs)
        return _wrapper



class JavascriptRetriever(abstract_retrieve.AbstractRetriever):
    '''
    Emulates a X screen and controls a Firefox instance.

    For using the JavascriptRetriever you need to install **xvfb**, **xephyr** and **Firefox**.
    The JavascriptRetriever object is a singleton. In order to fully close it,
    please use the method `tear_down()`.

    Usage
        >>> retriever = JavascriptRetriever()
        >>> website_str = retriever.open('http://www.weblyzard.com')
        >>> retriever.tear_down()
    '''
    num_selenium_retrievers = 0
    display = None
    browser = None

    def __init__(self, waiting_time_in_secs=30):
        '''
        :param float waiting_time_in_secs: Describes how long the Firefox should maximally wait until it raises an
                                           exception.
        '''
        self.waiting_time_in_secs = waiting_time_in_secs
        self._initialize_display()


    def _initialize_display(self):
        if not self.display:
            self.display = pyvirtualdisplay.Display()
            self.display.start()

        if not self.browser:
            self.browser = webdriver.Firefox()
            self.browser.implicitly_wait(self.waiting_time_in_secs)
            self.num_selenium_retrievers += 1


    def set_up(self, *args, **kwargs):
        self._initialize_display()


    def tear_down(self, *args, **kwargs):
        '''
        Closes Firefox, X and removes the instance.
        '''
        self.browser.quit()
        self.display.stop()
        del self

    def open(self, url, **kwargs):
        '''
        :param str url: Surf to a given URL and return the source code of the site.
        '''
        self.browser.get(url=url)
        sleep(2)
        return self.browser.page_source

