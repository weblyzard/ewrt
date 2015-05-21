#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
@package eWRT.stat.language

language detection
"""
import re
from glob import glob
from os.path import basename

from eWRT.util.module_path import get_resource
from psycopg2.tests.testutils import unittest

def read_wordlist(fname):
    """ reads a language wordlist from a file """
    with open(fname) as f: 
        return set( map(str.lower, map(str.strip, f.readlines() )))

# returns the language name based on the language file's name
get_lang_name = lambda fname: basename(fname).split(".")[0]

LANG_DATA_DIR =  get_resource( __file__, ('data', ))

##
# \var STOPWORD_DICT: a dictionary of the 100 most common words in the given language
STOPWORD_DICT = { get_lang_name(fname): read_wordlist(fname) for fname in glob( LANG_DATA_DIR+"/*.csv") }
DELETE_CHARS = { ch: None for ch in ",.!?\"'" }


def detect_language(text):
    """ detects the most probable language for the given text """
    if not text.strip():
        return None

    text = text.lower()
    text = re.sub(r'[^\w]', ' ', text)
    words = map( unicode.strip, text.translate(DELETE_CHARS).split(" "))
    current_lang      = None
    current_wordcount = 0 
    for lang, reference_wordlist in STOPWORD_DICT.items():
        wordcount = sum( [ 1 for word in words if word in reference_wordlist ] )
        if wordcount >= current_wordcount and wordcount > 0:
            current_wordcount = wordcount
            current_lang = lang
            
    return current_lang




class DetectLanguageTest(unittest.TestCase):
    
    def test_detect_language(self):
        """ tests the language detection based on examples """
        
        text = u"#maryboo #health #baby #mom #food #cosmetics #love  http://t.co/nPqzL8MRKa"
        #RT @LesbianGIFs_: She's HOT AF 😩🔥 http://t.co/xZ2VFdAtNx
        print detect_language(text)
        
        text = u"""Das Glück der Erde liegt in diesem Fall im Dreck. Begeistert 
                  werfen sich die Schüler einer zweiten Klasse Volksschule
                  Erdklumpen auf die grünen T-Shirts. Andere rennen lachend herum, 
                  reißen verstohlen Sauerampfer aus dem Beet und stecken sich die
                  Blätter in den Mund."""
        
        print detect_language(text)
        assert detect_language(text) == 'de'
        
        text = u"""Deux nouveaux décès par crise cardiaque en lien avec la
                  consommation de boissons énergisantes ont été signalés aux
                  autorités sanitaires, a indiqué mercredi 6 juin au soir l'agence
                  de sécurité sanitaire pour l'alimentation (Anses).""" 
        
        assert detect_language(text) == 'fr'
    
        text = u"""Weniger 1V-Renten, mehr Pensionskassengelder ZÜRICH. Immer weniger Leute beziehen eine IVunsere PensionskassenGuthaben: Sie wachsen. Seit 2003 ist die Zahl der jährlich neu zugesprochenen Renten bei der Invalidenversicherung (IV) um mehr als 47% gesUnken. «Wir führen das auf die 5. IVG-Revision, die relativ stabile Wirtschaftslage und die Fortschritte bei der Wiedereingliederung zurück», sagt Zurich-Sprecher Frank Keidel. Vom starken Rückgang profitiert nicht nur die IV als erste Säule, sondern alle Erwerbstätigen. Denn dank der gesunkenen Zahl der Invaliden müssen auch die Pensionskassen weniger IV-Rentenbeiträge aus der zweiten Säule ausschütten. Unter dem Strich bleibt deshalb viel mehr Geld für die Altersvorsorge. Die Beiträge der zweiten Säule setzen sich zusammen aus IV-, Todesfall- und Kostenprämie. Eine Umfrage von 20 Minuten bei den Versicherungen zeigt, dass die Risikoprämten für Invalidität teils um 10 bis 20% gesenkt werden konnten. «Oberdurchschnittlich konnten wIr 2011 die Prämien im Gross- und Detailhandel, bei Optikern, Apotheken und Drogerien senken», so Allianz-Suisse-SprecherBernddeWall. Ebenfalls stark profitiert hätten Elektro-, Sanitär- und Lüftungsinstallateure, Maler, Gipser und Glaser Bei Swlss Life sanken die Prämien seit 2007 durchschnittlich um %. Auch Axa Wmterthur hat in den letzten Jahren die Taufe bereits dreimal gesenkt. Und mit der teilautonomen Sanimelstiftung Vita plant sie für 2013 eine durchschnittliche r? /2 1 1 IV-Renten sind rOckilufig. FOTOLIA Senkung der Prämien von rund 300 Franken pro versicherte Person. ELISABEflI RIZZI"""
    
        assert detect_language(text) == 'de'
       
    
    def test_exceptions(self):
        """ results for empyt strings """
        assert detect_language(u" ") == None
        assert detect_language(u"") == None

if __name__ == '__main__':
    unittest.main()