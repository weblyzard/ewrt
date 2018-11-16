"""
From the Wikipedia title in a specific language, identify the Wikidata
entity it refers to and return it as a pywikibot.Page
"""


try:
    import pywikibot
except RuntimeError:
    import os
    os.environ['PYWIKIBOT_NO_USER_CONFIG'] = '1'
    import pywikibot


def wikidata_from_wptitle(title, language='de'
                                          '', site=None):
    """"""
    if site is None:
        site = pywikibot.Site(language, 'wikipedia')
    page = pywikibot.Page(site, title=title)
    item  = page.data_item()
    return item
