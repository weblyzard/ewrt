query = """SELECT ?item WHERE{
  ?item wdt:P31* wd:Q515.
  ?item wdt:P1082 ?population.
  FILTER(?population > 50000)
  }"""