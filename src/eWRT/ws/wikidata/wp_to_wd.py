import warnings

import pywikibot

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
        return is_preferred(location_page.claims['P17'])
    except KeyError:
        raise ValueError('No country found for this location!')



def is_preferred(claim_instances):
    if len(claim_instances) == 1:
        return [claim_instances[0].target]
    else:
        preferred = [claim for claim in claim_instances if claim.rank == 'preferred']
        if len(preferred) == 1:
            return [claim.target for claim in preferred]
        elif len(preferred):
            warnings.warn('No claim instance marked as preferred!')
            return [claim.target for claim in preferred]
        else:
            warnings.warn(
                'Incorrectly tagged data: several instances marked as preferred, this should not happen!')
            return [claim.target for claim in preferred]

#
# london_country = get_country_from_location('Q84')
# print(london_country)