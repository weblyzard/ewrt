from eWRT.ws.wikidata.postprocess_geo import item_with_country


def test_item_with_country():
    """
    The order of the local_attributes determines which is used first, thus
    which is returned as 'the' country of an entity
    :return:
    """
    # birth_place first:
    assert item_with_country('Sigmund Freud', 'en',
                             ['P19', 'P27']) == 'Czech Republic'
    # citizenship first:
    assert item_with_country('Sigmund Freud', 'en', ['P27', 'P19']) == 'Austria'
