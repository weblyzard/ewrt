""" @package eWRT.util.execute
    Helpers for executing third party modules
"""

# (C)opyrights 2008-2012 by Albert Weichselbraun <albert@weichselbraun.net>
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

__author__    = "Albert Weichselbraun"
__revision__  = "$Id$"
__copyright__ = "GPL"

from subprocess import PIPE, Popen
from os.path import isfile


def pipe_content(cmd, stdin=None):
    """ Pipes the content through the given command.
        @param[in] cmd:   command to be executed
        @param[in] stdin: standard input
        @return: (exit_status, stdout)
    """
    if not isfile(cmd.split(" ")[0]):
        raise ValueError, "Command %s is not available." % (cmd)
    
    if stdin:
        process_stdin = PIPE
    else:
        process_stdin = None

    process_stdout = PIPE
    p = Popen( cmd.split(" "),
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



class TestExecute(object):
    
    def test_pipe_content(self):
        assert pipe_content("/bin/grep 22", "12\n22\n33") == (0, "22\n")
        