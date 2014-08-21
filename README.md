# easy Web Retrieval Toolkit (eWRT)

## Quickstart:

adjust
  `config.py.sample `
to your setting and save it as config.py

## Packages:

* `eWRT.access` - file, Web and database access
* `eWRT.input` - input and clearnup modules
* `eWRT.ontology` - tools for comparing, evaluating and visualizing ontologies
* `eWRT.stat` - the eWRT statistics packages
* `eWRT.util` - utility classes for transparent caching, logging, monitoring, etc.
* `eWRT.visualize` - eWRT visualization library
* `eWRT.ws` - Web service access (REST, Amazon, Flickr, Facebook, ...)

## Requirements:

* python-libraries:
   - facebook api - http://code.google.com/p/pyfacebook/
   - google-trends api - http://github.com/suryasev/unofficial-google-trends-api/tree/master
   - oauth - http://oauth.googlecode.com/
   - simplejson - http://pypi.python.org/pypi/simplejson/ 
   - tango - http://tango.ryanmcgrath.org/
   - python-rdflib
   - python-nltk
   - python-feedparser (eWRT.ws.rss)

* text conversion (eWRT.input.conv):
   - lynx 
   - pdftotext (poppler-utils)
   - antiword


