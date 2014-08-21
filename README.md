# extensible Web Retrieval Toolkit (eWRT)

The **Extensible Web Retrieval Toolkit (eWRT)** is a modular open-source Python API which 
  1. offers a unified interface for retrieving social data from Web sources such as Delicious, Flickr, Yahoo! and Wikipedia, 
  2. includes various helper classes for effective caching and data management,
  3. provides components for low-level natural language processing functionalities such as language detection, phonetic string similarity measures, and methods for string normalization.

## Quickstart:

adjust
  `eWRT/src/siteconfig.py-sample`
to your setting and save it to
*  `~/.eWRT/siteconfig.py` (user specific settings) and/or
* `/etc/eWRT/siteconfig.py` (system wide settings)

## Packages:

* `eWRT.access` - file, Web and database access
  * `db` - database access
  * `file` - file access
  * `http` - access web resources supporting authentication (basic, digest), compression, etc.
  * `javascript` - control Firefox to extract AJAX pages
* `eWRT.input` - input and cleanup modules
  * `clean` - clean and normalize text phrases
  * `conv` - convert doc, html and pdf files to text documents; convert XCL to rdf
  * `corpus` - input readers for the Reuters and BBC corpus
  * `csv` - read and analyze csv files
  * `stock` - stock quotes
* `eWRT.ontology` - tools for comparing, evaluating and visualizing ontologies
  * `compare` - compare ontology nodes, relations, and relation types
  * `eval` - determine the coherence of ontology nodes
  * `visualize` - visualize ontologies
* `eWRT.stat` - the eWRT statistics packages
  * `coherence` - compute the coherence between terms (Dice, PMI)
  * `metrics` - evaluation metrics (precision, recall, F1)
  * `language` - simple language detection
  * `string` - word (Levenshtein, Damerau-Levenshtein, Soundex, ...) and document (Vector Space Model) similarity metrics 
* `eWRT.util` - utility classes for transparent caching, logging, monitoring, etc.
  * `advLogging` - log to SNMP handler
  * `assert` - assertion based counters (decorators)
  * `async` - asynchronous procedure calls (experimental)
  * `cache` - transparent memory and disk caching of function calls (decorators)
  * `exception` - SNMP exception handling
  * `loggerProfile` - simplified logging
  * `module_path` - compute relative paths
  * `monitoring` - support for Nagios NSCA services
  * `pickleIterator` - iterate over objects stored in pickle files
  * `profile` - python profiling 
  * `timing` - time python methods (decorators)
* `eWRT.visualize` - eWRT visualization library
* `eWRT.ws` - Web service access (REST, Amazon, Flickr, Facebook, ...)
  * `amazon` 
  * `conceptnet`
  * `delicious`
  * `facebook` 
  * `flickr`
  * `geonames`
  * `google`
  * `googlealerts`
  * `googletrends`
  * `linkedin`
  * `opencalais`
  * `rest` - efficiently access/publish REST services
  * `rss`
  * `technorati`
  * `twitter`
  * `wikipedia`
  * `wordnet`
  * `wot`
  * `yahoo`
  * `youtube`

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


