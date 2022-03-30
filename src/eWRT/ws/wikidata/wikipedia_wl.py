#!/usr/bin/python
"""
Last modified: Sept. 9 2018
@author: Jakob Steixner, jakob.steixner@modul.ac.at

Wrapper around the [`wikipedia` package](https://pypi.org/project/wikipedia/)
See also [GitHub](https://github.com/goldsmith/Wikipedia/).

Introduces a `@property` revision_timestamp.

Note: the [MediaWikiAPI-fork](https://github.com/lehinevych/MediaWikiAPI/)
of this package seems to be more actively maintained nowadays, but it doesn't
ship with a timestamp-attribute either. Both are licensed with the MIT license.
"""
import requests

from wikipedia import (WikipediaPage as WikipediaPageDef, PageError, search, API_URL)


class WikipediaPage(WikipediaPageDef):

    @property
    def revision_timestamp(self):
            '''
            Timestamp of most recent revision of Wikipedia page.
            '''
            params = {'titles': self.title,
                    'prop': 'revisions',
                    'ellimit': 1,
                    'action': 'query',
                'format': 'json'
                }
            response = requests.get(API_URL, params=params)
            revisions = response.json()['query']['pages'][self.pageid]
            return revisions[0]['timestamp']

        # return self._revision_timestamp


def page(title=None, pageid=None, auto_suggest=True, redirect=True, preload=False):
    '''
    Get a WikipediaPage object for the page with title `title` or the pageid
    `pageid` (mutually exclusive).

    Keyword arguments:

    * title - the title of the page to load
    * pageid - the numeric pageid of the page to load
    * auto_suggest - let Wikipedia find a valid page title for the query
    * redirect - allow redirection without raising RedirectError
    * preload - load content, summary, images, references, and links during initialization
    '''

    if title is not None:
        if auto_suggest:
            results, suggestion = search(title, results=1, suggestion=True)
            try:
                title = suggestion or results[0]
            except IndexError:
                # if there is no suggestion or search results, the page doesn't
                # exist
                raise PageError(title)
        return WikipediaPage(title, redirect=redirect, preload=preload)
    elif pageid is not None:
        return WikipediaPage(pageid=pageid, preload=preload)
    else:
        raise ValueError("Either a title or a pageid must be specified")

if __name__ == '__main__':
    wikipedia_page = WikipediaPage(title='Ukraine')
    timestamp = wikipedia_page.revision_timestamp
    pass