import warnings

import pywikibot

from wikibot_parse_item import ParseItemPage

class WikiPage:

    def __init__(self, title, language='en', site=None):
        self.itempage = wikidata_from_wptitle(title,language,site)

def wikidata_from_wptitle(title, language='en', site=None):
    if site is None:
        site = pywikibot.Site(language, 'wikipedia')
    page = pywikibot.Page(site, title=title)
    item = pywikibot.ItemPage.fromPage(page)
    return item


def get_country_from_location(location_page):
    """Try to get country info when some sub-country level
    location attribute, but not country itself, is present."""
    location_page.get()
    try:
        return ParseItemPage.attribute_preferred_values(location_page.claims['P17'])
    except KeyError:
        raise ValueError('No country found for this location!')

