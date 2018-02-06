#!/usr/bin/env python
"""
 @package eWRT.input.conv.html
 converts HTML pages into text
"""

# (C)opyrights 2009-2010 by Albert Weichselbraun <albert@weichselbraun.net>
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


from eWRT.config import CMD_CONV
from eWRT.util.execute import pipe_content


class HtmlToText(object):
    """ converts HTML into text
        requires a converter
    """

    @staticmethod
    def getText(html_content, encoding="utf8"):
        """ @param[in] html_content the content of the html page to convert 
            @param[in] encoding the document encoding 
            @returns the text representation of the Web page
        """
        # check whether this is really a html file
        if not "<" in html_content or not ">" in html_content:
            return html_content

        _, html = pipe_content(CMD_CONV['html'], html_content)
        return html


class TestHtmlToText(object):

    def testConversion(self):
        text = HtmlToText.getText(
            "<html><body><h1>Hallo</h1><ul><li>1</li><li>Jasna</li></ul></body></html>")
        assert 'Jasna' in text

    def testBorderCases(self):
        assert HtmlToText.getText("") == ""
        assert HtmlToText.getText("   ") == "   "
