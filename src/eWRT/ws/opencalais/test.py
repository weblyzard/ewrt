from __init__ import Calais
import unittest



class TestCalais( unittest.TestCase ):
    ''' Testing GoogleTrends webservice '''
    
    test_html = '''  
  <html>
  <head>
  <title>test</title>
  </head>
  <body>
  <div class="content">
    <h1>Input Content</h1>
<h2>Language</h2>
<p>OpenCalais today supports content in English, French and Spanish. OpenCalais applies a Language Identification module before processing the text for entities, events and facts. This module might fail to recognize the language if the submitted text length is small.</p>
<p>If the submitted content is less than 100 characters and the language cannot be recognized, OpenCalais will assume the language is English by default and and the English module will process the text for entities, events and facts. In addition, in such cases, OpenCalais will return &quot;Input Text Too Short&quot; as the language code in the RDF.</p>
<h2>HTML Cleaning</h2>
<p>A document coded in HTML usually contains much more information than what is perceived as &ldquo;new and relevant textual content&rdquo;. This information might be:</p>

<ul type="disc">
<li>The HTML tags</li>
<li>Various metadata</li>
<li>Browsing menus</li>
<li>Advertisements</li>
<li>Links to other service providers like Facebook or Digg.</li>
<li>Links to other HTML pages on the same site that are not part of the main content frame.</li>
<li>General information about the hosting site, including copyright notice, etc.</li>
</ul>
<p>In order to optimize extraction and categorization results or, for that matter, any semantic-related algorithm operating on the text, we opt for the text to be as free as possible from the above objects.</p>

<p>The HTML cleaner aims to clean the text as much as possible of these objects, leaving only a basic HTML structure that contains only the new and relevant data. It does so using both HTML-structural and machine-learning-based heuristics.&nbsp;</p>
<h2>Format&nbsp;</h2>
<p>OpenCalais supports four formats of content: TEXT/HTML, TEXT/HTMLRAW, TEXT/XML and TEXT/RAW.</p>
<p>When no content type is specified, Calais attempts to auto-detect the type (one of: TEXT/XML, TEXT/HTML or TEXT/RAW).</p>
<p><strong><em>Note:</em></strong><em> </em>TEXT/TXT is no longer used. If this type is given, it is processed as though the contentType value was TEXT/RAW and the results appears as TEXT/RAW.</p>
<p><strong>TEXT/HTML:</strong> No conversion of the submitted content, will remove irrelevant text content as well as HTML tags and scripts. Entity and event detection will be relative to the cleansed text. For optimal results it is recommended to use this contentType when submitting HTML content.</p>
<p><strong>TEXT/HTMLRAW:</strong> Will apply OpenCalais' legacy converter and limited cleansing, removing only HTML tags and scripts, This is equivalent to TEXT/HTML of previous versions.</p>

<p><strong>TEXT/XML:</strong> Will apply the XML converter for escaping the necessary characters, hence entity and event detection will be relative to the cleansed text. For optimal results it is recommended to use this contentType when submitting XML content. The XML converter also supports the NewsML standard.</p>
<p>If the content is submitted as TEXT/XML, OpenCalais will process the following XML nodes:</p>
</div>
</body>
</html>
 ''' 
    
    def setUp(self):
        self.c = Calais('heinz')
        

    def testAnalyze(self):
        things = self.c.analyze(self.test_html, 'text/html')
        print things
        assert len(things) == 6

if __name__ == '__main__':
    unittest.main()