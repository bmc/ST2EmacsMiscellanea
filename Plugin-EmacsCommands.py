# This software is released under a BSD license, adapted from
# http://opensource.org/licenses/bsd-license.php
#
# See http://software.clapper.org/ST2EmacsMiscellanea
#
# Copyright (c) 2011 Brian M. Clapper.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name "clapper.org" nor the names of its contributors may be
#   used to endorse or promote products derived from this software without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sublime, sublime_plugin
import string
import textwrap
import re
import comment
import paragraph

class FixupWhitespaceCommand(sublime_plugin.TextCommand):
    '''
    FixupWhitespaceCommand is a Sublime Text 2 plugin command that emulates
    the Emacs (fixup-whitespace) command: It collapses white space behind
    and ahead of the cursor, leaving just one space. For compatibility with
    Emacs, if the cursor is in the first column, this plugin leaves no spaces.
    Also for compatibility with Emacs, if the character at point is not a
    white space character, insert one.
    '''

    def run(self, edit):
        sel = self.view.sel()
        if (sel is None) or (len(sel) == 0):
            return

        # Determine whether there's white space at the cursor.

        cursor_region = sel[0]
        point = cursor_region.begin()
        line = self.view.line(point)
        cur = self.view.substr(point)
        prev = self.view.substr(point - 1) if point > line.begin() else u'\x00'

        if prev.isspace():
            prefix_ws_region = self._handle_prefix_whitespace(point, line)
        else:
            prefix_ws_region = None

        if cur.isspace() and (not self._line_end(cur)):
            suffix_ws_region = self._handle_suffix_whitespace(point, line)
        else:
            suffix_ws_region = None

        if (suffix_ws_region is None) and (prefix_ws_region is None):
            # We're not on white space. Insert a blank.
            self.view.insert(edit, point, ' ')
        else:
            # Now do the actual delete.
            if suffix_ws_region is not None:
                self.view.erase(edit, suffix_ws_region)

            if prefix_ws_region is not None:
                self.view.erase(edit, prefix_ws_region)

            # Make sure there's one blank left, unless:
            #
            # a) the next character is not a letter or digit, or
            # b) the previous character is not a letter or digit, or
            # c) we're at the beginning of the line
            point = self.view.sel()[0].begin()
            bol = line.begin()
            if point > bol:
                def letter_or_digit(c):
                    return c.isdigit() or c.isalpha()

                c = self.view.substr(point)
                c_prev = self.view.substr(point - 1)

                if letter_or_digit(c) or letter_or_digit(c_prev):
                    self.view.insert(edit, point, ' ')
       
    def _handle_prefix_whitespace(self, point, line):
        p = point
        p -= 1
        c = self.view.substr(p)
        bol = line.begin()
        while (p > bol) and c.isspace():
            p -= 1
            c = self.view.substr(p)

        # "point" is now one character behind where we want it to be,
        # unless we're at the beginning of the line.
        if p > bol or (not c.isspace()):
            p += 1

        # Return the region of white space.
        return sublime.Region(p, point)

    def _handle_suffix_whitespace(self, point, line):
        p = point
        c = self.view.substr(p)
        bol = line.begin()
        eol = line.end()
        while (p <= eol) and (c.isspace()) and (not self._line_end(c)):
            p += 1
            c = self.view.substr(p)
        
        # Return the region of white space.
        return sublime.Region(point, p)

    def _line_end(self, c):
        return (c in ["\r", "\n", u'\x00'])
