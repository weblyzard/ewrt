#!/usr/bin/env python
"""
 @package eWRT.convert.html
 converts HTML pages into text
"""

# (C)opyrights 2009 by Albert Weichselbraun <albert@weichselbraun.net>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from eWRT.config import CMD_HTML_CONV
import subprocess

class HtmlToText(object):
    """ converts HTML into text
        requires a converter
    """

    @staticmethod
    def getText(text, encoding="utf8"):
        html = HtmlToText.execute( CMD_HTML_CONV, text )
        return html[1]

    @staticmethod
    def execute(cmd, stdin=None):
        """ @param[in] cmd command to be executed
            @param[in] stdin
            @param[in] stdout
        """
        if stdin:
            process_stdin = subprocess.PIPE
        else:
            process_stdin = None

        process_stdout = subprocess.PIPE
        p = subprocess.Popen( cmd.split(" "),
                              bufsize= 0,
                              shell  = False,
                              stdin  = process_stdin,
                              stdout = process_stdout )
        
        # write input to stdin, if present
        if stdin:
            p.stdin.write( stdin )
            p.stdin.close()

        # get stdout
        content = p.stdout.read()
        return ( p.wait(), content )



class TestHtmlToText(object):

    def testConversion(self):
        text =  HtmlToText.getText( "<html><body><h1>Hallo</h1><ul><li>1</li><li>Jasna</li></ul></body></html>" )
        assert 'Jasna' in text
