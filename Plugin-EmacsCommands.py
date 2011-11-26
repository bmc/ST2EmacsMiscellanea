import sublime, sublime_plugin
import string
import textwrap
import re
import comment
import paragraph

class EmacsOpenLineCommand(sublime_plugin.TextCommand):
    '''
    Emacs-style 'open-line' command: Inserts a newline at the current
    cursor position, without moving the cursor like Sublime's insert
    command does.
    '''
    def run(self, edit):
        sel = self.view.sel()
        if (sel is None) or (len(sel) == 0):
            return

        point = sel[0].end()
        self.view.insert(edit, point, '\n')
        self.view.run_command('move', {'by': 'characters', 'forward': False})

class FixupWhitespaceCommand(sublime_plugin.TextCommand):
    '''
    FixupWhitespaceCommand is a Sublime Text 2 plugin command that emulates
    the Emacs (fixup-whitespace) command: It collapses white space behind
    and ahead of the cursor, leaving just one space. For compatibility with
    Emacs, if the cursor is in the first column, this plugin leaves no spaces.
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

            if letter_or_digit(c) and letter_or_digit(c_prev):
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

class WrapParagraphCommand(paragraph.WrapLinesCommand):
    """
    The Sublime "wrap_width" setting controls both on-screen wrapping and
    the column at which the WrapLinesCommand folds lines. Those two
    settings should be different; otherwise, things don't look right
    on the screen. This plugin looks for a "wrap_paragraph" setting and,
    if found, uses that value to override the value of "wrap_width". Then,
    it invokes the stock SublimeText "wrap_lines" command.

    Bind "wrap_paragraph" to a key to use this command.

    See related bug report: http://sublimetext.userecho.com/topic/82731-/
    """
    def run(self, edit, width=0):
        if width == 0 and self.view.settings().get("wrap_paragraph"):
            try:
                width = int(self.view.settings().get("wrap_paragraph"))
            except TypeError:
                pass

        super(WrapParagraphCommand, self).run(edit, width)

class RecenterInView(sublime_plugin.TextCommand):
    '''
    Reposition the view so that the line containing the cursor is at the
    center of the viewport, if possible. Unlike the corresponding Emacs
    command, recenter-top-bottom, this command does not cycle through
    scrolling positions. It always repositions the view the same way.

    This command is frequently bound to Ctrl-l.
    '''
    def run(self, edit):
        self.view.show_at_center(self.view.sel()[0])