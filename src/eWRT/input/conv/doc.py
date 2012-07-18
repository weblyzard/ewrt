#!/usr/bin/env python
"""
 @package eWRT.input.conv.doc
 converts Microsoft Word documents into text
"""

# (C)opyrights 2009-2012 by Albert Weichselbraun <albert@weichselbraun.net>
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
    def getText(word_document_content):
        """ @param[in] word_document_content the content of the html page to convert 
            @param[in] encoding the document encoding 
            @returns the text representation of the Web page
        """
        _, html = pipe_content( CMD_CONV['doc'], word_document_content )
        return html
