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
