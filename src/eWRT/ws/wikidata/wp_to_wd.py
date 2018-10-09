import pywikibot
import wikipedia

# class WikiPage:
#
#     def __init__(self, title, language='en', site=None):
#         self.itempage = wikidata_from_wptitle(title, language, site)


def wikidata_from_wptitle(title, language='de'
                                          '', site=None):
    """"""
    if site is None:
        site = pywikibot.Site(language, 'wikipedia')
    page = pywikibot.Page(site, title=title)
    item  = page.data_item()
    return item
